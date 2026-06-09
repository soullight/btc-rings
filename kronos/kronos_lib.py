"""
Shared Kronos forecasting core. Used by kronos_forecast.py (live multi-asset
signal) and kronos_validate.py (walk-forward backtest).

Confirmation signal only. Edge is the call. Pattern wins. (See ../KRONOS_SPEC.md)
"""
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests

HERE = Path(__file__).resolve().parent


def _find_kronos_repo():
    """Locate the vendored Kronos model code. Works on the Mac (code/Kronos) and
    on the Nevada tracker host (~/kronos-tracker/Kronos)."""
    env = os.environ.get("KRONOS_REPO")
    candidates = ([Path(env)] if env else []) + [
        HERE / "Kronos",            # tracker layout: alongside this file
        HERE.parent.parent / "Kronos",  # repo layout: code/Kronos
    ]
    for c in candidates:
        if (c / "model").is_dir():
            return c
    return candidates[-1]


KRONOS_REPO = _find_kronos_repo()   # vendored model code, MIT

# Asset universe: (display name, exchange symbol)
ASSETS = [("BTC", "BTCUSDT"), ("ETH", "ETHUSDT"), ("SOL", "SOLUSDT"), ("ZEC", "ZECUSDT")]

INTERVAL = "1h"
PRED_LEN = 24           # forecast horizon (hours)
N_PATHS = 30            # Monte Carlo paths for live signal

# Model is env-configurable so we can A/B mini vs base vs large on the same data.
# mini: Tokenizer-2k, ctx 2048, 4.1M.  base/small: Tokenizer-base, ctx 512, 102M/24.7M.
MODEL_ID = os.environ.get("KRONOS_MODEL_ID", "NeoQuasar/Kronos-mini")
TOKENIZER_ID = os.environ.get("KRONOS_TOKENIZER_ID", "NeoQuasar/Kronos-Tokenizer-2k")
MAX_CONTEXT = int(os.environ.get("KRONOS_MAX_CONTEXT", "2048"))
LOOKBACK = int(os.environ.get("KRONOS_LOOKBACK", "360"))   # context bars (<= MAX_CONTEXT)

# binance.vision = Binance global K-line mirror, NOT US-geo-blocked. Fallback: binance.us
KLINE_SOURCES = [
    "https://data-api.binance.vision/api/v3/klines",
    "https://api.binance.us/api/v3/klines",
]
_COLS = ["open_time", "open", "high", "low", "close", "volume",
         "close_time", "amount", "trades", "tb_base", "tb_quote", "ignore"]


