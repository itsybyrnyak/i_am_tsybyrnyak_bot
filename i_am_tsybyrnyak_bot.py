import telebot
from telebot import types
import uuid
import os 
import speech_recognition as sr

language='ru_RU'
bot = telebot.TeleBot("TOKEN")
r = sr.Recognizer()

def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language=language)
            return text
        except:
            return "Sorry.. run again..."

def main_bot(msg, chatid):
    trig = True
    if 'селфи' in msg.lower():
        photofile = open('selfie.jpg', 'rb')
        bot.send_photo(chatid, photofile, 'Вид со смотровой площадки Центра семьи "Казан" в городе Казани')
        photofile.close()
        trig = False
    if 'школ' in msg.lower():
        photofile = open('school.jpg', 'rb')
        bot.send_photo(chatid, photofile)
        photofile.close()
        trig = False
    if 'gpt' in msg.lower() or 'чат' in msg.lower():
        voicefile = open('gpt.ogx', 'rb')
        bot.send_voice(chatid, voicefile)
        voicefile.close()
        trig = False
    if 'sql' in msg.lower() or 'эскьюэль' in msg.lower():
        voicefile = open('sql.ogx', 'rb')
        bot.send_voice(chatid, voicefile)
        voicefile.close()
        trig = False
    if 'любовь' in msg.lower():
        voicefile = open('flove.ogx', 'rb')
        bot.send_voice(chatid, voicefile)
        voicefile.close()
        trig = False
    if 'увлечение' in msg.lower():
        hobbymsg = open('hobby.txt', 'r', encoding='utf8').read()
        bot.send_message(chatid, hobbymsg)
        trig = False
    if trig: bot.send_message(chatid, "Запрос не распознан! \n Для справки используйте /help")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btnselfie = types.KeyboardButton(text='Последнее селфи')
    btnschool = types.KeyboardButton(text='Школьное фото')
    btnhobby = types.KeyboardButton(text='Мое увлечение')
    btngpt = types.KeyboardButton(text='ChatGPT')
    btnsql = types.KeyboardButton(text='SQL vs NoSQL')
    btnflove = types.KeyboardButton(text='Первая любовь')
    kb.add(btnselfie, btnschool, btnhobby, btngpt, btnsql, btnflove)
    himsg = open('readme.md', 'r', encoding='utf8').read()
    bot.send_message(message.chat.id, himsg, reply_markup=kb)

@bot.message_handler(commands=['source'])
def source(message):
    kbi = types.InlineKeyboardMarkup()
    btngit = types.InlineKeyboardButton(text='Github', url='https://github.com/itsybyrnyak/i_am_tsybyrnyak_bot.git')
    kbi.add(btngit)
    bot.send_message(message.chat.id, 'Исходный код:', reply_markup=kbi)

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full = "voice/" + filename + ".ogg"
    file_name_full_converted = "ready/" + filename + ".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system("ffmpeg -i " + file_name_full + "  " + file_name_full_converted)
    text = recognise(file_name_full_converted)
    main_bot(text, message.chat.id)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    main_bot(message.text, message.chat.id)

bot.infinity_polling()
