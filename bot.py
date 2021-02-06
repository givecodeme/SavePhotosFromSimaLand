import os
import requests
import pandas as pd
import telebot
# from telebot import types
from config import token

bot = telebot.TeleBot(token)


def save_image(url, path, index):
    exp = url.split('.')[-1]
    path = f'{path}/{index}.{exp}'
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     text='Отпрвьте файл Excel от Сима Ленда')


@bot.message_handler(content_types=['document'])
def save_photos(message):
    # with open('test.txt', 'rb') as file:
    #     bot.send_document(message.chat.id, file)
    file_info = bot.get_file(message.document.file_id)
    file = bot.download_file(file_info.file_path)
    df = pd.read_excel(file)
    try:
        os.mkdir('Images')
    except:
        pass

    path = 'Images/'
    for index, item in df.iterrows():
        name = item['Заголовок']
        cat = item['Категория 1']
        images = item['Изображения'].split(';')
        path_image = os.path.join(path, cat)
        try:
            os.mkdir(path_image)
        except:
            pass
        path_image = os.path.join(path_image, name)
        try:
            os.mkdir(path_image)
        except:
            continue

        [save_image(image, path_image, index)
         for index, image in enumerate(images)]

        print('success', index)
    import shutil
    shutil.make_archive('Images', 'zip', 'Images')

    with open('Images.zip', 'rb') as file:
        bot.send_document(message.chat.id, file)
    shutil.rmtree('Images')
    os.remove('Images.zip')


bot.polling(none_stop=True, interval=0)
