import re
import requests
import json

def test_run():
    test_email = 'randommail@yahoo.com'
    test_pass = 'testthispassword'
    try:
        print(start(test_email, test_pass))
    except Exception as e:
        raise e

def get_ready():
    global crsf_token
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    req = requests.get("https://www.sunnxt.com/", headers=header)
    crsf_token = re.search(r'<meta name="csrf-token" content="(\S+)"', req.text)[1]
    
def start(email, password):
    session_requests = requests.session()
    session_requests.headers["x-csrf-token"] = crsf_token
    session_requests.headers["x-requested-with"] = 'XMLHttpRequest'
    session_requests.headers["content-type"] = "application/json;charset=UTF-8"
    payload = '{"email":"%s","password":"%s"}' % (email, password)
    req2 = session_requests.post("https://www.sunnxt.com/login", data=payload)
    resonse = req2.json()
    if req2.status_code != 200:
        return False, {'Status': 'Error', 'Code': req2.status_code,  'Message': resonse["error"]}
    profile = json.loads(resonse["profile"])
    pack_active = profile["result"]["profile"]["subscriptionStatus"]
    if pack_active in ["Expired", "Inactive"]:
        return False, {'Status': 'Free / Expired'}
    Pack_name = resonse["userSubscriptions"]["results"][0]["displayName"]
    date = resonse["userSubscriptions"]["results"][0]["validityEndDate"]
    return True, {'Status': pack_active, 'Plan': Pack_name, 'Expires On': date}

get_ready()