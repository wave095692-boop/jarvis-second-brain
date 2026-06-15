import json
import urllib.request
import ssl

ssl_context = ssl._create_unverified_context()

def check_project_billing(token, project_id):
    url = f"https://cloudbilling.googleapis.com/v1/projects/{project_id}/billingInfo"
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    try:
        with urllib.request.urlopen(req, context=ssl_context) as response:
            info = json.loads(response.read().decode('utf-8'))
            print(f"Billing info for {project_id}:", json.dumps(info, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error getting billing info for {project_id}:", e)

if __name__ == '__main__':
    with open('/Users/apple/.gemini/oauth_creds.json', 'r') as f:
        creds = json.load(f)
    token = creds.get('access_token')
    
    if token:
        print("Using token from oauth_creds.json...")
        check_project_billing(token, "gen-lang-client-0436078158")
        check_project_billing(token, "gen-lang-client-0695447969")
