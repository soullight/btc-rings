# KRONOS — Foundation Model for Market Direction · BUILD SPEC

*Portable spec. Hand this to any AI agent and it can reproduce or extend the build. Written 2026-06-09. Self-contained — all links inline.*

> **Build status (2026-06-09):** ✅ Multi-asset forecaster live (BTC / ETH / SOL / ZEC) · ✅ walk-forward validation harness built + run · ✅ multi-asset dashboard (`kronos.html`) · ✅ wired into the signal-router as a labeled NON-VOTING fragment (`SIGNAL-ROUTER-PLAYBOOK.md` + `nav.html`).

---

## 0. TL;DR

**Kronos** is the first open-source *foundation model for financial candlesticks (K-lines)* — a decoder-only transformer pre-trained on **12B+ K-line records from 45 global exchanges**, accepted to **AAAI 2026**. You feed it recent OHLCV bars; it autoregressively generates probable future bars. Run it Monte-Carlo style (many sampled paths) and you get a **probability distribution over future price**, from which you read:

- **Upside probability** — % of sampled paths where price is higher N hours out
- **Volatility amplification** — % of paths where forecast volatility exceeds recent realized vol
- A **mean forecast path** + uncertainty cone

The author's own live demo does exactly this for BTC/USDT, 24h ahead, hourly: **https://shiyu-coder.github.io/Kronos-demo/**

It is **MIT-licensed**, the public models are **tiny** (4.1M–102M params), and they run in **seconds on Apple Silicon (MPS)** or CPU. No API, no cost, fully local.

**Role in Lawrence's stack:** a NEW *confirmation signal* in the btc-rings-site family — never a veto. Edge stays the call (see `PLAYBOOK.md`). Kronos is one more institutional cross-check, and per the top-priority trading principle, **pattern wins; Kronos does not get a vote over a pattern read.** It supplies probability, not authority.

---

## 1. ALL THE LINKS

| What | URL |
|---|---|
| **GitHub (official, shiyu-coder)** | https://github.com/shiyu-coder/Kronos |
| **Paper (arXiv 2508.02739)** | https://arxiv.org/abs/2508.02739 · HTML: https://arxiv.org/html/2508.02739v1 |
| **Live BTC/USDT demo** | https://shiyu-coder.github.io/Kronos-demo/ |
| **HF — Tokenizer (base)** | https://huggingface.co/NeoQuasar/Kronos-Tokenizer-base |
| **HF — Tokenizer (2k)** | https://huggingface.co/NeoQuasar/Kronos-Tokenizer-2k |
| **HF — Kronos-mini** | https://huggingface.co/NeoQuasar/Kronos-mini |
| **HF — Kronos-small** | https://huggingface.co/NeoQuasar/Kronos-small |
| **HF — Kronos-base** | https://huggingface.co/NeoQuasar/Kronos-base |
| **Author** | Yu Shi & team |
| **License** | MIT |

---

## 2. THE MODEL FAMILY

| Model | Tokenizer | Context | Params | Public? | Best for |
|---|---|---|---|---|---|
| **Kronos-mini** | Kronos-Tokenizer-2k | **2048** | 4.1M | ✅ | Long lookback (the demo uses this — 360h context) |
| **Kronos-small** | Kronos-Tokenizer-base | 512 | 24.7M | ✅ | Short-context, higher capacity |
| **Kronos-base** | Kronos-Tokenizer-base | 512 | 102.3M | ✅ | Highest public capacity, 512 ctx |
| Kronos-large | Kronos-Tokenizer-base | 512 | 499.2M | ❌ proprietary | — |

**Architecture (two-stage):** (1) a specialized tokenizer **quantizes** continuous multi-dim OHLCV K-lines into *hierarchical discrete tokens* (two token streams, "pre"/s1 and "post"/s2); (2) an **autoregressive transformer** is pre-trained on those tokens. Forecasting = sample the next tokens, decode back to OHLCV.

