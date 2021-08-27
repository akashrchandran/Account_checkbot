from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ( CommandHandler, Filters, MessageHandler, Updater)
from message import Editmessage, Sendmessage, logger
from Checks.Altbalaji import altbalaji_helper
from Checks.hoichoi import hoichoi_helper
from Checks.voot import Voot_helper
from Checks.zee5 import zee_helper
from Checks.sun import Sun_helper
from Miscellaneous.Scraper import pastebin, text_scraper, throwbin, ghostbin
import os


bot_token = os.environ.get('TG_BOT_TOKEN')
WEBHOOK = bool(os.environ.get("WEBHOOK", False))
PORT = int(os.environ.get("PORT", "1234"))
HEROKU_URL = os.environ.get("HEROKU_URL")
startmessage = [[
		InlineKeyboardButton(
			"Telegraph 📝",
			url='https://telegra.ph/Instructions-to-Use-This-Bot-04-07'
		),
        InlineKeyboardButton(
			"DEV 👷🏻",
			url='https://t.me/pseudo_monk'
		)
        ]]


def start(update, context):
    info = update.effective_user
    print(info)
    chat_id = info.id
    userid= info['username']
    text = f'Welcome @{userid}, To Account Check Bot, to know more use /help or read the telegraph below. This bot is provided for educational use only, any misuse then you should be responsible'
    Sendmessage(chat_id, text, reply_markup=InlineKeyboardMarkup(startmessage))
    return

    
def combos_spilt(combos):
    split = combos.split('\n')
    return split


def help(update, context):
    chat_id = update.message.chat_id
    text = "<b>Available Sites:\n!alt~space~combo* - to check Altbalaji accounts\n!hoi~space~combo* - to check Hoichoi accounts\n!voo~space~combo* - to check Voot accounts\n!zee~space~combo* - to check Zee5 accounts\n\nMiscellaneous:-\n!pst~space~title|text - to paste text on Throwbin.io and get paste link</b>(If you don't want to give title then skip it just send the text)\n\n*combo here means Email:password combination,':' is important."
    Sendmessage(chat_id, text, reply_markup= InlineKeyboardMarkup(startmessage))

def duty(update, context):
    chat_id = update.message.chat_id
    text =  update.message.text.split(' ', 1)
    if text[0] == '!alt':
        if '\n' in text[1]:
            simple = combos_spilt(text[1])
            for i in simple:
                altbalaji_helper(chat_id, i)
            Sendmessage(chat_id, 'Completed')
        else:
            altbalaji_helper(chat_id, text[1])
    elif text[0] == '!voo':
        if '\n' in text[1]:
            simple = combos_spilt(text[1])
            for i in simple:
                Voot_helper(chat_id, i)
            Sendmessage(chat_id, 'Completed')
        else:
            Voot_helper(chat_id, text[1])
    elif text[0] == '!hoi':
        if '\n' in text[1]:
            simple = combos_spilt(text[1])
            for i in simple:
                hoichoi_helper(chat_id, i)
            Sendmessage(chat_id, 'Completed')
        else:
            hoichoi_helper(chat_id, text[1])
    elif text[0] == '!zee':
        if '\n' in text[1]:
            simple = combos_spilt(text[1])
            for i in simple:
                zee_helper(chat_id, i)
            Sendmessage(chat_id, 'Completed')
        else:
            zee_helper(chat_id, text[1])
    elif text[0] == '!sun':
        if '\n' in text[1]:
            simple = combos_spilt(text[1])
            for i in simple:
                Sun_helper(chat_id, i)
            Sendmessage(chat_id, 'Completed')
        else:
            Sun_helper(chat_id, text[1])
    elif text[0] == '!pst':
            try:
                throwbin(chat_id, text[1])
            except IndexError:
                Sendmessage(chat_id, "<i>Somethings wrong with your format!</i>")
    else:
        logger.info('Unknown Command')


def scraperdfnc(update, context):
    msg = update.message.text
    status_msg = update.message
    chat_id = status_msg.chat_id
    try:
        if 'pastebin' in msg:
            link = msg.split(' ')[1]
            pastebin(chat_id,link)
        elif 'ghostbin' in msg:
            link = msg.split(' ')[1]
            ghostbin(chat_id,link)
        else:
            scrape_text = status_msg['reply_to_message']['text']
            text_scraper(chat_id, scrape_text)
    except:
        Sendmessage(chat_id, 'Only Supports pastebin, please check if you send paste bin link')

def main():
    updater = Updater(
        bot_token,
        use_context=True
    )
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, duty))
    dp.add_handler(CommandHandler("scrape", scraperdfnc))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    logger.info("Bot Started!!!")
    if WEBHOOK:
        updater.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TG_BOT_TOKEN
        )
        updater.bot.set_webhook(url=HEROKU_URL + TG_BOT_TOKEN)
    else:
        updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
