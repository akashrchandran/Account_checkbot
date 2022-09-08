from operator import le
import requests
from datetime import datetime
from bot.helper.util import Bad, ComboStats, ConfigInfo, Free, Hit, Expired

config_info = ConfigInfo(
    name="Voot config",
    site="https://voot.com",
    proxy=False,
    supported= ComboStats(bad = Bad, hit = Hit, free = Free, expire=Expired),
)

class Interface:
    def check(self, email, password):
        self.session = requests.Session()
        self.session.headers['content-type'] = 'application/json;charset=UTF-8'
        payload = '{"type":"traditional","deviceId":"X11","deviceBrand":"PC/MAC","data":{"email":"%s","password":"%s"}}' % (email, password)
        result = self.session.post("https://userauth.voot.com/usersV3/v3/login", data=payload)
        response = result.json()
        if result.status_code != 200:
            return Bad(code=response['status']['code'], message=response['status']['message'])
        acess = response['data']['authToken']['accessToken']
        self.session.headers.update({'accesstoken': str(acess)})
        response = self.session.get('https://pxapi.voot.com/smsv4/int/ps/v1/voot/transaction/list')
        result = response.json()
        total = result['results']['total']
        if int(total) == 0:
            return Free()
        pay_list = result['results']['list'][0]
        ts = int(pay_list['endDate']['timeStamp'])
        try:
            human = datetime.utcfromtimestamp(ts)
        except ValueError:
            human = datetime.fromtimestamp(ts/1000.0)
        expire = human < datetime.now()
        if expire:
            return Expired()
        Pack_name = pay_list['itemDetails']['name']
        Pack_recur = pay_list['itemDetails']['isRenewable']
        days = human - datetime.now()
        return Hit(plan=Pack_name, left=days.days, recur=Pack_recur)