**Reported results (paper):** new SOTA on price-series forecasting — **+93% RankIC** over leading time-series foundation models, **+87%** over best non-pretrained baseline; **9% lower MAE** on volatility forecasting; **22%** better generative fidelity for synthetic K-lines. Treat as authors' benchmarks — *we validate on our own walk-forward before trusting it with size.*

---

## 3. HOW INFERENCE WORKS (the API surface)

```python
from model import Kronos, KronosTokenizer, KronosPredictor

tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-2k")   # 2k for mini
model     = Kronos.from_pretrained("NeoQuasar/Kronos-mini")
predictor = KronosPredictor(model, tokenizer, device="mps", max_context=2048)  # cpu/cuda/mps

pred_df = predictor.predict(
    df=x_df,                 # pandas DF with columns: open, high, low, close [, volume, amount]
    x_timestamp=x_ts,        # pandas Series of historical bar timestamps
    y_timestamp=y_ts,        # pandas Series of FUTURE bar timestamps (defines horizon)
    pred_len=24,             # how many bars to forecast
    T=1.0,                   # sampling temperature
    top_p=0.9,
    sample_count=1,          # see note below
)
# -> DataFrame of forecast open/high/low/close/volume/amount indexed by y_timestamp
```

**Inputs:** `open/high/low/close` required; `volume/amount` optional (auto-filled). Timestamps drive temporal features (Kronos extracts minute/hour/weekday/etc. internally). No NaNs allowed.

**CRITICAL gotcha — Monte Carlo:** inside `predict()`, `sample_count>1` is **averaged internally** (returns the mean path, not the distribution). To get a *distribution* of paths for probability calcs, call `predict(..., sample_count=1)` **N times in a loop** and collect each path. This is what the live demo means by "Monte Carlo sampling (N=30 paths)."

**Context limits:** mini=2048 bars, small/base=512. Longer input is silently truncated — keep `lookback ≤ context`.

---

## 4. THE SIGNAL WE COMPUTE (matches the demo)

Given the last **360h** of BTC/USDT 1h bars as context, forecast **24h** (`pred_len=24`), **N=30 paths**:

- **last_close** = most recent actual close
- **upside_probability** = `mean(path.close[-1] > last_close)` across paths → P(higher in 24h)
- **mean_path** = elementwise mean of the 30 close paths (the headline forecast line)
- **p10 / p50 / p90** cone = per-step percentiles across paths (uncertainty band)
- **expected_return_24h** = `(mean_path[-1] / last_close) - 1`
- **realized_vol_hist** = std of last-24h log returns (actual)
- **forecast_vol** = mean across paths of std of forecast log returns
- **volatility_amplification** = `mean(path_forecast_vol > realized_vol_hist)` → P(vol expands)

**Mapping to a confirmation read** (data, not a command):

| upside_prob | Kronos read |
|---|---|
| ≥ 0.65 | bullish confirm |
| 0.55–0.65 | lean bullish |
| 0.45–0.55 | neutral / no edge |
| 0.35–0.45 | lean bearish |
| ≤ 0.35 | bearish confirm |

High **volatility_amplification** (>0.7) = widen stops / size down regardless of direction.

---

## 5. INTEGRATION INTO btc-rings-site (as built)

