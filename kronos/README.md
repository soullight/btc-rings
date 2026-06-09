# Kronos Forecaster — BTC / ETH / SOL / ZEC

Local producer for the `kronos.html` dashboard. AAAI-2026 foundation-model 24h
directional forecast. **Confirmation signal only — Edge is the call, pattern wins,
Kronos gets no vote.**

Full spec + all links: [`../KRONOS_SPEC.md`](../KRONOS_SPEC.md)

## Run

```bash
cd code/btc-rings-site/kronos
python3 kronos_forecast.py                 # forecast all 4 assets -> kronos_signals.json
python3 kronos_validate.py 30 12 20        # walk-forward backtest -> kronos_validation.json
cd .. && python3 -m http.server 8099       # open http://localhost:8099/kronos.html
```

First run downloads `Kronos-mini` + `Kronos-Tokenizer-2k` from HuggingFace (~tens of MB).
A full 4-asset forecast is seconds on Apple Silicon (MPS). Validation is heavier
(minutes-to-tens-of-minutes depending on window/step/paths).

## Why local-only
Binance/most price APIs return 403/451 in the sandbox/cron host (see
`../signal-history.json`). This runs on Lawrence's Mac and writes static JSON the
dashboard reads. Source: `data-api.binance.vision` (Binance global mirror, not
US-geo-blocked); fallback `api.binance.us`.

## Files
- `kronos_lib.py` — shared core: data fetch, model load, MC paths, signal math
- `kronos_forecast.py` — multi-asset live forecast driver
- `kronos_validate.py [window_days] [step_h] [n_paths]` — walk-forward validation
- `kronos_signals.json` — combined (consumed by `../kronos.html`)
- `signals/kronos_<ASSET>.json` — per-asset · `kronos_signal.json` — BTC back-compat
- `kronos_history.json` — rolling log · `kronos_validation.json` — backtest scorecard

## Assets
Edit `ASSETS` in `kronos_lib.py` to add/remove. Currently BTC, ETH, SOL, ZEC.

## Model code
Vendored at `code/Kronos/` (cloned from https://github.com/shiyu-coder/Kronos, MIT).
