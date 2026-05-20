# BTC TRADE JOURNAL

*Started 2026-05-19. One row per trade. Backfilled with edge signals YTD as the baseline.*

*The point of this journal: build a real record of YOUR trades — and ALSO the trades you declined — so we see what edge is actually capturing, what you're catching, and what costs are accruing from the AI-block patterns.*

---

## ACTIVE POSITION

| Status | Size | Entry date | Entry price | Edge state at entry | Current P&L |
|---|---|---|---|---|---|
| FLAT | 0 | — | — | — | — |

*Update this row when you enter / when you exit. One row only — current position state.*

---

## CLOSED TRADES — 2026

### How to fill in: edge signal → executed?

For each edge signal, log whether you took it. If yes, your actual entry/exit prices. If no, what the trade WOULD have done — so the cost of declining is visible.

| # | Edge signal | Entry date | Entry $ | Exit date | Exit $ | Edge ret % | Your action | Your ret % | $ on $400K |
|---|---|---|---|---|---|---|---|---|---|
| 1 | LEAN BUY → BUY (Feb 23) | 2026-02-23 | $64,642 | 2026-03-10 | $69,961 | +8.2% | DECLINED (AI block) | — | **MISSED $32,800** |
| 2 | LEAN BUY → BUY (Mar 13) | 2026-03-13 | $70,942 | 2026-03-17 | $73,937 | +4.2% | DECLINED (AI block) | — | **MISSED $16,800** |
| 3 | LEAN BUY → BUY (Apr 11) | 2026-04-11 | $73,078 | 2026-05-17 | $77,416 | +5.9% | DECLINED (AI block) | — | **MISSED $23,600** |
| | | | | | | | | **Cumulative missed:** | **$73,200** |

*Edit the "Your action" and "Your ret %" columns once you confirm whether you actually took each trade, the actual fill prices, and your real exit prices. The cumulative-missed row tracks the cost of the AI-blocking pattern.*

---

## OPEN-AIR TRADES — what you called that wasn't edge

Trades where YOUR intuition fired but edge didn't catch it (different timeframe, news event, etc.). Log these separately so we see where your read adds value beyond edge.

| # | Date | Setup | Entry $ | Exit $ | Ret % | $ on $400K | Notes |
|---|---|---|---|---|---|---|---|
| 1 | 2026-01-10 (called) | Bottom call ahead of Jan rally | $90,392 | $96,945 (target) | +7.2% | $29,000 | Edge resolution daily — didn't catch Fed-driven spike. Your read was right. |
| 2 | 2026-02-05 (called) | Spike-low bottom call | $62,812 | $69,791 (target) | +11.1% | $44,400 | Edge said EXIT during the collapse — would have missed re-entry. Your read was right. |

*These are reads that edge structurally can't catch (faster than its daily resolution, or news-driven). Track separately. Build the record of where intuition beats the system.*

---

## NEW TRADE TEMPLATE — copy this row, fill as you go

```
| N | Edge signal (e.g. LEAN BUY @ $X, score Y) | YYYY-MM-DD | $X | YYYY-MM-DD | $X | +/-X.X% | TOOK / DECLINED / PARTIAL | +/-X.X% | $X |
```

