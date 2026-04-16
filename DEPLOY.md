# Deploy Bitcoin Rings to GitHub Pages

## One-time setup (run from this folder):

```bash
cd btc-rings-site
git init
git add .
git commit -m "Bitcoin Rings — live BTC visualization"
gh repo create btc-rings --public --source=. --push
```

Then go to: https://github.com/soullight/btc-rings/settings/pages

- Source: **Deploy from a branch**
- Branch: **main** / **(root)**
- Click Save

Your site will be live at: **https://soullight.github.io/btc-rings/**

## Pages:
- `/` or `/index.html` — The Map (clean 4-ring view)
- `/nav.html` — Navigation hub
- `/swing.html` — 20/60 day swing cycles
- `/macro.html` — Full macro Cycle 4 view
- `/backtest.html` — Swing system backtest

## To update later:
```bash
cd btc-rings-site
git add .
git commit -m "Update"
git push
```
