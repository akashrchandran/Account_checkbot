from pathlib import Path

from bot.helper.database import set_up_database

Path("combo/").mkdir(exist_ok=True)
Path("storage/").mkdir(exist_ok=True)
set_up_database()