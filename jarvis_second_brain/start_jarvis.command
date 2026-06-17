#!/bin/bash
# Double-clickable launcher for Jarvis Second Brain Dashboard on macOS

# Dynamically resolve directory containing this script
DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIRECTORY"

# Kill any existing server on port 8500
lsof -t -i :8500 | xargs kill -9 2>/dev/null

# Launch python server in background
nohup python3 server.py > server.log 2>&1 &

echo "--------------------------------------------------------"
echo "🤖 JARVIS SECOND BRAIN DASHBOARD LAUNCHED"
echo "URL: http://localhost:8500"
echo "LAN: http://$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost"):8500"
echo "--------------------------------------------------------"

# Wait 1 second for the server to bind, then automatically open the browser
sleep 1
open "http://localhost:8500"

echo "เซิร์ฟเวอร์รันอยู่เบื้องหลังเรียบร้อยแล้ว คุณสามารถปิดหน้าต่าง Terminal นี้ได้เลยครับ"
sleep 3
exit 0
