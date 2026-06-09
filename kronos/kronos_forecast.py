#!/usr/bin/env python3
"""
Kronos multi-asset directional forecaster — BTC / ETH / SOL / ZEC.

For each asset: pull the last LOOKBACK hours of 1h K-lines, run Kronos-mini
Monte-Carlo (N independent paths), and write a confirmation signal:
  - upside_probability        P(price higher in PRED_LEN hours)
  - volatility_amplification  P(forecast vol > recent realized vol)
  - mean forecast path + p10/p50/p90 cone

Mirrors the author's live demo: https://shiyu-coder.github.io/Kronos-demo/
RUN LOCALLY (Apple Silicon). Writes static JSON the kronos.html dashboard reads.

Role: CONFIRMATION signals. Edge is the call. Pattern wins. Kronos does not get
a vote. (See ../KRONOS_SPEC.md)
"""
import json
from datetime import datetime, timezone

import kronos_lib as K


def forecast_asset(predictor, name, symbol):
    df, x_ts = K.fetch_klines(symbol, limit=K.LOOKBACK)
    last_close = float(df["close"].iloc[-1])
    hist_closes = df["close"].to_numpy(dtype=float)
    close_paths, y_ts = K.run_paths(predictor, df, x_ts)
    sig = K.compute_signal(close_paths, last_close, hist_closes)
    sig.update({
        "name": name,
        "symbol": symbol,
        "context_last_ts_utc": x_ts.iloc[-1].strftime("%Y-%m-%d %H:%M:%S"),
        "forecast_ts_utc": [t.strftime("%Y-%m-%d %H:%M") for t in y_ts],
    })
    print(f"  {name:4s} {sig['read']:16s} up={sig['upside_probability']*100:5.1f}%  "
          f"er={sig['expected_return']*100:+.2f}%  volamp={sig['volatility_amplification']*100:4.0f}%  "
          f"${last_close:,.2f} -> ${sig['mean_target']:,.2f}")
    return sig


def main():
    predictor = K.load_predictor()
    now = datetime.now(timezone.utc)
    sig_dir = K.HERE / "signals"
    sig_dir.mkdir(exist_ok=True)

    print(f"[forecast] {len(K.ASSETS)} assets, {K.N_PATHS} paths, {K.PRED_LEN}h horizon\n")
    assets_out = []
    for name, symbol in K.ASSETS:
        try:
            sig = forecast_asset(predictor, name, symbol)
        except Exception as e:  # noqa: BLE001
            print(f"  {name:4s} FAILED: {e}")
            continue
        assets_out.append(sig)
        (sig_dir / f"kronos_{name}.json").write_text(json.dumps(
            {"generated_utc": now.strftime("%Y-%m-%d %H:%M:%S"), "model": K.MODEL_ID,
             "lookback_hours": K.LOOKBACK, "horizon_hours": K.PRED_LEN, "n_paths": K.N_PATHS,
             "interval": K.INTERVAL, **sig}, indent=2))

    combined = {
        "generated_utc": now.strftime("%Y-%m-%d %H:%M:%S"),
        "model": K.MODEL_ID, "lookback_hours": K.LOOKBACK, "horizon_hours": K.PRED_LEN,
        "n_paths": K.N_PATHS, "interval": K.INTERVAL, "assets": assets_out,
    }
    (K.HERE / "kronos_signals.json").write_text(json.dumps(combined, indent=2))

    # backward-compat: BTC-only file the original single-asset dashboard read
    btc = next((a for a in assets_out if a["name"] == "BTC"), None)
    if btc:
        (K.HERE / "kronos_signal.json").write_text(json.dumps(
            {"generated_utc": now.strftime("%Y-%m-%d %H:%M:%S"), "symbol": btc["symbol"],
             "interval": K.INTERVAL, "lookback_hours": K.LOOKBACK, "horizon_hours": K.PRED_LEN,
             "n_paths": K.N_PATHS, "model": K.MODEL_ID, **btc}, indent=2))

    # rolling history (one row per asset per run)
    hist_path = K.HERE / "kronos_history.json"
    history = json.loads(hist_path.read_text()) if hist_path.exists() else []
    for a in assets_out:
        history.append({"generated_utc": now.strftime("%Y-%m-%d %H:%M:%S"), "name": a["name"],
                        "read": a["read"], "upside_probability": a["upside_probability"],
                        "expected_return": a["expected_return"],
                        "volatility_amplification": a["volatility_amplification"],
                        "last_close": a["last_close"], "mean_target": a["mean_target"]})
    hist_path.write_text(json.dumps(history[-2000:], indent=2))

    print(f"\n[forecast] wrote kronos_signals.json (+ per-asset) for {len(assets_out)} assets")


if __name__ == "__main__":
    main()
