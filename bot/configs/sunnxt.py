import re
import requests
import json

from bot.helper.util import Bad, ComboStats, ConfigInfo, Free, Hit

config_info = ConfigInfo(
    name="Sunnxt config",
    site="https://www.sunnxt.com/",
    proxy=True,
    supported= ComboStats(bad = Bad, hit = Hit, free = Free),
)

class Interface:
    def __init__(self):
        req = self.session.get("https://www.sunnxt.com/")
        self.crsf_token = re.search(r'<meta name="csrf-token" content="(\S+)"', req.text)[1]

    def check(self, email, password):
        self.session = requests.Session()
        self.session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        self.session.headers["x-csrf-token"] = self.crsf_token
        self.session.headers["x-requested-with"] = 'XMLHttpRequest'
        self.session.headers["content-type"] = "application/json;charset=UTF-8"
        payload = '{"email":"%s","password":"%s"}' % (email, password)
        req2 = self.session.post("https://www.sunnxt.com/login", data=payload)
        resonse = req2.json()
        if req2.status_code != 200:
            return Bad(code=req2.status_code, message=resonse["error"])
        profile = json.loads(resonse["profile"])
        pack_active = profile["result"]["profile"]["subscriptionStatus"]
        if pack_active in ["Expired", "Inactive"]:
            return Free()
        Pack_name = resonse["userSubscriptions"]["results"][0]["displayName"]
        date = resonse["userSubscriptions"]["results"][0]["validityEndDate"]
        return Hit(status=pack_active, plan=Pack_name, left=date)