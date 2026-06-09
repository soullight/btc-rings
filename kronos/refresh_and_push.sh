#!/bin/bash
# Kronos hourly refresh + publish for GitHub Pages (soullight.github.io/btc-rings).
# Regenerates kronos/*.json via the forecaster, then commits + pushes if changed.
# Loaded by ~/Library/LaunchAgents/com.lawrence.kronos-pages.plist (StartInterval 3600).
# Logs to /tmp/kronos_pages.log.
set -uo pipefail

REPO="/Users/lawgreg/consciousness_agent/code/btc-rings-site"
PY="/Users/lawgreg/.pyenv/versions/3.11.6/bin/python3"
GIT="/opt/homebrew/bin/git"
BRANCH="main"
LOG="/tmp/kronos_pages.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

log "=== refresh_and_push start ==="
cd "$REPO" || { log "FATAL: cannot cd to $REPO"; exit 1; }

# --- Clear a stale index/HEAD lock only if no live git process is running ---
for lock in .git/index.lock .git/HEAD.lock; do
  if [ -f "$lock" ]; then
    if pgrep -x git >/dev/null 2>&1; then
      log "lock $lock present and a git process is live; leaving it and bailing"
      exit 0
    fi
    log "removing stale lock $lock (no live git proc)"
    rm -f "$lock"
  fi
done

# --- Regenerate the JSON the dashboard reads ---
log "running kronos_forecast.py ..."
( cd "$REPO/kronos" && "$PY" kronos_forecast.py ) >> "$LOG" 2>&1
rc=$?
if [ $rc -ne 0 ]; then
  log "forecast FAILED (rc=$rc); not committing"
  exit $rc
fi

# --- Commit only if something changed ---
"$GIT" add kronos/*.json
if "$GIT" diff --cached --quiet; then
  log "no JSON change; nothing to commit"
  exit 0
fi
"$GIT" commit -m "kronos: hourly forecast refresh" >> "$LOG" 2>&1
log "committed."

# --- Push, with a single rebase+retry on transient conflict ---
# --autostash lets the rebase proceed even if unrelated tracked files in the
# working tree are dirty (this repo carries other in-progress edits).
push_once() {
  "$GIT" pull --rebase --autostash origin "$BRANCH" >> "$LOG" 2>&1 && "$GIT" push origin "$BRANCH" >> "$LOG" 2>&1
}
if push_once; then
  log "pushed OK."
else
  log "push failed; retrying once after rebase ..."
  if push_once; then
    log "pushed OK on retry."
  else
    log "push still failing; leaving commit local for next run."
    exit 1
  fi
fi

log "=== refresh_and_push done ==="
