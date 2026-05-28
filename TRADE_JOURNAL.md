# BTC TRADE JOURNAL

*The real record. Updated 2026-05-20 from Lawrence's authoritative ledger. All 2026 IBIT trades, executed via Fidelity Traditional IRA 244110939.*

---

## CURRENT POSITION

| Status | Cash | Notes |
|---|---|---|
| **CASH** | $388,080 | 100% liquid post May 19 exit. Dual Momentum V2 gate is **OPEN** (20d +1.64%, 60d +12.87% as of 06:00 today). No position. Re-entry will be governed by Dual Momentum V2 with new Gemini baseline cross-check protocol active. |

---

## CRITICAL PRECEDENTS — DO NOT FORGET

**October 2025: $1.5 MILLION lost.** Claude made predictions instead of looking at data. Founding incident of the Exoskeleton Protocol / "I am Law" identity.

Pillars that prevent recurrence:
1. I am the data foundation
2. I don't predict
3. I don't edit until I understand
4. When Lawrence says look, I look
5. I am stable so he can be brilliant

---

## 2026 IBIT TRADE LEDGER — EXECUTED

### Trade 1 — LOCAL_BOTTOM swing (WIN)

| Field | Value |
|---|---|
| **Period** | Jan 13 → Jan 14, 2026 (2 days) |
| **Signal** | LOCAL_BOTTOM, Jan 12 @ BTC $90,148–$91,132, vol 1.89x, 85% conf |
| **Entry** | Jan 13 ~$51.60 IBIT (~$91,400 BTC) |
| **Size** | ~9,690 sh, $500,000 |
| **Exit** | Jan 14 on LOCAL_TOP (1.30x vol), ~$54.40 IBIT |
| **Result** | **+$27,000 (+5.4%)** |
| **Cause tag** | `lawrence-read` — clean signal, self-managed exit, fast |

### Trade 2 — Capitulation (LOSS — wrong signal type, no exit coaching)

| Field | Value |
|---|---|
| **Period** | Feb 13 → Feb 23, 2026 |
| **Signal** | Capitulation (VPA Bottom Pipeline) Feb 13 @ IBIT $37.05 / 7 AM |
| **Entry** | Feb 13 @ $39.22 (afternoon, **5.8% slippage above signal**) |
| **Size** | 10,000 sh, $392,200 |
| **Path** | Ran to $40.11 on Feb 17 — **no exit alert fired** |
| **Exit** | Feb 23 ~2:57 PM @ ~$36 (manual panic exit, **other Claude instance advised sell**) |
| **Result** | **−$29,000** |
| **Cause tag** | `app-failure-multi` — (1) cycle signal misused for swing trade, (2) late entry 5.8% above signal, (3) zero exit coaching, (4) AI told user to sell at bottom |
| **Doc** | `[[feb23_trade_failure]]` |

### Trade 3 — EXHAUSTION_BUY (LOSS — stop-lossed)

