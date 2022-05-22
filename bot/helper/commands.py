from bot.configs.altbalaji import altbalaji_helper
from configs.hoichoi import hoichoi_helper
from configs.voot import Voot_helper
from configs.zee5 import zee_helper
from configs.sun import Sun_helper


class _BotCommands:
    def __init__(self):
        self.start = 'start'
        self.voot = "voo"
        self.alt = 'alt'
        self.zee5 = 'zee'
        self.hoichoi = 'hoi'
        self.scraper = 'scrape'

BotCommands = _BotCommands()