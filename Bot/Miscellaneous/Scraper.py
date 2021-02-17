import re
from bs4 import BeautifulSoup
import requests
from throwbin import ThrowBin
from message import Sendmessage, Editmessage

def pastebin(chat_id, link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.find('textarea', 'textarea').text
    lst = re.findall('\S+@\S+.\S+:\S+', str(text))
    sperator = '\n'
    cleared = sperator.join(lst)
    Sendmessage(chat_id, cleared)

def text_scraper(chat_id, text):
    lst = re.findall('\S+@\S+.\S+:\S+', str(text))
    sperator = '\n'
    cleared = sperator.join(lst)
    Sendmessage(chat_id, cleared)

def throwbin(chat_id, text):
    msg = Sendmessage(chat_id, '<i>Pasting...</i>')
    try:
        real = text.split('|')
        title = real[0]
        real_text = real[1]
    except IndexError:
        real_text = text
        title = '@acc_checkbot'
    tb = ThrowBin()
    my_paste = tb.post(
        title=title,
        text=real_text,
        syntax="text"
    )
    print(f"Status {my_paste.status} | Link: {my_paste.link}")
    msg_txt = f'<b>Pasted ✅\nStatus: {my_paste.status}\nLink: {my_paste.link}</b>'
    Editmessage(chat_id, msg_txt, msg)

