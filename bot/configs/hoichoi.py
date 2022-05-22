import requests
from datetime import date

def test_run():
    test_email = 'randommail@yahoo.com'
    test_pass = 'testthispassword'
    try:
        print(hoichoi_helper(test_email, test_pass))
    except Exception as e:
        raise e

def hoichoi_helper(email, password):
    session_request = requests.Session()
    url = 'https://prod-api.viewlift.com/identity/signin?site=hoichoitv&deviceId=browser-f76c181a-94b5-11eb-a8b3-0242ac130003'
    payload = '{"email":"%s","password":"%s"}' %(email, password)
    response = session_request.post(url, data=payload)
    result = response.json()
    if response.status_code != 200:
        return False, {'Status': 'Error', 'Code': result['code'],  'Message': result['error']}
    elif result['isSubscribed'] == False:
        return False, {'Status': 'Free'}
    user_token = result['authorizationToken']
    session_request.headers['authorization'] = user_token
    url2 = 'https://prod-api.viewlift.com/subscription/user?site=hoichoitv&userId=f76c181a-94b5-11eb-a8b3-0242ac130003'
    response = session_request.get(url2)
    result = response.json()
    Pack_name = result["subscriptionPlanInfo"]["name"]
    timing = result["subscriptionInfo"]["subscriptionEndDate"].split('T')[0]
    sub2split = timing.split('-')
    days = date(int(sub2split[0]), int(sub2split[1]), int(sub2split[2])) - date.today()
    Pack_recur = result["subscriptionPlanInfo"]["renewable"]
    return True, {'Status': 'Premium', 'Plan': Pack_name, 'Days Left': days.days, 'Recurring': Pack_recur}