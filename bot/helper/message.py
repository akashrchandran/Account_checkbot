import logging
from telegram import Bot
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

bot_token = os.environ.get('TG_BOT_TOKEN')
bot = Bot(bot_token)

def Sendmessage(chat_id, text, reply_id = None, reply_markup=None):
    try:
        message = bot.send_message(chat_id=chat_id,
                                   text=text,
                                   reply_to_message_id=reply_id,
                                   parse_mode="HTML",
                                   reply_markup=reply_markup
                                   )
        return message.message_id
    except Exception as e:
        logger.info(e)
        raise UserWarning from e


def Editmessage(chat_id, text, msg_id, reply_markup=None):
    try:
        bot.edit_message_text(chat_id=chat_id,
                              text=text, message_id=msg_id, parse_mode="HTML",
                              reply_markup=reply_markup
                              )
    except Exception as e:
        logger.info(e)

def download_file(file_id, file_name):
    newFile = bot.get_file(file_id)
    return newFile.download(custom_path=f"combo/{file_name}")

def send_file(chat_id, reply_id, file):
    try:
        bot.send_document(chat_id, open(file, 'rb'), reply_to_message_id=reply_id)
    except Exception as e:
        logger.info(e)