import urllib.request
import json
import ssl
import random
import string

ssl._create_default_https_context = ssl._create_unverified_context

# Generate random string for email username
rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
email = f"jarvisboss_{rand_str}@web-library.net"
password = ''.join(random.choices(string.ascii_letters + string.digits, k=12)) + "!"

print(f"Creating Mail.tm account with email: {email} and password: {password}...")

# 1. Get domains to confirm web-library.net is available
domains_req = urllib.request.Request(
    'https://api.mail.tm/domains',
    headers={'User-Agent': 'Mozilla/5.0'}
)
try:
    domains_res = json.loads(urllib.request.urlopen(domains_req).read().decode('utf-8'))
    available_domains = [d['domain'] for d in domains_res.get('hydra:member', [])]
    print(f"Available domains: {available_domains}")
    if available_domains:
        domain = available_domains[0]
        email = f"jarvisboss_{rand_str}@{domain}"
except Exception as e:
    print(f"Error fetching domains: {e}, falling back to web-library.net")

# 2. Create account
create_data = json.dumps({'address': email, 'password': password}).encode('utf-8')
create_req = urllib.request.Request(
    'https://api.mail.tm/accounts',
    data=create_data,
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
)
try:
    res = json.loads(urllib.request.urlopen(create_req).read().decode('utf-8'))
    print("Account created successfully:")
    print(json.dumps(res, indent=2))
except Exception as e:
    print(f"Error creating account: {e}")
    exit(1)

# 3. Get token
token_data = json.dumps({'address': email, 'password': password}).encode('utf-8')
token_req = urllib.request.Request(
    'https://api.mail.tm/token',
    data=token_data,
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
)
try:
    res = json.loads(urllib.request.urlopen(token_req).read().decode('utf-8'))
    token = res['token']
    print(f"Token acquired: {token}")
    # Write details to credentials file
    with open('/Users/apple/.gemini/antigravity-ide/scratch/new_email_credentials.json', 'w') as f:
        json.dump({'email': email, 'password': password, 'token': token}, f, indent=2)
    print("Credentials saved to /Users/apple/.gemini/antigravity-ide/scratch/new_email_credentials.json")
except Exception as e:
    print(f"Error getting token: {e}")
