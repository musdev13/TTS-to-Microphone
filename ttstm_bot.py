import telebot
from gtts import gTTS
from pygame import mixer
import time
import sys

bot_token = sys.argv[1]
language = sys.argv[2]

bot = telebot.TeleBot(bot_token, parse_mode=None)

def speak(text):
    if text != '' and text != '/start' and text != '/ru' and text != '/uk' and text != '/en' and text != '/help' and text != '/lang':
        gTTS(text=text,lang=language, slow=False).save('text.mp3')

        mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')
        mixer.music.load('text.mp3')
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
        else:
            mixer.music.unload()

@bot.message_handler(commands=['ru'])
def ch_ru(message):
    global language
    language = 'ru'
    bot.send_message(message.chat.id, "Язык сменён на *Русский!*", "Markdown")
@bot.message_handler(commands=['uk'])
def ch_uk(message):
    global language
    language = 'uk'
    bot.send_message(message.chat.id, "Язык сменён на *Українську!*", "Markdown")
@bot.message_handler(commands=['en'])
def ch_en(message):
    global language
    language = 'en'
    bot.send_message(message.chat.id, "Язык сменён на *English!*", "Markdown")
@bot.message_handler(commands=['lang'])
def lang(message):
    global language
    bot.send_message(message.chat.id, f"Ваш Текущий язык: *{language}*", "Markdown")
@bot.message_handler(commands=['start','help'])
def help(message):
    global language
    bot.send_message(message.chat.id, "*Команды:*\n/ru - Сменить язык TTS на Русский\n/uk - Сменить язык TTS На Українську\n/en - Сменить язык TTS на English\n\n/lang - Показать текущий язык TTS\n\n*Всё остальное будет озвучиваться через ваш виртуальный микрофон!*",parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text != '' and message.text != '/start' and message.text != '/ru' and message.text != '/uk' and message.text != '/en' and message.text != '/help' and message.text != '/lang':
        bot.send_message(message.chat.id, "Говорит!")
        #print(message.text)
        speak(message.text)
        bot.send_message(message.chat.id, "Готово!")

    
bot.infinity_polling()