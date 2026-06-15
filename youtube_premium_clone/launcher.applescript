try
	do shell script "nc -z localhost 8000"
on error
	do shell script "cd /Users/apple/.gemini/antigravity-ide/scratch/youtube_premium_clone && nohup python3 server.py > /dev/null 2>&1 &"
	delay 1
end try

try
	do shell script "open -a \"Google Chrome\" --args --app=\"http://localhost:8000\""
on error
	do shell script "open \"http://localhost:8000\""
end try
