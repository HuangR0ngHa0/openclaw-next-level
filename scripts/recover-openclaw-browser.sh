#!/usr/bin/env bash
set -euo pipefail

LOG_DIR="$HOME/.openclaw/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/recover-browser.log"

echo "[$(date '+%F %T')] recover-browser start" >> "$LOG_FILE"

# 1) Ensure gateway is up (safe if already running)
openclaw gateway start >> "$LOG_FILE" 2>&1 || true

# 2) If remote CDP is already listening, do nothing
if ss -ltn 2>/dev/null | grep -q ':9222 '; then
  echo "[$(date '+%F %T')] port 9222 already listening; skip chromium launch" >> "$LOG_FILE"
  exit 0
fi

# 3) Launch Chromium with the known-good profile + CDP port
/snap/bin/chromium \
  --user-data-dir="$HOME/snap/chromium/common/chromium" \
  --remote-debugging-port=9222 \
  >> "$LOG_FILE" 2>&1 &

echo "[$(date '+%F %T')] chromium launch requested" >> "$LOG_FILE"
exit 0
