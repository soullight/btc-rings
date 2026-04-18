(function (global) {
  "use strict";

  const DAY_MS = 24 * 60 * 60 * 1000;

  function mean(arr) {
    if (!arr || !arr.length) return 0;
    return arr.reduce((a, b) => a + b, 0) / arr.length;
  }

  function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
  }

  function pctChange(a, b) {
    if (!Number.isFinite(a) || !Number.isFinite(b) || a === 0) return 0;
    return (b - a) / a;
  }

  function rollingMedian(values, window) {
    const out = [];
    for (let i = 0; i < values.length; i++) {
      const start = Math.max(0, i - Math.floor(window / 2));
      const end = Math.min(values.length, i + Math.ceil(window / 2));
      const slice = values.slice(start, end).sort((a, b) => a - b);
      out.push(slice[Math.floor(slice.length / 2)]);
    }
    return out;
  }

  function quantile(sortedValues, q) {
    if (!sortedValues.length) return 0;
    const idx = (sortedValues.length - 1) * q;
    const lo = Math.floor(idx);
    const hi = Math.ceil(idx);
    if (lo === hi) return sortedValues[lo];
    return sortedValues[lo] + (sortedValues[hi] - sortedValues[lo]) * (idx - lo);
  }

  function calcAtrPercent(closes, period) {
    if (closes.length < period + 1) return 0.02;
    const trs = [];
    for (let i = 1; i < closes.length; i++) {
      trs.push(Math.abs(closes[i] - closes[i - 1]) / closes[i - 1]);
    }
    return mean(trs.slice(-period));
  }

  function autocorr(values, lag) {
    const n = values.length;
    if (n <= lag + 2) return -1;
    const x = values.slice(0, n - lag);
    const y = values.slice(lag);
    const mx = mean(x);
    const my = mean(y);
    let num = 0;
    let dx = 0;
    let dy = 0;
    for (let i = 0; i < x.length; i++) {
      const vx = x[i] - mx;
      const vy = y[i] - my;
      num += vx * vy;
      dx += vx * vx;
      dy += vy * vy;
    }
    if (dx === 0 || dy === 0) return -1;
    return num / Math.sqrt(dx * dy);
  }

  function estimateDominantCycle(closes, minLag = 35, maxLag = 90) {
    if (closes.length < maxLag + 20) return 60;

    // Detrend with log returns so trend persistence does not masquerade as a cycle.
    const returns = [];
    for (let i = 1; i < closes.length; i++) {
      const prev = closes[i - 1];
      const next = closes[i];
      returns.push(prev > 0 && next > 0 ? Math.log(next / prev) : 0);
    }
    const smooth = rollingMedian(returns, 5);
    let bestLag = 60;
    let bestCorr = -Infinity;
    for (let lag = minLag; lag <= maxLag; lag++) {
      const c = autocorr(smooth, lag);
      if (c > bestCorr) {
        bestCorr = c;
        bestLag = lag;
      }
    }
    // If no meaningful periodicity appears, preserve the operator's 60d anchor.
    if (bestCorr < 0.35) return 60;
    return clamp(bestLag, 45, 75);
  }

  function dynamicWindow(closes) {
    const atrPct = calcAtrPercent(closes, 20);
    const w = Math.round(6 + atrPct * 180);
    return clamp(w, 6, 18);
  }

  function findTroughsAdaptive(closes, nominalCycle) {
    const smooth = rollingMedian(closes, 5);
    const halfWindow = dynamicWindow(closes);
    const minGap = Math.max(14, Math.round(nominalCycle * 0.6));
    const troughs = [];

    for (let i = halfWindow; i < smooth.length - halfWindow; i++) {
      let isMin = true;
      for (let j = 1; j <= halfWindow; j++) {
        if (smooth[i] > smooth[i - j] || smooth[i] > smooth[i + j]) {
          isMin = false;
          break;
        }
      }
      if (!isMin) continue;

      const reboundWindow = smooth.slice(i + 1, Math.min(smooth.length, i + 6));
      const rebound = reboundWindow.length ? (Math.max(...reboundWindow) - smooth[i]) / smooth[i] : 0;
      if (rebound < 0.015) continue;

      if (!troughs.length || i - troughs[troughs.length - 1] >= minGap) {
        troughs.push(i);
      } else {
        const last = troughs[troughs.length - 1];
        if (smooth[i] < smooth[last]) troughs[troughs.length - 1] = i;
      }
    }

    return { troughs, halfWindow };
  }

  function classifyVolume(volumes) {
    if (volumes.length < 70) return { band: "normal", ratio20: 1, ratio60: 1, trend: 1 };
    const recent5 = mean(volumes.slice(-5));
    const prev5 = mean(volumes.slice(-10, -5));
    const avg20 = mean(volumes.slice(-20));
    const avg60 = mean(volumes.slice(-60));
    const ratio20 = avg20 ? recent5 / avg20 : 1;
    const ratio60 = avg60 ? recent5 / avg60 : 1;
    const trend = prev5 ? recent5 / prev5 : 1;

    const ratios = [];
    for (let i = 60; i < volumes.length; i++) {
      const local5 = mean(volumes.slice(i - 4, i + 1));
      const local60 = mean(volumes.slice(i - 59, i + 1));
      ratios.push(local60 ? local5 / local60 : 1);
    }
    const sorted = ratios.slice().sort((a, b) => a - b);
    const q30 = quantile(sorted, 0.30);
    const q70 = quantile(sorted, 0.70);
    const q90 = quantile(sorted, 0.90);

    let band = "normal";
    if (ratio60 >= q90) band = "massive";
    else if (ratio60 >= q70) band = "high";
    else if (ratio60 < q30) band = "thin";

    return { band, ratio20, ratio60, trend, thresholds: { q30, q70, q90 } };
  }

  function classifyFearGreed(value) {
    if (value <= 15) return "extreme_fear";
    if (value <= 30) return "fear";
    if (value <= 45) return "moderate_fear";
    if (value <= 55) return "neutral";
    if (value <= 70) return "moderate_greed";
    if (value <= 85) return "greed";
    return "extreme_greed";
  }

  function inferFlowState(fgValue, volumeBand) {
    const z = classifyFearGreed(fgValue);
    if (z === "extreme_fear") return volumeBand === "massive" || volumeBand === "high" ? "CAPITULATION" : "ACCUMULATION";
    if (z === "fear" || z === "moderate_fear") return volumeBand === "massive" || volumeBand === "high" ? "ABSORPTION" : "ACCUMULATION";
    if (z === "neutral") return "MOMENTUM";
    if (z === "moderate_greed") return volumeBand === "thin" ? "EXHAUSTION" : "MOMENTUM";
    if (z === "greed") return volumeBand === "thin" ? "EXHAUSTION" : "DISTRIBUTION";
    return volumeBand === "massive" ? "DISTRIBUTION" : "EXHAUSTION";
  }

  function detectRegime(closes) {
    if (closes.length < 70) return "range";
    const c = closes[closes.length - 1];
    const c20 = closes[closes.length - 20];
    const c60 = closes[closes.length - 60];
    const m20 = pctChange(c20, c);
    const m60 = pctChange(c60, c);

    const daily = [];
    for (let i = closes.length - 20; i < closes.length; i++) {
      if (i <= 0) continue;
      daily.push(Math.abs(pctChange(closes[i - 1], closes[i])));
    }
    const rv = mean(daily);

    if (daily.length && Math.max(...daily) > 0.08) return "shock";
    if (m20 > 0.03 && m60 > 0.05) return "trend_up";
    if (m20 < -0.03 && m60 < -0.05) return "trend_down";
    if (rv < 0.015) return "range";
    return "mixed";
  }

  function decide({ timing, flow, regime }) {
    let action = "RIDE";
    const notes = [];

    if (timing.phase === "early" && ["CAPITULATION", "ABSORPTION"].includes(flow.state)) {
      action = "DEPLOY";
      notes.push("timing+conviction alignment");
    } else if (timing.phase === "late" && ["DISTRIBUTION", "EXHAUSTION"].includes(flow.state)) {
      action = "EXIT";
      notes.push("late cycle with distribution");
    } else if (timing.phase === "early") {
      action = "DEPLOY";
      notes.push("early cycle bias");
    } else if (timing.phase === "late") {
      action = "EXIT";
      notes.push("late cycle bias");
    }

    if (regime === "shock" && action === "DEPLOY") {
      action = "RIDE";
      notes.push("shock lockout");
    }
    if (regime === "trend_down" && action === "DEPLOY" && flow.state === "ACCUMULATION") {
      action = "RIDE";
      notes.push("downtrend caution");
    }

    return { action, notes };
  }

  async function fetchJson(url) {
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }

  async function fetchBtcDaily() {
    const errors = [];

    try {
      const cg = await fetchJson("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=730&interval=daily");
      const rows = cg.prices.map((p, i) => ({
        ts: p[0],
        close: p[1],
        volume: cg.total_volumes?.[i]?.[1] ?? 0
      }));
      return { source: "CoinGecko", rows };
    } catch (e) {
      errors.push(`CoinGecko: ${e.message}`);
    }

    try {
      const cc = await fetchJson("https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=730");
      const rows = cc.Data.Data.map((d) => ({
        ts: d.time * 1000,
        close: d.close,
        volume: d.volumeto
      }));
      return { source: "CryptoCompare", rows };
    } catch (e) {
      errors.push(`CryptoCompare: ${e.message}`);
    }

    throw new Error(errors.join(" | "));
  }

  async function fetchFearGreed() {
    const data = await fetchJson("https://api.alternative.me/fng/?limit=365&format=json");
    const rows = data.data
      .map((d) => ({ ts: Number(d.timestamp) * 1000, value: Number(d.value) }))
      .sort((a, b) => a.ts - b.ts);
    return rows;
  }

  function joinLatestFg(priceRows, fgRows) {
    const latestTs = priceRows[priceRows.length - 1].ts;
    let best = fgRows[fgRows.length - 1];
    for (const row of fgRows) {
      if (row.ts <= latestTs + DAY_MS) best = row;
    }
    return best;
  }

  async function runSuite() {
    const [pricePack, fgRows] = await Promise.all([fetchBtcDaily(), fetchFearGreed()]);
    const closes = pricePack.rows.map((r) => r.close);
    const vols = pricePack.rows.map((r) => r.volume);

    const cycleLen = estimateDominantCycle(closes);
    const trough = findTroughsAdaptive(closes, cycleLen);
    const tIdx = trough.troughs[trough.troughs.length - 1] ?? closes.length - cycleLen;
    const progress = clamp((closes.length - 1 - tIdx) / cycleLen, 0, 1.6);
    const phase = progress < 0.35 ? "early" : progress > 0.80 ? "late" : "mid";

    const volume = classifyVolume(vols);
    const fg = joinLatestFg(pricePack.rows, fgRows);
    const flowState = inferFlowState(fg.value, volume.band);
    const regime = detectRegime(closes);

    const timing = { cycleLen, progress, phase, troughIndex: tIdx, window: trough.halfWindow };
    const flow = { state: flowState, fgValue: fg.value, volumeBand: volume.band, volume };
    const decision = decide({ timing, flow, regime });

    return {
      source: pricePack.source,
      price: closes[closes.length - 1],
      timing,
      flow,
      regime,
      decision,
      generatedAt: new Date().toISOString()
    };
  }

  global.BrainTransferEngine = {
    runSuite,
    _internals: {
      estimateDominantCycle,
      findTroughsAdaptive,
      classifyVolume,
      inferFlowState,
      detectRegime,
      decide
    }
  };
})(window);
