from datetime import date

import requests
from bot.helper.util import Bad, ComboStats, ConfigInfo, Free, Hit

config_info = ConfigInfo(
    name="Hoichoitv config",
    site="https://hoichoi.tv",
    proxy=False,
    supported= ComboStats(bad = Bad, hit = Hit, free = Free),
)

class Interface:
    def check(self, email, password):
        self.session = requests.Session()
        self.session.params = {"site": "hoichoitv", "userId": "f76c181a-94b5-11eb-a8b3-0242ac130003"}
        payload = '{"email":"%s","password":"%s"}' %(email, password)
        response = self.session.post('https://prod-api.viewlift.com/identity/signin', data=payload)
        result = response.json()
        if response.status_code != 200:
            return Bad(code=result['code'], message=result['error'])
        elif result['isSubscribed'] == False:
            return Free()
        self.session.headers['authorization'] = result['authorizationToken']
        response = self.session.get('https://prod-api.viewlift.com/subscription/user')
        result = response.json()
        Pack_name = result["subscriptionPlanInfo"]["name"]
        timing = result["subscriptionInfo"]["subscriptionEndDate"].split('T')[0]
        sub2split = timing.split('-')
        days = date(int(sub2split[0]), int(sub2split[1]), int(sub2split[2])) - date.today()
        Pack_recur = result["subscriptionPlanInfo"]["renewable"]
        return Hit(plan=Pack_name, left=days.days, recur=Pack_recur)
