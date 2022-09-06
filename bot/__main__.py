from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ( CommandHandler, Filters, CallbackQueryHandler, Updater)
from bot.helper.message import Editmessage, Sendmessage, download_file, logger
import os
from bot.helper.checker import make_keyboard, main_checker

bot_token = os.environ.get('TG_BOT_TOKEN')
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

def help(update, context):
    chat_id = update.message.chat_id
    text = "<b>Available Sites:\n!alt~space~combo* - to check Altbalaji accounts\n!hoi~space~combo* - to check Hoichoi accounts\n!voo~space~combo* - to check Voot accounts\n!zee~space~combo* - to check Zee5 accounts\n\nMiscellaneous:-\n!pst~space~title|text - to paste text on Throwbin.io and get paste link</b>(If you don't want to give title then skip it just send the text)\n\n*combo here means Email:password combination,':' is important."
    Sendmessage(chat_id, text, reply_markup= InlineKeyboardMarkup(startmessage))

def start_check(update, context):
    chat_id = update.message.chat_id
    msg_id = update.message.message_id
    reply = update.message.reply_to_message
    if not reply:
        Sendmessage(chat_id, "Please reply to some text or document!", reply_id=msg_id)
        return
    Sendmessage(chat_id, "Select the config:", reply_id=reply.message_id, reply_markup=make_keyboard())

def button(update, context) -> None:
    query = update.callback_query
    chat_id = query.from_user.id
    msg_id = query.message.message_id
    msg= update.callback_query.message.reply_to_message
    query.answer()
    query.edit_message_text(text="<i>Intializing...</i>", parse_mode="HTML")
    if msg.document:
        combo = download_file(msg.document.file_id, msg.document.file_name)
        file = True
    else:
        combo = msg.text
        file = False
    main_checker(chat_id, msg_id, context, query.data, combo, file=file)

def main():
    updater = Updater(
        bot_token,
        use_context=True
    )
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("check", start_check))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CallbackQueryHandler(button))
    logger.info("Bot Started!!!")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
