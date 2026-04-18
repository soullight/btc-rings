# Bitcoin Rings v2 Validation Notes

This document defines **robustness checks** for the DEPLOY / RIDE / EXIT engine without turning it into an optimization system.

## Core principles
- Validate **state quality**, not prediction probabilities.
- Keep outputs interpretable.
- Penalize high-frequency state flips.

## Checks
0. **Cycle significance guard**
   - Validate the best autocorrelation in the 35-90d search band.
   - If correlation is weak, force 60-day fallback instead of adaptive shortening.
1. **State persistence**
   - Median run length for each action state over history.
   - Flag if median run length < 3 days.
2. **Conflict rate**
   - Rate of timing/flow contradiction events.
   - Target lower contradiction after regime gating.
3. **Adverse excursion after DEPLOY**
   - Track worst drawdown within 5 and 10 days after DEPLOY.
4. **Exit lag**
   - Days between local crest and first EXIT state.
5. **Data degradation behavior**
   - Ensure missing Fear & Greed or volume does not silently produce strong calls.

## Why these checks
These checks preserve the operator philosophy (fast action labels) while improving stability and reducing false urgency during shock or chop regimes.