def _parse(raw):
    df = pd.DataFrame(raw, columns=_COLS)
    for c in ["open", "high", "low", "close", "volume", "amount"]:
        df[c] = df[c].astype(float)
    df["ts"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    return df


def fetch_klines(symbol, interval=INTERVAL, limit=LOOKBACK):
    """Most recent `limit` bars (<=1000). Returns (ohlcv_df, ts_series)."""
    last_err = None
    for base in KLINE_SOURCES:
        try:
            r = requests.get(base, params={"symbol": symbol, "interval": interval,
                                           "limit": limit}, timeout=20)
            r.raise_for_status()
            raw = r.json()
            if not isinstance(raw, list) or not raw:
                raise ValueError(f"empty payload from {base}")
            df = _parse(raw)
            return (df[["open", "high", "low", "close", "volume", "amount"]].reset_index(drop=True),
                    df["ts"].reset_index(drop=True))
        except Exception as e:  # noqa: BLE001
            last_err = e
            print(f"[data] {base.split('/')[2]} failed for {symbol}: {e}")
    raise RuntimeError(f"all kline sources failed for {symbol}; last: {last_err}")


def fetch_klines_paged(symbol, interval=INTERVAL, total=1500):
    """Page backward to assemble `total` recent bars (for validation). Returns full df with ts col."""
    base = KLINE_SOURCES[0]
    frames, end_time, got = [], None, 0
    while got < total:
        params = {"symbol": symbol, "interval": interval, "limit": min(1000, total - got)}
        if end_time is not None:
            params["endTime"] = end_time
        r = requests.get(base, params=params, timeout=20)
        r.raise_for_status()
        raw = r.json()
        if not raw:
            break
        df = _parse(raw)
        frames.append(df)
        got += len(df)
        end_time = int(df["open_time"].iloc[0]) - 1   # step before earliest bar
        if len(df) < params["limit"]:
            break
        time.sleep(0.15)
    full = pd.concat(frames).sort_values("open_time").drop_duplicates("open_time").reset_index(drop=True)
    return full


_PREDICTOR = None


def load_predictor():
    """Load Kronos-mini once and cache (reused across assets / eval points)."""
    global _PREDICTOR
    if _PREDICTOR is not None:
        return _PREDICTOR
    sys.path.insert(0, str(KRONOS_REPO))
    import torch
    from model import Kronos, KronosTokenizer, KronosPredictor

    device = "mps" if torch.backends.mps.is_available() else (
        "cuda" if torch.cuda.is_available() else "cpu")
    print(f"[model] device={device}  loading {MODEL_ID} ...")
    tok = KronosTokenizer.from_pretrained(TOKENIZER_ID)
    mdl = Kronos.from_pretrained(MODEL_ID)
    _PREDICTOR = KronosPredictor(mdl, tok, device=device, max_context=MAX_CONTEXT)
    return _PREDICTOR


def run_paths(predictor, df, x_ts, pred_len=PRED_LEN, n_paths=N_PATHS, T=1.0, top_p=0.9):
    """N independent sampled paths (sample_count=1 each -> a true distribution). Returns close paths (N, pred_len)."""
    freq = x_ts.diff().median()
    y_ts = pd.Series([x_ts.iloc[-1] + freq * (i + 1) for i in range(pred_len)])
    paths = []
    for _ in range(n_paths):
        pred = predictor.predict(df=df, x_timestamp=x_ts, y_timestamp=y_ts,
                                 pred_len=pred_len, T=T, top_p=top_p,
                                 sample_count=1, verbose=False)
        paths.append(pred["close"].to_numpy(dtype=float))
    return np.vstack(paths), y_ts


def read_label(upside_prob):
    if upside_prob >= 0.65:
        return "BULLISH CONFIRM"
    if upside_prob >= 0.55:
        return "LEAN BULLISH"
    if upside_prob > 0.45:
        return "NEUTRAL"
    if upside_prob > 0.35:
        return "LEAN BEARISH"
    return "BEARISH CONFIRM"


def compute_signal(close_paths, last_close, hist_closes, pred_len=PRED_LEN):
    final = close_paths[:, -1]
    upside_prob = float(np.mean(final > last_close))
    mean_path = close_paths.mean(axis=0)
    p10 = np.percentile(close_paths, 10, axis=0)
    p50 = np.percentile(close_paths, 50, axis=0)
    p90 = np.percentile(close_paths, 90, axis=0)
    expected_return = float(mean_path[-1] / last_close - 1.0)

    hist_ret = np.diff(np.log(hist_closes[-(pred_len + 1):]))
    realized_vol = float(np.std(hist_ret))
    path_vols = np.std(np.diff(np.log(close_paths), axis=1), axis=1)
    vol_amplification = float(np.mean(path_vols > realized_vol))
    forecast_vol = float(np.mean(path_vols))

    return {
        "upside_probability": round(upside_prob, 4),
        "read": read_label(upside_prob),
        "expected_return": round(expected_return, 5),
        "volatility_amplification": round(vol_amplification, 4),
        "forecast_vol_hourly": round(forecast_vol, 5),
        "realized_vol_hourly": round(realized_vol, 5),
        "last_close": round(float(last_close), 4),
        "mean_target": round(float(mean_path[-1]), 4),
        "mean_path": [round(float(v), 4) for v in mean_path],
        "p10": [round(float(v), 4) for v in p10],
        "p50": [round(float(v), 4) for v in p50],
        "p90": [round(float(v), 4) for v in p90],
    }