**Required entry fields at trade start:**
- Edge state + score + size at entry
- Your actual entry price (not edge's hypothetical)
- Position size in dollars (full / half / quarter)
- Confirmation status: did vibe/signal agree? Disagreement?

**Required exit fields at trade close:**
- Your actual exit price
- Edge state + score at exit (did edge tell you to exit, or did you exit earlier/later?)
- Hold days
- $ P&L on the actual position size
- One-line note: what worked, what didn't, what surprised you

---

## RULES (reference — full playbook at `PLAYBOOK.md`)

1. **When edge says LEAN BUY or BUY → log it, then act.** If you decline, log it as DECLINED in column "Your action" and we track the cost.
2. **When edge says EXIT → log it, exit on close.** No "wait one more day" unless vibe + signal explicitly contradict.
3. **When you take a discretionary trade outside edge → log it in OPEN-AIR TRADES.** Track separately so we see intuition's edge above the system.
4. **Weekly review:** count edge signals fired, count you took, count you declined. Compute $ captured, $ missed. The MISSED column should converge toward 0 — that means you're trusting the system.

---


## AUTO-LOGGED EDGE SIGNALS

*Auto-logged by edge-tracker (Nevada cron). One row per state transition.*

| Date | Transition | Price | Score | Size | Reasons | Took? |
|---|---|---|---|---|---|---|
| 2026-01-24 | EXIT → LEAN EXIT | $89,108 | -10 | 0/3 | 20D cycle just troughed (day 4) · 60D troughs breaking lower · Post-halving expansion window | |
| 2026-01-26 | LEAN EXIT → EXIT | $88,275 | -35 | 0/3 | 60D troughs breaking lower · Post-halving expansion window · 60D past midpoint, price declining from crest | |
| 2026-02-09 | EXIT → LEAN EXIT | $70,109 | -10 | 0/3 | 20D cycle just troughed (day 4) · 60D troughs breaking lower · Post-halving expansion window | |
| 2026-02-11 | LEAN EXIT → EXIT | $67,040 | -35 | 0/3 | 60D troughs breaking lower · Post-halving expansion window · 60D past midpoint, price declining from crest | |
| 2026-02-17 | EXIT → WAIT | $67,478 | +10 | 0/3 | 60D cycle early (day 12 of ~57) · 60D troughs breaking lower · Post-halving expansion window | |
| 2026-02-22 | WAIT → BUY | $67,627 | +45 | 2/3 | 20D cycle just troughed (day 4) · 60D cycle early (day 17 of ~57) · 60D troughs breaking lower | |
| 2026-02-24 | BUY → LEAN BUY | $64,070 | +20 | 1/3 | 60D cycle early (day 19 of ~57) · 60D troughs breaking lower · Post-halving expansion window | |
| 2026-02-26 | LEAN BUY → WAIT | $67,498 | +10 | 0/3 | 60D cycle early (day 21 of ~57) · 60D troughs breaking lower · Post-halving expansion window | |
| 2026-02-28 | WAIT → BUY | $66,985 | +45 | 2/3 | 20D cycle just troughed (day 4) · 60D cycle early (day 23 of ~57) · 60D troughs breaking lower | |
| 2026-03-02 | BUY → LEAN BUY | $68,832 | +20 | 1/3 | 60D cycle early (day 25 of ~57) · 60D troughs breaking lower · Post-halving expansion window | |
| 2026-03-03 | LEAN BUY → WAIT | $68,338 | +10 | 0/3 | 60D cycle mid-phase · 60D troughs breaking lower · Post-halving expansion window | |
| 2026-03-09 | WAIT → LEAN EXIT | $68,439 | -20 | 0/3 | 60D cycle mid-phase · 60D troughs breaking lower · Post-halving expansion window | |
| 2026-03-12 | LEAN EXIT → LEAN BUY | $70,528 | +25 | 1/3 | 20D cycle just troughed (day 4) · 60D troughs breaking lower · Post-halving expansion window | |
| 2026-03-14 | LEAN BUY → WAIT | $71,224 | +0 | 0/3 | 60D troughs breaking lower · Post-halving expansion window | |
| 2026-03-16 | WAIT → LEAN EXIT | $74,885 | -10 | 0/3 | 60D troughs breaking lower · Post-halving expansion window · 20D cycle in topping zone (day 8) | |
| 2026-03-18 | LEAN EXIT → EXIT | $71,249 | -30 | 0/3 | 60D troughs breaking lower · Post-halving expansion window · 60D past midpoint, price declining from crest | |
| 2026-03-25 | EXIT → LEAN EXIT | $71,305 | -20 | 0/3 | 60D troughs breaking lower · Post-halving expansion window · 60D past midpoint, price declining from crest | |
| 2026-03-26 | LEAN EXIT → WAIT | $68,782 | +5 | 0/3 | 20D cycle just troughed (day 4) · 60D troughs breaking lower · Post-halving expansion window | |
| 2026-03-28 | WAIT → LEAN EXIT | $66,327 | -20 | 0/3 | 60D troughs breaking lower · Post-halving expansion window · 60D past midpoint, price declining from crest | |
| 2026-03-29 | LEAN EXIT → EXIT | $65,968 | -35 | 0/3 | 60D troughs breaking lower · Post-halving expansion window · 60D past midpoint, price declining from crest | |
| 2026-04-02 | EXIT → LEAN EXIT | $66,895 | -10 | 0/3 | 20D cycle just troughed (day 4) · 60D troughs breaking lower · Post-halving expansion window | |
| 2026-04-04 | LEAN EXIT → EXIT | $67,291 | -35 | 0/3 | 60D troughs breaking lower · Post-halving expansion window · 60D past midpoint, price declining from crest | |
| 2026-04-10 | EXIT → LEAN BUY | $72,990 | +35 | 1/3 | 60D cycle early (day 12 of ~53) · 60D troughs making higher lows · Post-halving expansion window | |
| 2026-04-15 | LEAN BUY → BUY | $74,831 | +45 | 3/3 | 60D cycle early (day 17 of ~53) · 60D troughs making higher lows · Post-halving expansion window | |
| 2026-04-20 | BUY → WAIT | $75,865 | +15 | 0/3 | 60D cycle early (day 22 of ~53) · 60D troughs making higher lows · Late 4-year cycle | |
| 2026-05-03 | WAIT → LEAN BUY | $78,557 | +30 | 1/3 | 20D cycle just troughed (day 4) · 60D troughs making higher lows · Late 4-year cycle | |
| 2026-05-05 | LEAN BUY → WAIT | $80,907 | +5 | 0/3 | 60D troughs making higher lows · Late 4-year cycle | |
| 2026-05-13 | WAIT → LEAN EXIT | $79,291 | -25 | 0/3 | 60D troughs making higher lows · Late 4-year cycle · 60D past midpoint, price declining from crest | |
| 2026-05-14 | LEAN EXIT → WAIT | $81,079 | -5 | 0/3 | 60D troughs making higher lows · Late 4-year cycle · 20D cycle in topping zone (day 15) | |
| 2026-05-15 | WAIT → LEAN EXIT | $79,065 | -25 | 0/3 | 60D troughs making higher lows · Late 4-year cycle · 60D past midpoint, price declining from crest | |
| 2026-05-16 | LEAN EXIT → EXIT | $78,115 | -30 | 0/3 | 60D troughs making higher lows · Late 4-year cycle · 60D past midpoint, price declining from crest | |

---
## REVIEW LOG — append rows weekly

| Week ending | Edge signals fired | Taken | Declined | $ captured | $ missed | Notes |
|---|---|---|---|---|---|---|
| 2026-05-19 | 3 (Feb, Mar, Apr) | 0 | 3 | $0 | $73,200 | Baseline — pre-playbook. AI-block pattern. Reset starts now. |

*Add a new row each Sunday. The trend you want: $missed → 0, $captured → 6-figure annual.*
