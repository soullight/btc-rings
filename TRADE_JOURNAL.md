# BTC TRADE JOURNAL

*The real record. Updated 2026-06-16 from Lawrence's authoritative ledger. All 2026 IBIT trades, executed via Fidelity Traditional IRA 244110939.*

---

## CURRENT POSITION

| Status | Cash | Notes |
|---|---|---|
| **CASH** | ~$399,081 | 100% liquid as of **2026-06-16** — exited the June swing (9,000 IBIT @ $36.03) at market, **+$11,001 (+3.4%)**. Cash derived: $388,080 base + $11,001 swing gain. Dual Momentum V2 gate **CLOSED** (deep bear). No position. Next entry governed by Dual Momentum V2 + Bressert cycle + Lawrence's read. |

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

### Trade 5 — June swing (WIN)

| Field | Value |
|---|---|
| **Period** | Jun 11 → Jun 16, 2026 (5 days) |
| **Signal** | Swing off the Jun 5 cycle trough (BTC ~$59–61K); held the bounce |
| **Entry** | Jun 11 @ $36.03 IBIT (BTC-equiv $63,578) |
| **Size** | 9,000 sh, $324,270 |
| **Exit** | Jun 16 at market — BTC $65,735, IBIT ~$37.25 |
| **Result** | **+$11,001 (+3.4%)** |
| **Cause tag** | `lawrence-read` — self-managed swing off the trough, clean exit back to cash |

---

## 2026 NET P&L

| # | Trade | Date | P&L |
|---|---|---|---|
| 1 | LOCAL_BOTTOM swing | Jan 13–14 | **+$27,000** |
| 2 | Capitulation | Feb 13–23 | **−$29,000** |
| 3 | EXHAUSTION_BUY (stopped) | Mar 18–27 | **≈ −$31,000** |
| 4 | Dual Momentum V2 | Apr 7 → May 19 | **+$17,190** |
| 5 | June swing | Jun 11–16 | **+$11,001** |
| | **TOTAL** | | **≈ −$4,809** |

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


## 2026-07-11 — SOLD 45,000 TRX → 14,894.08 USDT (SunSwap, TRC-20)
- **The setup:** TRX/BTC at the **91.9th percentile** of its 8.5-year history (new ratio board's first signal, day one). Rule executed: feed the stack from what's ratio-RICH. BTC $64K, −21% from 60d high; DM 20/60 = CASH → parked in stable per the system, deploy to BTC on the CASH→BTC flip (Telegram alert armed).
- **Fill:** 45,000 TRX @ ~3.0213 TRX/USDT → 14,894.08 USDT · fee 22.5 TRX (~$7.44) · price impact 0.00% · kept 2,065 TRX (gas + stub).
- **Re-entry thesis (his call, tagged):** TRON = long-term global settlement rail; ACCUMULATE when TRX/BTC swings cheap — 🎯 alert armed at ≤20th percentile.
- **Why it matters:** first rep of the calibration system (stack measured in ₿; sell rich bags, buy BTC on momentum confirm, re-buy theses cheap). Lawrence: "This is what I've wanted all the way along, for literally the last 10 years."

## 2026-07-14 — ETH UNSTAKE: exited 2 of 4 validators (~64 ETH) to rotate to BTC
- Per ETH research verdict (rotate 50-75%, keep tail). Native Prysm validators on elux ([[rf_eth_validators]]). Voluntary-exit broadcast for indices 1998776 + 1998777 (pubkeys 0xb69e… + 0x8b53…); verified active_exiting. KEPT 1998923 + 1165884 (active_ongoing) as the tail.
- Withdrawal address 0x213012cd9446251983d36f5edf1079dba3fc40e8 (= fee recipient, Lawrence confirmed he controls it; already holds 2.33 ETH of accumulated staking rewards). ~64 ETH sweeps there after exit queue (~days). Then → BTC (direct or stable→BTC on DM flip).
- Executed by agent at Lawrence's explicit request ("can't you do this, I shouldn't be doing this") after verifying pubkey↔index, withdrawal address, and healthy status. Ran as eth-user via sudo (elux user lacked keystore read perms).

## 2026-07-31 — ETH UNSTAKE #2: exited the LAST 2 validators — fully out of staking
- Lawrence: *"I'd like to stop validating all together — I feel much better with my eth outside of the node. Doesn't really seem to be a purpose for it, certainly not worth being tied down for 2% interest."* No tail kept; this closes the position opened 2024-01.
- Voluntary-exit broadcast on elux (Prysm v7.1.8, beacon fully synced, sync_distance 0) for **1165884** (`0xaeff3125…04ed68`, "precisely-relevant-dinosaur") + **1998923** (`0xa878f061…5dd684de`, "slightly-gentle-panda"). **Independently verified `active_exiting`** on the public beacon API — exit_epoch **465388**, withdrawable_epoch **465644** (~28h), so the ~64 ETH sweeps within days.
- Destination = the same proven `0x213012cd9446251983d36f5edf1079dba3fc40e8`. Confirmed on-chain BEFORE broadcasting: all four validators carry 0x01 credentials pointing there, and it already holds **66.12 ETH** from the first exit. Landing = the full ~130 ETH liquid.
- Plan unchanged (his 7/14 call): → STABLE on landing → BTC on the DM 20/60 flip, pooled with the ~$14.9K TRX USDT.
- 🐛 **The landing watcher had never run once.** `eth_landing_watch.py` (Nevada, `17 */4 * * *`) was wired 7/14 and looked armed; the first 64 ETH landed with NO ping. Two independent faults: every public RPC returned **403 without a User-Agent**, and the cron redirect wrote to a `logs/` dir that did not exist, so the job died before python started — and a total source failure `exit(0)`d silently, so it looked healthy. Fixed all three (UA header, dir created, loud failure + Telegram alert after 3 blind runs), re-armed at baseline 66.13. Receipts logged.
- Access: `elux` user now has key auth from this Mac + Nevada, and `NOPASSWD` sudo to `eth-user` only (Lawrence pasted both, one time) — no future exit needs him.
- **2026-08-02 status:** both validators now read **`withdrawal_possible`** — the exit itself is finished and nothing more needs signing. 32.001 + 32.010 ETH are still on the beacon chain waiting for the protocol's automatic withdrawal sweep to reach their indices; the address still shows 66.12 ETH. That sweep is a **few days**, not weeks.
