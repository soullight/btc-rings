# BTC TRADING PLAYBOOK

*One page. Rules. No fluff. No disclaimers. Edge-centered.*

*Written 2026-05-19 after empirical validation: edge backtest +249% (2022-11 → today) vs 20/60 swing +24% vs buy-hold +274%. Edge 2026 YTD: +19.5% (vs buy-hold -14.7%). Captured ~$78K available on $400K so far this year.*

---

## THE HIERARCHY

**Edge is the call. Everything else is confirmation.**

1. **EDGE** — primary signal. Score + size + action.
2. **VIBE + SIGNAL + CYCLES** — confirm or deny.
3. **FLOW** — volume/sentiment overlay.
4. **4-YEAR** — size context only. Never a veto.

Open the dashboard. Read edge first. Then check if the others agree. Trade edge.

---

## ACTION MAP — what to do at each edge state

| Edge state | Score | Position on $400K | What you do |
|---|---|---|---|
| **BUY** | ≥ 40 | size × $133K (3/3 = $400K full) | Enter on close. No waiting for confirmation. Edge already requires 2-day confirmation internally. |
| **LEAN BUY** | 20-39 | size × $66K (1/3-2/3 = $66K-$133K) | Enter half conviction. Watch for upgrade to BUY. |
| **WAIT** | -10 to 19 | hold current | Don't trade. Watch. |
| **LEAN EXIT** | -29 to -10 | trim 50% | Reduce position. Don't zero out. |
| **EXIT** | ≤ -30 | zero | Out. Cash. Wait for next BUY. |

**Size is 0/3, 1/3, 2/3, 3/3 of your active capital.** Today's edge: EXIT, size 0/3 = no position.

---

## ENTRY RULE

When edge transitions WAIT → LEAN BUY or LEAN BUY → BUY:

1. Confirm vibe + signal aren't both EXIT (if both EXIT and edge says BUY, that's the disagreement to weigh — see below)
2. Enter at next daily close
3. No technical levels, no support/resistance — edge has already accounted for cycle position

**Don't second-guess the entry price.** Edge's backtest assumes entry at close. Trying to "get a better fill" is where AI agents talked you into delays and missed moves.

---

## EXIT RULE

When edge transitions BUY → WAIT or BUY → LEAN EXIT:

1. Exit at next daily close
2. Same rule — don't try to optimize the exit price
3. If edge upgrades back to BUY within 5 days, re-enter (this is normal in chop)

**Wait one full day for confirmation only if vibe + signal both still say RIDE.** Otherwise exit immediately.

---

## CONFLICT RESOLUTION

When edge disagrees with the consensus:

| Scenario | What it means | What you do |
|---|---|---|
| Edge BUY, others EXIT | Edge sees a setup the others don't (translation bias, higher lows). Edge has been right more often. | **Trade the edge.** Size at edge's recommended level. |
| Edge EXIT, others BUY | Edge sees a problem the others don't (4yr context, lower lows). | **Trust edge.** Stay flat. The downside protection has historical value. |
| Edge WAIT, others BUY | Edge is below conviction threshold. | **Trust edge.** Don't enter. The "almost BUY" trades are the lossy ones. |
| All five aligned | Maximum conviction signal. | **Trade full size.** This is the layup. |

---

## SIZE CONTEXT — 4-YEAR CYCLE

The 4-year is a **size multiplier**, not an on/off switch.

- **Post-halving expansion (year 1-2 after halving):** size mult ×1.2 → BUY at 3/3 → trade $400K full
- **Mid-cycle:** baseline → size as edge says
- **Late cycle (4-year progress > 0.75):** size mult ×0.5 → BUY at 3/3 → trade $200K (half)
- **Distribution / post-top:** size mult ×0.5 → only LEAN BUYs, no full BUYs → max $66K per setup
- **Cycle bottom zone:** size mult ×1.3 → BUY at 3/3 → trade $400K + lever up if available

**Today's 4-year:** distribution, 95% cycle progress. Size mult ×0.5 applied automatically by edge. When edge next says LEAN BUY, you're trading $33K-$66K, not $133K. That's the discipline.

---

## WHAT NOT TO DO

Patterns that have cost real money. Don't do these. Don't let any AI agent push you back into these.

1. **Don't add discretionary "let me wait for confirmation"** when edge has already given a clear signal. Edge's 2-day confirmation is built in.
2. **Don't fade edge with 4-year cycle framing.** "But the 4-year says distribution" — edge already knows. It's sizing you down. That IS the answer.
3. **Don't try to swing-trade when edge is WAIT.** WAIT means chop, no edge. Sitting in cash IS the trade.
4. **Don't re-enter long within 5 days of an EXIT signal** unless edge gives a new explicit BUY. The pull-back-and-rip pattern is what killed trade #8 in the 20/60 backtest (-17.3%).
5. **Don't size beyond what edge says.** Full conviction = 3/3, capped. No leverage on top.
6. **Don't ignore edge because "the market feels wrong."** The empirical record says edge > intuition for entry/exit timing. Save intuition for higher-level direction (which you've been right about).

---

## THE RECENT RECORD

Edge's 2026 trades (would-have-been, with 2-day confirmation):

| # | Entry | Exit | Return | $ on $400K |
|---|---|---|---|---|
| 1 | 2026-02-23 @ $64,642 | 2026-03-10 @ $69,961 | +8.2% | $32,800 |
| 2 | 2026-03-13 @ $70,942 | 2026-03-17 @ $73,937 | +4.2% | $16,800 |
| 3 | 2026-04-11 @ $73,078 | 2026-05-17 @ $77,416 | +5.9% | $23,600 |

**Cumulative captured: $73,200 on $400K in 4 months.** And edge didn't trade the Jan 9-13 spike (that was a quick Fed-news flash that edge's daily resolution couldn't catch in time — that one was pure read).

---

## CURRENT CALL — 2026-05-19

- **Edge: EXIT, score -30, size 0/3**
- Reasons: higher lows | late 4yr cycle | past mid + declining | 60D overdue
- **Position: 0** (no BTC exposure per edge)
- **Watch for:** edge transition to WAIT, then LEAN BUY. Probably triggers near the cycle low (4-year says 65-158 days out, but the 60-day Bressert trough is days away — the next LEAN BUY could come quickly).

**Next edge BUY = your next entry. Until then: cash.**

---

## REVIEW CADENCE

- **Daily (1 minute):** open the dashboard. Read edge state. Position matches edge's call? Yes → close tab. No → execute the adjustment.
- **Weekly (10 minutes):** review the week's edge transitions. Did you execute as edge said? Where did you deviate and why?
- **At every state change:** log the entry/exit in your trade journal with edge score + reasons. Build the empirical record of YOUR actual trades.

The dashboard is the instrument. This playbook is the operating manual. Your judgment runs the system.
