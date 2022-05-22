import requests
from datetime import datetime


def test_run():
    test_email = 'randommail@yahoo.com'
    test_pass = 'testthispassword'
    try:
        print(voot_helper(test_email, test_pass))
    except Exception as e:
        raise e


def voot_helper(email, password):
    session_requests = requests.session()
    payload = '{"type":"traditional","deviceId":"X11","deviceBrand":"PC/MAC","data":{"email":"%s","password":"%s"}}' % (
        email, password)
    session_requests.headers['content-type'] = 'application/json;charset=UTF-8'
    login_url = "https://userauth.voot.com/usersV3/v3/login"
    result = session_requests.post(login_url, data=payload)
    response = result.json()
    if result.status_code != 200:
        return False, {'Status': 'Error', 'Code': response['status']['code'],  'Message': response['status']['message']}
    acess = response['data']['authToken']['accessToken']
    session_requests.headers.update({'accesstoken': str(acess)})
    subs_url = 'https://pxapi.voot.com/smsv4/int/ps/v1/voot/transaction/list'
    response = session_requests.get(subs_url)
    result = response.json()
    total = result['results']['total']
    if int(total) == 0:
        return False, {'Status': 'Free'}
    pay_list = result['results']['list'][0]
    ts = int(pay_list['endDate']['timeStamp'])
    try:
        human = datetime.utcfromtimestamp(ts)
    except ValueError:
        human = datetime.fromtimestamp(ts/1000.0)
    expire = human < datetime.today()
    if expire:
        return False, {'status': 'Expired'}
    Pack_name = pay_list['itemDetails']['name']
    Pack_recur = pay_list['itemDetails']['isRenewable']
    days = human - datetime.today()
    return True, {'Status': 'Premium', 'Plan': Pack_name, 'Days Left': days.days, 'Recurring': Pack_recur}


test_run()
