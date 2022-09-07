import requests
from datetime import date

from bot.helper.util import Bad, ComboStats, ConfigInfo, Expired, Hit

config_info = ConfigInfo(
    name="Sunnxt config",
    site="https://www.sunnxt.com/",
    proxy=True,
    supported= ComboStats(bad = Bad, hit = Hit, expire = Expired),
)

class Interface:
    def __init__(self):
        self.session = requests.session()
        self.session.headers['content-type'] = 'application/json'
        self.session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        self.session.headers['accept'] = '*/*'
    def check(self, email, password):
        payload = '{"email": "%s", "password":"%s"}' %(email, password)
        result = self.session.post("https://userapi.zee5.com/v2/user/loginemail", data=payload)
        response = result.json()
        if result.status_code != 200:
            return Bad(code=response['code'], message=response['message'])
        acess = response['access_token']
        self.session.headers['authorization'] = f'bearer {str(acess)}'
        subs_url = 'https://subscriptionapi.zee5.com/v1/subscription?translation=en&country=IN&include_all=flase'
        response1 = self.session.get(subs_url)
        result1 = response1.json()
        if result1 == []:
            return Expired()
        timedioint = result1[0]["subscription_end"].split('T')[0]
        sub2split = timedioint.split('-')
        days = date(int(sub2split[0]), int(sub2split[1]), int(sub2split[2])) - date.today()
        Pack_name = result1[0]['subscription_plan']['title']
        pack_price = str(result1[0]['subscription_plan']['price'])
        Pack_recur = result1[0]['recurring_enabled']
        Pack_pyed = result1[0]['payment_provider']
        return Hit(plan=Pack_name, left=days.days, recur=Pack_recur, extra={'Price': f'{pack_price} INR', 'Payment': Pack_pyed,})