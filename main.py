#! /bin/python3

from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json
import os
from dotenv import load_dotenv

from super import responder_super, comandos_super


load_dotenv()
app = os.getenv('APP')
token = os.getenv('TOKEN')
entorno = os.getenv('ENTORNO')
bot = Bot(token)
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    print('Function start.')
    context.chat_data['funcion'] = 'iii'
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def super(update, context):
    print('Funcion super.')
    comandos_super(context, dispatcher, update.effective_chat.id)

super_handler = CommandHandler('super', super)
dispatcher.add_handler(super_handler)

def responder_iii(update, context):
    print('Funcion echo.')
    print(update.message.from_user.first_name + '(' + update.message.from_user.username + '): ')
    print('            ' + update.message.text)
    msj = update.message.text.replace('a', 'i').replace('e', 'i').replace('o', 'i').replace('u', 'i').replace('A', 'I').replace('E', 'I').replace('O', 'I').replace('U', 'I')
    context.bot.send_message(chat_id=update.effective_chat.id, text=msj)

def echo(update, context):
    try:
        funcion = context.chat_data['funcion']
    except KeyError:
        context.chat_data['funcion'] = 'iii'
        funcion = 'iii'

    if funcion == 'super':
        responder_super(update, context)
    elif funcion == 'iii':
        responder_iii(update, context)
    else:
        print('Funcion ninguna: ', update.message.text)


hola_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(hola_handler)

print(bot.get_me()['first_name'])

# Inicia poolling del bot.

def main():
    if entorno == 'PROD':
        updater.start_webhook(listen="0.0.0.0",
                            port=int(os.environ.get('PORT', '8443')),
                            url_path=token)
        updater.bot.set_webhook("https://" + app + ".herokuapp.com/" + token)
        updater.idle()
    elif entorno == 'DEV':
        updater.start_polling()
        updater.idle()
    else:
        print('El entorno configurado no pertenece a produccion ni desarrollo.')

if __name__ == '__main__':
    main()
