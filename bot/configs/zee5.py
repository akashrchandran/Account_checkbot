import requests
from datetime import date

def test_run():
    test_email = 'randommail@yahoo.com'
    test_pass = 'testthispassword'
    try:
        print(zee_helper(test_email, test_pass))
    except Exception as e:
        raise e

def zee_helper(email, password):
    session_requests = requests.session()
    session_requests.headers['content-type'] = 'application/json'
    payload = '{"email": "%s", "password":"%s"}' %(email, password)
    login_url = "https://userapi.zee5.com/v2/user/loginemail"
    result = session_requests.post(login_url, data=payload)
    response = result.json()
    if result.status_code != 200:
        return False, {'Status': 'Error', 'Code': response['code'],  'Message': response['message']}
    acess = response['access_token']
    head2 = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'accept': '*/*', 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty',}
    session_requests.headers['authorization'] = f'bearer {str(acess)}'
    subs_url = 'https://subscriptionapi.zee5.com/v1/subscription?translation=en&country=IN&include_all=flase'
    response1 = session_requests.get(subs_url, headers=head2)
    result1 = response1.json()
    if result1 == []:
        return False, {'Status': 'Expired'}
    timedioint = result1[0]["subscription_end"].split('T')[0]
    sub2split = timedioint.split('-')
    days = date(int(sub2split[0]), int(sub2split[1]), int(sub2split[2])) - date.today()
    Pack_name = result1[0]['subscription_plan']['title']
    pack_price = str(result1[0]['subscription_plan']['price'])
    Pack_recur = result1[0]['recurring_enabled']
    Pack_pyed = result1[0]['payment_provider']
    return True, {'Status': 'Premium', 'Plan': Pack_name, 'Price': f'{pack_price} INR', 'Payment': Pack_pyed, 'Days Left': days.days, 'Recurring': Pack_recur}