#!/bin/bash
# Launcher script for Jarvis Second Brain Dashboard

# Dynamically resolve directory containing this script
DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIRECTORY"

# Kill any existing server on port 8500
lsof -t -i :8500 | xargs kill -9 2>/dev/null

# Launch python server in background
nohup ./.venv/bin/python -u server.py > server.log 2>&1 &

echo "--------------------------------------------------------"
echo "🤖 JARVIS SECOND BRAIN DASHBOARD LAUNCHED"
echo "URL: http://localhost:8500"
echo "LAN: http://$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost"):8500"
echo "--------------------------------------------------------"