- **Lives at:** `code/btc-rings-site/kronos/`.
- **Vendored model code:** `code/Kronos/` (cloned from the official repo; `model/` imported via sys.path).
- **Shared core:** `kronos/kronos_lib.py` — data fetch (single + paged), model load (cached singleton), Monte-Carlo path runner, signal math. Used by both the forecaster and the validator.
- **Producer:** `kronos/kronos_forecast.py` — loops the asset universe `ASSETS = [BTC, ETH, SOL, ZEC]`, forecasts each, writes JSON. Runs **locally** (Apple Silicon). *Must NOT run in the sandbox/cron host* — Binance + most price APIs return 403/451 there (see `signal-history.json`). Working source: `https://data-api.binance.vision` (Binance global K-line mirror, not US-geo-blocked); fallback `api.binance.us`.
- **Validator:** `kronos/kronos_validate.py [window_days] [step_h] [n_paths]` — walk-forward backtest of the upside_probability signal vs realized 24h direction. Writes `kronos/kronos_validation.json`. **Run this before sizing on Kronos.** Defaults `30 12 20` (conservative for runtime; widen for rigor).
- **Outputs:**
  - `kronos/kronos_signals.json` — combined, all assets (the dashboard reads this)
  - `kronos/signals/kronos_<ASSET>.json` — per-asset
  - `kronos/kronos_signal.json` — BTC-only (back-compat)
  - `kronos/kronos_history.json` — rolling log (one row/asset/run)
  - `kronos/kronos_validation.json` — backtest scorecard
- **Dashboard:** `kronos.html` — single-file vanilla JS, dark theme, matches the family (`dashboard-pattern` skill). Asset tabs (BTC/ETH/SOL/ZEC), the read + two probability gauges, forecast cone, and the validation scorecard table.
- **Router wiring:** added as a **labeled NON-VOTING fragment** in `SIGNAL-ROUTER-PLAYBOOK.md` and a card in `nav.html`. It does NOT enter the composite score.
- **Hierarchy:** Edge is the call. Kronos joins VIBE/SIGNAL/CYCLES as confirmation. **Never a veto. Pattern wins.**

### Validation metrics (what the scorecard means)
- **hit_rate vs base_rate_up** — directional accuracy vs the naive "always guess the base rate" baseline. Edge = hit_rate − base_rate_up.
- **brier / brier_skill** — Brier score of the probability calls; `brier_skill > 0` means it beats the base-rate guess.
- **high_conf_hit_rate** — accuracy restricted to confident calls (|prob−0.5| ≥ 0.15). This is the number that matters for sizing: does Kronos get the calls *it's sure about* right?
- **Trust gate:** if an asset isn't beating base rate with positive skill, treat that asset's live Kronos read as noise.

---

## 6. REPRODUCE FROM SCRATCH (any host with Python ≥3.10 + torch ≥2.0)

```bash
# 1. Vendor the model code
git clone --depth 1 https://github.com/shiyu-coder/Kronos.git
# 2. Deps (torch already present on Lawrence's M4 Max: 2.5.1 + MPS)
pip install "einops>=0.7" huggingface_hub safetensors pandas numpy tqdm
# 3. Run the forecaster (downloads Kronos-mini + Tokenizer-2k from HF on first run, ~tens of MB)
python3 kronos/kronos_forecast.py            # writes kronos_signal.json
# 4. Serve the dashboard
python3 -m http.server 8099                  # open http://localhost:8099/kronos.html
```

**Hardware:** M4 Max 128GB is wild overkill — mini is 4.1M params, a forecast run is seconds. Could run on a Raspberry Pi.

---

## 7. DONE vs BACKLOG

**Done (2026-06-09):** multi-asset (BTC/ETH/SOL/ZEC) · walk-forward validation harness · multi-asset dashboard · labeled non-voting router fragment.

**Backlog:**
- **Schedule the local producer** — a launchd job on the Mac (hourly/daily) so the dashboard stays fresh without manual runs. Cannot be a cloud cron (price APIs 403 there).
- **More assets / NASDAQ** — extend `ASSETS` in `kronos_lib.py`; for stocks add a Yahoo source (^IXIC etc.). Feed the rotation/cascade dashboards.
- **Bigger validation** — re-run `kronos_validate.py 90 6 30` for a 90-day / 6h-step / 30-path scorecard once you want rigor (longer runtime).
- **Fine-tune** (`finetune/train_predictor.py`, `train_tokenizer.py`, multi-GPU `torchrun`) on Lawrence's asset set / timeframe — needs a GPU box (Nevada is CPU-only; parked dependency).
- **Agent-payable endpoint** — expose the forecast as a 402-gated `/api/forecast` resource via the agent-payments rail (`AGENT_PAYMENTS_ARCHITECTURE.md`).

