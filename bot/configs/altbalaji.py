import requests
from datetime import date


def test_run():
    test_email = 'randommail@yahoo.com'
    test_pass = 'testthispassword'
    try:
        print(start(test_email, test_pass))
    except Exception as e:
        raise e


def start(email, password):
    session_request = requests.Session()
    url = 'https://api.cloud.altbalaji.com/accounts/login?domain=IN'
    payload = '{"username":"%s","password":"%s"}' % (email, password)
    response = session_request.post(url, data=payload)
    result = response.json()
    if response.status_code != 200:
        return False, {'Status': result['status'], 'Code': result['code'],  'Message': result['message']}
    session_token = result['session_token']
    subs_url = 'https://payment.cloud.altbalaji.com/accounts/orders?limit=1&domain=IN'
    head2 = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'content-type': 'application/json',
        'xssession': str(session_token),
    }
    response = session_request.get(subs_url, headers=head2)
    result = response.json()
    if result['orders'] == []:
        return False, {'Status': 'Free'}
    validto = result['orders'][0]['dates']['valid_to']
    validtosplit = validto.split('T')[0]
    sub2split = validtosplit.split('-')
    trial = date(int(sub2split[0]), int(sub2split[1]),
                 int(sub2split[2])) < date.today()
    if trial:
        return False, {'status': 'Expired'}
    days = date(int(sub2split[0]), int(sub2split[1]),
                int(sub2split[2])) - date.today()
    subscription = result['orders'][0]['product']['titles']
    Pack_name = subscription['default']
    Pack_recur = str(result['orders'][0]['product']['recurring'])
    Pack_date = subscription['en']
    return True, {'Status': 'Premium', 'Plan': Pack_name, 'Type': Pack_date, 'Days Left': days.days, 'Recurring': Pack_recur.capitalize()}
