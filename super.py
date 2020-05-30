from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler
import sys


menu_super = ['add', 'remove', 'info', 'back']

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

def show_menu(update, context):
    button_list = [InlineKeyboardButton(b, callback_data=b) for b in menu_super]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    context.bot.send_message(chat_id=update.effective_chat.id, text="Diga:", reply_markup=reply_markup)

# Info handler
def back():
    del context.chat_data['state']
    context.chat_data['funcion'] = 'iii'
    context.bot.send_message(chat_id=id, text='Saliste al super')

def info(update, context):
    print('Funcion info.')
    lista, msj = '',  ''
    if len(context.user_data) != 0:
        for k in context.user_data:
            lista += str(context.user_data[k]) + ' ' + k + ',\n'
        msj = lista[:-2] + '.'
    else:
        msj = 'La lista esta vacia.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=msj)
    show_menu(update, context)
    print('context.bot_data', context.bot_data)
    print('context.chat_data', context.chat_data)
    print('context.user_data: ', context.user_data)

# Add handler
def get_cantidad(update, context):
    print('Funcion get_cantidad.')
    try:
        cant = int(update.message.text)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text='No leo numeros romanos')
    else:
        ultimo_prod = context.chat_data['ultimo']
        if cant <= 0:
            del context.user_data[ultimo_prod]
            msj = 'Eliminaste ' + ultimo_prod + '!'
        else:
            context.user_data[ultimo_prod] = cant
            msj = str(cant) + ' ' + ultimo_prod + '!'
        context.chat_data['ultimo'] = None
        context.chat_data['state'] = 'nuevo'
        context.bot.send_message(chat_id=update.effective_chat.id, text=msj)
        show_menu(update, context)
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)

def get_producto(producto, context, id):
    print('Funcion get_producto.')
    context.user_data[producto] = 1
    context.chat_data['ultimo'] = producto
    context.chat_data['state'] = 'cant'
    context.bot.send_message(chat_id=id, text='Cuantas unidades?')
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)

def add(update, context):
    print('Funcion add.')
    context.chat_data['state'] = 'prod'
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)

# Remove handler
def remove_producto(producto, context, id):
    print('Funcion remove_producto.')
    del context.user_data[producto]
    context.bot.send_message(chat_id=id, text='Eliminaste: ' + producto)
    show_menu(update, context)
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)

def remove(update, context):
    print('Funcion remove.')
    context.chat_data['state'] = 'remove'
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)

# Messajes handler (without command)
def responder_super(update, context):
    if context.chat_data['state'] == 'prod':
        get_producto(update.message.text, context, update.effective_chat.id)
    elif context.chat_data['state'] == 'cant':
        get_cantidad(update, context)
    elif context.chat_data['state'] == 'remove':
        remove_producto(update.message.text, context, update.effective_chat.id)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='No entiendo :/')

def super(update, context):
    print('Funcion super.')
    context.chat_data['state'] = 'nuevo'
    context.chat_data['funcion'] = 'super'
    show_menu(update, context)