---

## 8. LIVE TRACKER ON NEVADA (database + cron + dashboard)

Built 2026-06-09. A continuously-running forecast ledger so we measure **real forward performance** + a paper-trading P&L, not just a backtest.

- **Host:** Nevada (`anteth`, Tailscale `100.112.3.85`, **SSH port 50022**, user `ante`). 16 cores / 62 GB / **1.1 TB free**. torch 2.12 CPU. `data-api.binance.vision` returns 200 from there (the data path works — unlike the sandbox/cron host).
- **Dir:** `~/kronos-tracker/` — `Kronos/` (model code), `venv/`, `kronos_lib.py`, `db.py`, `paper.py`, `tracker.py`, `backfill.py`, `query.py`, `web/index.html`, `data/kronos.db`. Source mirrored in repo at `code/btc-rings-site/kronos/tracker/`.
- **Database:** SQLite (`data/kronos.db`). Tables: `forecasts`, `outcomes` (graded once the 24h horizon elapses), `paper_trades` (recomputed), `meta`. Searchable via `query.py` (canned reports + arbitrary SQL) — it's a plain single-file DB.
- **Cron (user crontab on Nevada):** hourly `tracker.py` (forecast 4 assets → grade matured → recompute paper book → export `web/snapshot.json`); `@reboot` restarts the web server.
- **Dashboard:** `http://100.112.3.85:8090/` (Tailscale-only bind) — latest signals, paper P&L ($1k & $100k), equity curves, accuracy/trust-gate table. Auto-refreshes every 5 min.
- **Paper strategy:** LONG when `upside_prob ≥ 0.55`, else CASH (long-only, non-overlapping 24h). Matches a Fidelity account that buys long products and can't short. Benchmarked vs buy-and-hold.
- **Fidelity mapping (signal → tradeable product, NOT automated):** BTC→**IBIT**, SOL→**GSOL**, ZEC→**ZCSH** (Grayscale Zcash Trust). ETH→ETHA (not in Lawrence's active set). The DB emits a signal; Lawrence places the trade in Fidelity.
- **Backfill:** `backfill.py [days] [step_h] [n_paths]` replays history out-of-sample (model only sees data up to each decision point) and records forecast+known-outcome pairs, so the P&L has immediate history. Marked `source='backfill'`.
- **Capital plan:** start $1,000 (live), models $100,000 in parallel (equity is a multiplier — same curve scaled). Only size up after the trust gate (hit_rate > base_rate, positive skill) holds on live + backfilled data.

Operate it:
```bash
ssh anteth                                   # port 50022 via ~/.ssh/config alias
cd ~/kronos-tracker
./venv/bin/python tracker.py                 # manual run (cron does this hourly)
./venv/bin/python query.py pnl               # paper P&L
./venv/bin/python query.py accuracy          # trust gate
./venv/bin/python query.py sql "SELECT ..."  # arbitrary search
```

---

## 9. HONEST CAVEATS

- Foundation-model forecasts are **probabilistic priors, not oracles.** High-noise regime (crypto) = wide cones. The value is the *distribution*, not the mean line.
- Authors' benchmark gains are on their eval sets. **Validate on our own walk-forward** before sizing.
- Zero-shot (no fine-tune) is the default here; fine-tuning could help but needs GPU.
- Binance global API is **US-geo-blocked** (451) — the `data-api.binance.vision` mirror is the working source locally; the cron/sandbox host blocks it entirely, so this signal is **produced on the local Mac**, not in the cloud.
- This is **decision support, not financial advice.** Edge + pattern lead. Kronos confirms.
