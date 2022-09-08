import requests
from datetime import date
from bot.helper.util import ConfigInfo, ComboStats, Free, Expired, Hit, Bad

config_info = ConfigInfo(
    name="Altbalaji config",
    site="https://altbalaji.com",
    proxy=False,
    supported= ComboStats(bad = Bad, hit = Hit, free = Free, expire = Expired),
)

class Interface:
    def check(self, email, password):
        self.session = requests.Session()
        self.session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        self.session.headers['content-type'] = 'application/json'
        self.session.headers['accept'] = 'application/json, text/plain, */*'
        url = 'https://api.cloud.altbalaji.com/accounts/login?domain=IN'
        payload = '{"username":"%s","password":"%s"}' % (email, password)
        response = self.session.post(url, data=payload)
        result = response.json()
        if response.status_code != 200:
            return Bad(status=result['status'], code=result['code'], message=result['message'])
        session_token = result['session_token']
        subs_url = 'https://payment.cloud.altbalaji.com/accounts/orders?limit=1&domain=IN'
        self.session.headers['xssession'] = str(session_token)
        response = self.session.get(subs_url)
        result = response.json()
        if result['orders'] == []:
            return Free()
        validto = result['orders'][0]['dates']['valid_to']
        validtosplit = validto.split('T')[0]
        sub2split = validtosplit.split('-')
        trial = date(int(sub2split[0]), int(sub2split[1]),int(sub2split[2])) < date.today()
        if trial:
            return Expired()
        days = date(int(sub2split[0]), int(sub2split[1]), int(sub2split[2])) - date.today()
        subscription = result['orders'][0]['product']['titles']
        Pack_name = subscription['default']
        Pack_recur = bool(result['orders'][0]['product']['recurring'])
        Pack_date = subscription['en']
        return Hit(plan=Pack_name, type=Pack_date, left=days.days, recur=Pack_recur)