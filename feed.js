/* feed.js — the source chain that actually works, in one place.
 *
 * Written 2026-08-10 after an audit found 8 of 39 pages blank or broken. Every failure traced
 * to the same three dead sources, and each page had its own copy of the fetch chain, so one
 * API change broke eight pages independently.
 *
 * DEAD, do not reach for these:
 *   api.binance.com / fapi.binance.com  451 — geo-blocked from every machine here, AND from the
 *                                            CORS proxies (allorigins relays, Binance blocks the
 *                                            proxy's IP). Proxying cannot fix a geo-block.
 *   min-api.cryptocompare.com           401 — now key-gated.
 *   api.coingecko.com .../market_chart?days=max
 *                                       401 — deep history moved behind a key; the short windows
 *                                            still work but 429 under any real load.
 *
 * ALIVE, free, no key, CORS open:
 *   www.bitstamp.net           full daily OHLCV back to 2011-08-18, paginated 1000/call
 *   api.exchange.coinbase.com  300 candles/call, many products, live ticker
 *   api.kraken.com             live ticker; daily OHLC capped at 721 candles
 *
 * Every function returns null on total failure rather than throwing, so a caller can render
 * "no feed" instead of dying silently — which is how all 8 broken pages failed.
 */
(function (g) {
  'use strict';

  function iso(ms) { return new Date(ms).toISOString().slice(0, 10); }

  async function jget(url, ms) {
    const c = new AbortController(), k = setTimeout(() => c.abort(), ms || 15000);
    try {
      const r = await fetch(url, { signal: c.signal });
      clearTimeout(k);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return await r.json();
    } catch (e) { clearTimeout(k); throw e; }
  }

  /* Full daily OHLCV. Returns [{date,open,high,low,close,volume}] oldest-first, or null. */
  async function daily(days) {
    days = days || 4000;
    try {                                   // Bitstamp — the only free full history
      const m = {}; let end = Math.floor(Date.now() / 1000);
      for (let i = 0; i < 8 && Object.keys(m).length < days; i++) {
        const j = await jget('https://www.bitstamp.net/api/v2/ohlc/btcusd/?step=86400&limit=1000&end=' + end, 20000);
        const o = j && j.data && j.data.ohlc; if (!o || !o.length) break;
        let oldest = end;
        for (const r of o) {
          const ts = +r.timestamp;
          if (+r.close > 0) m[iso(ts * 1000)] = { date: iso(ts * 1000), open: +r.open, high: +r.high, low: +r.low, close: +r.close, volume: +r.volume };
          if (ts < oldest) oldest = ts;
        }
        if (oldest >= end) break; end = oldest - 86400; if (oldest < 1300000000) break;
      }
      const d = Object.keys(m).sort();
      if (d.length > 200) return d.slice(-days).map(k => m[k]);
    } catch (e) { }
    try {                                   // Coinbase — 300/call
      const m = {}; let end = Date.now();
      for (let i = 0; i < 14 && Object.keys(m).length < days; i++) {
        const s = new Date(end - 300 * 864e5).toISOString(), e2 = new Date(end).toISOString();
        const j = await jget('https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=86400&start=' + s + '&end=' + e2, 20000);
        if (!Array.isArray(j) || !j.length) break;
        for (const c of j) if (c[4] > 0) m[iso(c[0] * 1000)] = { date: iso(c[0] * 1000), open: c[3], high: c[2], low: c[1], close: c[4], volume: c[5] };
        end = Math.min.apply(null, j.map(c => c[0])) * 1000 - 864e5;
      }
      const d = Object.keys(m).sort();
      if (d.length > 200) return d.slice(-days).map(k => m[k]);
    } catch (e) { }
    try {                                   // Kraken — 721 max, last resort
      const j = await jget('https://api.kraken.com/0/public/OHLC?pair=XXBTZUSD&interval=1440', 20000);
      if (j && j.result) {
        const k = Object.keys(j.result).filter(x => x !== 'last')[0], m = {};
        j.result[k].forEach(c => { if (+c[4] > 0) m[iso(c[0] * 1000)] = { date: iso(c[0] * 1000), open: +c[1], high: +c[2], low: +c[3], close: +c[4], volume: +c[6] }; });
        const d = Object.keys(m).sort();
        if (d.length > 200) return d.slice(-days).map(x => m[x]);
      }
    } catch (e) { }
    return null;
  }

  /* Live BTC price. Returns {price, change24, source} or null. */
  async function ticker() {
    try {
      const j = await jget('https://api.kraken.com/0/public/Ticker?pair=XXBTZUSD', 8000);
      if (j && j.result) { const k = Object.keys(j.result)[0], r = j.result[k];
        return { price: +r.c[0], change24: (+r.c[0] / +r.o - 1) * 100, source: 'Kraken' }; }
    } catch (e) { }
    try {
      const j = await jget('https://api.exchange.coinbase.com/products/BTC-USD/ticker', 8000);
      if (j && j.price) return { price: +j.price, change24: null, source: 'Coinbase' };
    } catch (e) { }
    try {
      const j = await jget('https://www.bitstamp.net/api/v2/ticker/btcusd/', 8000);
      if (j && j.last) return { price: +j.last, change24: +j.percent_change_24, source: 'Bitstamp' };
    } catch (e) { }
    return null;
  }

  /* Daily closes for any Coinbase product, e.g. altDaily('ETH-USD'). null if unsupported. */
  async function altDaily(product, days) {
    days = days || 300;
    try {
      const e2 = new Date().toISOString(), s = new Date(Date.now() - Math.min(days, 300) * 864e5).toISOString();
      const j = await jget('https://api.exchange.coinbase.com/products/' + product + '/candles?granularity=86400&start=' + s + '&end=' + e2, 20000);
      if (Array.isArray(j) && j.length) return j.map(c => ({ date: iso(c[0] * 1000), close: c[4], high: c[2], low: c[1] })).sort((a, b) => a.date < b.date ? -1 : 1);
    } catch (e) { }
    return null;
  }

  /* Loud failure. The 8 broken pages all failed by rendering nothing, which is
     indistinguishable from a page nobody opened. Never fail quietly again. */
  function noFeed(sel, msg) {
    const host = typeof sel === 'string' ? document.querySelector(sel) : sel;
    if (!host) return;
    const d = document.createElement('div');
    d.style.cssText = 'margin:16px 0;padding:12px 16px;border:1px solid #C4382A;border-radius:6px;' +
      'background:rgba(196,56,42,.12);color:#C4382A;font:12px ui-monospace,Menlo,monospace;line-height:1.6';
    d.textContent = '⛔ NO FEED — ' + (msg || 'every price source failed. This page is showing nothing, not zero.');
    host.prepend(d);
  }

  g.FEED = { daily: daily, ticker: ticker, altDaily: altDaily, noFeed: noFeed, jget: jget, iso: iso };
})(window);
