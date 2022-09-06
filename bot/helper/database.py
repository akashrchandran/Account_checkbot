import sqlite3
import threading

connection = sqlite3.connect("database.db",  check_same_thread=False)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
lock = threading.Lock()

def set_up_database():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `tasks` (
        `pid` INTEGER PRIMARY KEY AUTOINCREMENT,
        `chat_id` INT,
        `msg_id` INT,
        `site` VARCHAR,
        `total` INT,
        `checked` INT DEFAULT 0,
        `bad` INT DEFAULT 0,
        `free` INT DEFAULT 0,
        `expired` INT DEFAULT 0,
        `hits` INT DEFAULT 0
        );''')
    return

def add_task(site, chat_id, msg_id, total):
    with lock:
        cursor.execute(f'INSERT INTO tasks(site, chat_id, msg_id, total) VALUES ("{site}", {chat_id}, {msg_id}, {total})')
    return cursor.lastrowid

def fetch_one(pid):
    with lock:
        fetch = cursor.execute(f'SELECT * FROM tasks WHERE pid = {pid};').fetchone()
    return fetch

def update_one(pid, option):
    with lock:
        cursor.execute(f"UPDATE tasks SET {option} = {option} + 1 WHERE pid = {pid}")
        cursor.execute(f"UPDATE tasks SET checked = checked + 1 WHERE pid = {pid}")

def delete_one(pid):
    with lock:
        cursor.execute(f"DELETE FROM tasks WHERE pid = {pid}")