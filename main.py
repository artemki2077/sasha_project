import telebot
from telebot.types import Message
from cfg import config
from Filters import count_stars

client = telebot.TeleBot(config['token'])


@client.message_handler(commands=['start'])
def start_message(message):
    client.send_message(message.chat.id, "Привет!✌️ Я - Star Counter! Помогу тебе посчитать сколько звёзд на твоем фото. Просто отправь мне фото ночного неба! ")


@client.message_handler(content_types=['photo'])
def handle_docs_photo(message: Message):
    client.reply_to(message, "Считаю...")

    file_info = client.get_file(message.photo[-1].file_id)
    downloaded_file = client.download_file(file_info.file_path)

    src = f'files/photos/{message.chat.id}.jpg'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    res = count_stars(src)

    if type(res) == int:
        client.reply_to(message, f"На твоем фото {count_stars(src)} звезд!")
    else:
        client.reply_to(message, f"на твоей фотографии не звёзды")


client.polling(none_stop=True, interval=0)