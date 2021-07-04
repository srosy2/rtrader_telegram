from telegram.ext import Updater, CommandHandler
import requests
import re
from prepare import PrepareMessage
from server import Client


def get_url() -> str:
    contents = requests.get('https://random.dog/woof.json').json()
    image_url = contents['url']
    return image_url


def bop(update, context):
    client = Client(465, 993, 'gmail.com', 'leshhuk3@gmail.com', 'leshhuk.2000@mail.ru', 'Dkflbckfd1!')
    client.read()
    message = PrepareMessage('download_2_file', 'trader.jpg')
    url = get_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=message.return_image())
    context.bot.send_message(chat_id=chat_id, text=message.return_text())


def main():
    updater = Updater('1747444454:AAEW0elfYpO5OUr0A3aWHw1AeeLEybfRxjM', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop', bop))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
