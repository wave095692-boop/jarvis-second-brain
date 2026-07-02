import urllib.request
import json
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context

try:
    with open('/Users/apple/.gemini/antigravity-ide/scratch/new_email_credentials.json', 'r') as f:
        creds = json.load(f)
    email = creds['email']
    password = creds['password']
except Exception as e:
    print(f"Could not load new_email_credentials.json: {e}")
    email = "bossjarvis_farm_1@web-library.net"
    password = "SuperSecretPassword123!"

print(f"Logging in to get token for {email}...")

# 1. Get token
token_data = json.dumps({'address': email, 'password': password}).encode('utf-8')
token_req = urllib.request.Request(
    'https://api.mail.tm/token', 
    data=token_data, 
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
)
try:
    res = json.loads(urllib.request.urlopen(token_req).read().decode('utf-8'))
    token = res['token']
    print(f"Token acquired: {token[:15]}...")
except Exception as e:
    print(f"Error getting token: {e}")
    exit(1)

# 2. Check messages
messages_req = urllib.request.Request(
    'https://api.mail.tm/messages',
    headers={'Authorization': f'Bearer {token}', 'User-Agent': 'Mozilla/5.0'}
)

print("Fetching messages from inbox...")
try:
    msgs = json.loads(urllib.request.urlopen(messages_req).read().decode('utf-8'))
    print(f"Total messages: {len(msgs.get('hydra:member', []))}")
    for m in msgs.get('hydra:member', []):
        print(f"ID: {m['id']} | From: {m['from']} | Subject: {m['subject']}")
        # Get message detail
        msg_detail_req = urllib.request.Request(
            f"https://api.mail.tm/messages/{m['id']}",
            headers={'Authorization': f'Bearer {token}', 'User-Agent': 'Mozilla/5.0'}
        )
        msg_detail = json.loads(urllib.request.urlopen(msg_detail_req).read().decode('utf-8'))
        print("--- Text Content ---")
        print(msg_detail.get('text'))
        print("--- HTML Content snippet ---")
        print(msg_detail.get('html')[:1000] if msg_detail.get('html') else 'None')
        print("--------------------")
except Exception as e:
    print(f"Error fetching messages: {e}")
