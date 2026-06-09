#!/usr/bin/env python3
"""
Kronos walk-forward validation — does the upside_probability signal actually
predict 24h direction?

For each eval point t (stepped back through history): take 360h of context
ending at t, run Kronos Monte-Carlo, read upside_probability, then compare to
the REALIZED outcome (was close[t+24h] actually higher than close[t]?).

Metrics per asset:
  - n                  eval points
  - base_rate          fraction of points that actually went up (the naive baseline)
  - hit_rate           directional accuracy (pred up if prob>0.5)
  - brier              mean( (prob - realized)^2 ), lower better; 0.25 = always-0.5 guess
  - brier_skill        1 - brier/brier_baseline  (>0 beats the base-rate guess)
  - high_conf_hit_rate accuracy on points where |prob-0.5| >= 0.15 (the calls it's sure about)
  - mean_prob          calibration sanity check vs base_rate

This is the gate before sizing on Kronos. Per VALIDATION.md discipline.
Config is conservative for runtime; widen WINDOW_DAYS / N_PATHS_VAL for rigor.
"""
import json
import sys
from datetime import datetime, timezone

import numpy as np

import kronos_lib as K

WINDOW_DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 30   # eval span
STEP_H = int(sys.argv[2]) if len(sys.argv) > 2 else 12        # hours between eval points
N_PATHS_VAL = int(sys.argv[3]) if len(sys.argv) > 3 else 20   # paths per eval (speed/accuracy)


def validate_asset(predictor, name, symbol):
    eval_points = (WINDOW_DAYS * 24) // STEP_H
    # need: LOOKBACK context + (eval span) + PRED_LEN forward, with margin
    need = K.LOOKBACK + WINDOW_DAYS * 24 + K.PRED_LEN + STEP_H + 50
    full = K.fetch_klines_paged(symbol, total=need)
    closes = full["close"].to_numpy(dtype=float)
    ts = full["ts"]
    ohlcv_cols = ["open", "high", "low", "close", "volume", "amount"]
    n_bars = len(full)
    if n_bars < K.LOOKBACK + K.PRED_LEN + STEP_H * 2:
        print(f"  {name}: insufficient history ({n_bars} bars) — skipping")
        return None

    # last index where we still have PRED_LEN future bars to grade against
    last_eval = n_bars - K.PRED_LEN - 1
    first_eval = max(K.LOOKBACK, last_eval - eval_points * STEP_H)
    idxs = list(range(first_eval, last_eval + 1, STEP_H))

    probs, realized = [], []
    print(f"  {name}: {len(idxs)} eval points over {n_bars} bars...")
    for j, t in enumerate(idxs):
        ctx = full.iloc[t - K.LOOKBACK:t]
        df = ctx[ohlcv_cols].reset_index(drop=True)
        x_ts = ts.iloc[t - K.LOOKBACK:t].reset_index(drop=True)
        c0 = closes[t - 1]
        try:
            close_paths, _ = K.run_paths(predictor, df, x_ts,
                                         pred_len=K.PRED_LEN, n_paths=N_PATHS_VAL)
        except Exception as e:  # noqa: BLE001
            print(f"    point {t} failed: {e}")
            continue
        prob_up = float(np.mean(close_paths[:, -1] > c0))
        realized_up = 1.0 if closes[t - 1 + K.PRED_LEN] > c0 else 0.0
        probs.append(prob_up)
        realized.append(realized_up)
        print(f"    {j+1}/{len(idxs)}  prob_up={prob_up:.2f}  realized={'UP' if realized_up else 'DN'}", end="\r")
    print()

    probs = np.array(probs)
    realized = np.array(realized)
    n = len(probs)
    if n == 0:
        return None
    base_rate = float(realized.mean())
    pred_dir = (probs > 0.5).astype(float)
    hit_rate = float((pred_dir == realized).mean())
    brier = float(np.mean((probs - realized) ** 2))
    brier_base = float(np.mean((base_rate - realized) ** 2)) or 1e-9
    brier_skill = float(1 - brier / brier_base)
    mean_prob = float(probs.mean())

    hc = np.abs(probs - 0.5) >= 0.15
    hc_hit = float((pred_dir[hc] == realized[hc]).mean()) if hc.sum() else None

    return {
        "name": name, "symbol": symbol, "n": n,
        "base_rate_up": round(base_rate, 4),
        "hit_rate": round(hit_rate, 4),
        "brier": round(brier, 4),
        "brier_skill": round(brier_skill, 4),
        "high_conf_n": int(hc.sum()),
        "high_conf_hit_rate": round(hc_hit, 4) if hc_hit is not None else None,
        "mean_prob": round(mean_prob, 4),
    }


def main():
    predictor = K.load_predictor()
    print(f"[validate] window={WINDOW_DAYS}d step={STEP_H}h paths={N_PATHS_VAL}\n")
    results = []
    for name, symbol in K.ASSETS:
        try:
            r = validate_asset(predictor, name, symbol)
        except Exception as e:  # noqa: BLE001
            print(f"  {name} FAILED: {e}")
            continue
        if r:
            results.append(r)

    out = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "model": K.MODEL_ID, "window_days": WINDOW_DAYS, "step_hours": STEP_H,
        "n_paths": N_PATHS_VAL, "horizon_hours": K.PRED_LEN, "lookback_hours": K.LOOKBACK,
        "note": "hit_rate vs base_rate_up = directional edge. brier_skill>0 beats naive. "
                "high_conf = points where |prob-0.5|>=0.15. Gate before sizing on Kronos.",
        "results": results,
    }
    (K.HERE / "kronos_validation.json").write_text(json.dumps(out, indent=2))

    print("\n=== KRONOS VALIDATION ===")
    print(f"{'asset':5s} {'n':>4s} {'base↑':>6s} {'hit':>6s} {'brier':>6s} {'skill':>6s} {'HCn':>4s} {'HChit':>6s}")
    for r in results:
        hc = f"{r['high_conf_hit_rate']*100:5.1f}%" if r['high_conf_hit_rate'] is not None else "  n/a"
        print(f"{r['name']:5s} {r['n']:4d} {r['base_rate_up']*100:5.1f}% {r['hit_rate']*100:5.1f}% "
              f"{r['brier']:.3f} {r['brier_skill']:+.3f} {r['high_conf_n']:4d} {hc}")
    print("\n[validate] wrote kronos_validation.json")


if __name__ == "__main__":
    main()