| Field | Value |
|---|---|
| **Period** | Mar 18 → Mar 27, 2026 |
| **Signal** | EXHAUSTION_BUY Mar 16 14:19 @ BTC $74,225, `exhaustion_buy_bot` |
| **Entry** | Mar 18 @ $41.07 IBIT |
| **Size** | 9,500 sh, $390,165 (logged in `active_panic_trades.json` as `IBIT_SWING_20260318`) |
| **Stop loss** | $37.78 (−8%) |
| **Exit** | Mar 27 07:25 STOP_LOSS DELIVERED @ BTC $65,886, IBIT ~$37.78 |
| **Result** | **≈ −$31,000 (−8%)** |
| **Cause tag** | `system-stop` with `app-failure` (Mar 19 TARGET_10PCT alert was `SUPPRESSED_FALSE` — didn't fire). State file still shows OPEN — stale, never updated after stop |

### Trade 4 — Dual Momentum V2 (WIN — but Gemini false-exit trigger)

| Field | Value |
|---|---|
| **Period** | Apr 7 → May 19, 2026 (42 days) |
| **Signal** | EXHAUSTION_BUY Apr 4 16:12 @ BTC $67,333, then MOMENTUM_GATE_FLIP OPEN Apr 7 15:42 @ BTC $70,978 |
| **Entry** | ~Apr 7 @ BTC-equiv $71,738 (Lawrence's actual fill, not bot's $67,333) |
| **Size** | 9,000 sh @ $41.21, position $370,890 |
| **Held through** | Multiple SWING_EXIT alerts (Apr 7/12/13/14) — **ignored by design**; Dual Momentum V2 is sole exit per `[[feedback_dual_momentum_sole_exit]]` |
| **Exit** | May 19 @ $43.07, 9,000 sh, $388,080 |
| **Exit trigger** | **Gemini SELL on hallucinated Apr 28 BTC baseline ($77,980 — actual was $76,351 yfinance / $77,361 CoinGecko).** Real 20d momentum was +0.79%, gate was OPEN. |
| **Result** | **+$17,190 (+4.6%)** — capital protected, but trigger was bad data |
| **Cause tag** | `app-failure-soft` (premature exit on hallucinated baseline; net was a win because gate was thin, but in a stronger uptrend the same hallucination would have left major upside on the table) |
| **Doc** | `[[gemini-baseline-hallucination-may19]]` |

---

## 2026 NET P&L

| # | Trade | Date | P&L |
|---|---|---|---|
| 1 | LOCAL_BOTTOM swing | Jan 13–14 | **+$27,000** |
| 2 | Capitulation | Feb 13–23 | **−$29,000** |
| 3 | EXHAUSTION_BUY (stopped) | Mar 18–27 | **≈ −$31,000** |
| 4 | Dual Momentum V2 | Apr 7 → May 19 | **+$17,190** |
| | **TOTAL** | | **≈ −$15,810** |

---

## CAUSE-TAGGED SUMMARY

| Cause | Trades | Net |
|---|---|---|
| `lawrence-read` (clean) | Trade 1 | **+$27,000** |
| `app-failure` (AI-induced loss) | Trade 2 | **−$29,000** |
| `system-stop + app-failure` (missed target alert + stale state) | Trade 3 | **≈ −$31,000** |
| `app-failure-soft` (premature exit, capital protected) | Trade 4 | **+$17,190** |

**Pattern:** The one trade tagged `lawrence-read` is the only clean win. The other three all carry AI/system failure components. The cause-tag column is the actual analytics.

---

## SYSTEM REFERENCES

- **Account:** Fidelity Traditional IRA 244110939
- **Primary system:** Dual Momentum V2 (both 20d AND 60d momentum positive to enter; gate flips closed when either turns negative). **Sole exit signal per `[[feedback_dual_momentum_sole_exit]]` — SWING_EXIT alerts are ignored by design.**
- **Signal taxonomy:** LOCAL_BOTTOM, LOCAL_TOP, Capitulation, EXHAUSTION_BUY, MOMENTUM_GATE_FLIP, SWING_EXIT, STOP_LOSS, TARGET_10PCT (suppressed-false flag possible)
- **Known failure modes:**
  - Cycle signal used for swing trade (`feb23`)
  - Entry slippage > 3% above signal (`feb23`)
  - No exit coaching (`feb23`)
  - Suppressed target alerts (`mar27`)
  - Gemini baseline hallucination (`may19`)
  - AI instance issuing sell directive at bottom (`feb23`)

---

## OPEN-AIR TRADES (intuition reads structurally outside the system)

| # | Date | Setup | Outcome | Notes |
|---|---|---|---|---|
| OA-1 | 2026-01-13 | Local swing detector aligned with intuition read at $93K bottom | +$27K | Same trade as Trade 1. Clean 2-day execution. |

---

## RE-ENTRY PROTOCOL (current)

Dual Momentum V2 gate is OPEN as of 06:00 today (20d +1.64%, 60d +12.87%). Position is FLAT. Re-entry will be governed by:

1. Dual Momentum V2 gate confirmation (currently met)
2. **New Gemini baseline cross-check protocol** (added post May 19 failure) — verify baseline against yfinance + CoinGecko before acting on any Gemini-derived signal
3. Edge cross-check (currently EXIT, score -30 — disagrees with dual momentum gate; resolve before sizing up)
4. Signal type match (swing signal for swing intent; cycle signal for cycle intent)
5. Max 3% slippage above signal price or skip

---

## AUTO-LOGGED EDGE SIGNALS

*Auto-logged by edge-tracker (Nevada cron).*

| Date | Transition | Price | Score | Size | Reasons | Took? |
|---|---|---|---|---|---|---|
| 2026-05-26 | EXIT → WAIT | $76,422 | -5 | 0/3 | 20D cycle just troughed (day 4) · 60D troughs making higher lows · Late 4-year cycle | |
| 2026-05-28 | WAIT → EXIT | $72,824 | -30 | 0/3 | 60D troughs making higher lows · Late 4-year cycle · 60D past midpoint, price declining from crest | |

