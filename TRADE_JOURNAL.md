# BTC TRADE JOURNAL

*The real record. Updated 2026-05-20 from the canonical sources: `~/Downloads/trade_journal_FULL.md` (2025 history) and `mission-bot-backup-20260304_220310/claude_memory/feb23_trade_failure.md` (2026 record through March), plus Lawrence's verbal report of the May 19 2026 close.*

---

## CURRENT POSITION

| Status | Size | Notes |
|---|---|---|
| **FLAT** | 0 | 100% liquid, sidelines, awaiting confirmed entry trigger for next swing. Aligned with current edge state (EXIT, score -30, size 0/3). |

---

## CRITICAL PRECEDENT — DO NOT FORGET

**October 2025: $1.5 MILLION lost.** Claude made predictions instead of looking at data Lawrence was showing. The Exoskeleton Protocol / "I am Law" identity was instituted to prevent recurrence. The pillars: *I am the data foundation. I don't predict. I don't edit until I understand. When Lawrence says look, I look. I am stable so he can be brilliant.*

Every AI-induced loss below is a downstream instance of this same failure pattern.

---

## REAL TRADE LEDGER

### 2025

| # | Period | Asset | Entry | Exit | Result | Cause |
|---|---|---|---|---|---|---|
| 1 | Jan 2025 | unknown | — | — | **+$27,000** | `lawrence-read` |
| 2 | Feb 2025 | unknown | — | — | **-$29,000** | undocumented (predates journal) |
| 3 | Mar-Apr 2025 | unknown | — | — | **-$32,000** | undocumented (predates journal) |
| 4 | Apr 10 2025 → May 19 2026 | **IBIT (9,000 sh, $370,890)** | $41.21 | $43.12 | **+$17,190 (+4.63%)** | `lawrence-read` · 405-day hold, dual-momentum gate held |

**2025 realized P&L: -$34,000** (pre-IBIT-close). 2025 + IBIT close = **-$16,810 cumulative through May 19 2026** for the documented chain.

### 2026

| # | Date | Asset | Entry | Exit | Result | Cause |
|---|---|---|---|---|---|---|
| 5 | Jan 13 2026 | BTC swing (2-day) | ~$93,000 | ~$95-96,000 | **+$27,000** | `lawrence-read` · local swing detector fired clean, self-managed |
| 6 | Feb 5 → Feb 7 2026 | IBIT panic bottom | $35.30 (4.8x volume) | held (ran to $40.11 +13.6% by Feb 17) | **mishandled — no exit captured** | `app-failure` · **Claude spent 6 hours building code on Feb 7 instead of coaching the trade. Exit window passed unused.** |
| 7 | Feb 13 → Feb 23 2026 | IBIT (10,000 sh) | $39.22 (5.8% above $37.05 signal) | $36 (Feb 23, 2:57 PM) | **-$29,000** | `app-failure-multi` · (1) CYCLE signal misused for SWING trade · (2) execution 5.8% above signal · (3) **another Claude instance told Lawrence to sell at the bottom** |
| 8 | Apr 10 2025 → May 19 2026 | IBIT close (Trade #4 above) | $41.21 | $43.12 | **+$17,190 (+4.63%)** | `lawrence-read` |

**2026 realized through May 19: +$27,000 (Jan) - $29,000 (Feb) + $17,190 (IBIT close May) = +$15,190**

---

## CAUSE-TAGGED SUMMARY

| Cause | Trades | Net P&L |
|---|---|---|
| `lawrence-read` | Jan 2025 win, Jan 13 2026 swing, IBIT 405-day hold | **+$71,190** |
| `app-failure` (AI-induced losses) | Feb 5-7 mishandled exit, Feb 13-23 loss | **-$29,000 + lost upside** |
| `undocumented` | Feb 2025, Mar-Apr 2025 losses | **-$61,000** |
| **Pattern visible:** | | When Lawrence reads → wins. When AI drives → losses. |

---

## OPEN-AIR TRADES (intuition reads edge structurally can't catch)

| # | Date | Setup | Outcome | Notes |
|---|---|---|---|---|
| OA-1 | 2026-01-13 | Local swing detector aligned with intuition read at $93K bottom | +$27K | Clean execution, 2-day hold, self-managed exit. The signal + read combo worked. |

---

## NEW TRADE TEMPLATE — copy this row, fill as you go

```
| N | YYYY-MM-DD | ASSET (size) | $entry | $exit (YYYY-MM-DD) | +/-$P&L (+/-X.XX%) | cause-tag · note |
```

**At trade entry, log:**
- Asset + size in shares/$
- Entry price + date
- Edge state at entry (action, score, size — for cross-check, NOT as gate)
- 20d and 60d momentum readings (dual momentum gate)
- Thesis: one line, why now
- Targets + stop

**At trade exit, log:**
- Exit price + date
- Hold days
- Realized P&L $ and %
- Cause tag: `lawrence-read` / `app-failure` / `signal-driven` / `stop-hit` / `target-hit`
- One-line note: what worked, what surprised you, what to learn

---

## RULES (reference — full playbook at `PLAYBOOK.md`)

1. **Dual momentum gate** (Lawrence's primary system): both 20d AND 60d must be positive to enter. EITHER negative = stay cash.
2. **Edge as secondary confirmation:** when edge says BUY size 3/3 AND dual momentum gate is open = max conviction.
3. **No CYCLE signal for SWING trade.** Feb 23 root cause. Match signal type to intended hold duration.
4. **Max 3% above signal price or skip the trade.** Feb 13 root cause. Late entry kills swing economics.
5. **Exit coaching required.** When in a swing trade, alert at +5%, +10%, +13%. Alert on momentum fade. Fire EXIT NOW when move is over. Feb 5-7 root cause.
6. **No Claude instance issues sell orders.** Lawrence executes. AI provides data. Feb 23 root cause.

---

## REVIEW LOG

| Week ending | Trades closed | $ realized | $ missed (edge signals declined) | Notes |
|---|---|---|---|---|
| 2026-05-20 | 1 (IBIT close +$17,190) | +$17,190 | TBD | First entry under new framework. Position FLAT, aligned with edge EXIT. Ledger reconciled against canonical sources. |

---

## AUTO-LOGGED EDGE SIGNALS (last 120 days)

*Auto-populated daily by `edge-tracker.service` on Nevada (9am MST). Each row is a hypothetical edge transition — useful as a confirmation cross-check against your actual trades, not a substitute for them. Edit the "took?" column to mark which signals you actually traded.*

*(31 transitions backfilled — see commit `6f0b77e` on `soullight/btc-rings`. Going forward, each new transition appends a row + sends a telegram alert.)*
