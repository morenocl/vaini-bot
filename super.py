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
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=4))
    context.bot.send_message(chat_id=update.effective_chat.id, text="Diga:", reply_markup=reply_markup)

def get_items_from_context(context, _id):
    try:
        lista = context.user_data[_id]
    except KeyError:
        context.user_data[_id] = {}
        lista = context.user_data[_id]
    items = []
    for k in lista:
        items.append(str(k))
    return items

def show_button_remover(update, context):
    _id = str(update.effective_chat.id)
    items = get_items_from_context(context, _id)
    print('Lista de botones: ', items)
    if not items:
        message_id = update.callback_query.message.message_id
        context.bot.edit_message_text(text="Primero debe agregar.", chat_id=int(id), message_id=message_id, reply_markup={})
    else:
        button_list = [InlineKeyboardButton(b, callback_data=b) for b in items]
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Elija",reply_markup=reply_markup)

def back(update, context):
    _id = str(update.effective_chat.id)
    del context.chat_data[_id]['state']
    context.chat_data[_id]['funcion'] = 'iii'

def info(update, context):
    print('Funcion info.')
    _id = str(update.effective_chat.id)
    try:
        print('User data en info: ', context.user_data)
        user_data = context.user_data[_id]
    except KeyError:
        context.user_data[_id] = {}
        user_data = context.user_data[_id]

    lista, msj = '',  ''
    if len(user_data) != 0:
        for k in context.user_data[_id]:
            lista += str(context.user_data[_id][k]) + ' ' + k + ',\n'
        msj = lista[:-2] + '.'
    else:
        msj = 'La lista esta vacia.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=msj)
    show_menu(update, context)

# Add handler
def get_cantidad(update, context):
    print('Funcion get_cantidad.')
    _id = str(update.effective_chat.id)
    try:
        cant = int(update.message.text)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text='No leo numeros romanos')
    else:
        ultimo_prod = context.chat_data[_id]['ultimo']
        if cant <= 0:
            del context.user_data[_id][ultimo_prod]
            msj = 'Eliminaste ' + ultimo_prod + '!'
        else:
            context.user_data[_id][ultimo_prod] = cant
            msj = str(cant) + ' ' + ultimo_prod + '!'
        context.chat_data[_id]['ultimo'] = None
        context.chat_data[_id]['state'] = 'nuevo'
        context.bot.send_message(chat_id=update.effective_chat.id, text=msj)
        show_menu(update, context)
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)

def get_producto(producto, context, id):
    print('Funcion get_producto.')
    _id = str(id)
    try:
        lista = context.user_data[_id]
        chat = context.chat_data[_id]
    except:
        context.user_data[_id] = {}
        lista = context.user_data[_id]
        context.chat_data[_id] = {}
        chat = context.chat_data[_id]
    lista[producto] = 1
    chat['ultimo'] = producto
    chat['state'] = 'cant'
    context.bot.send_message(chat_id=id, text='Cuantas unidades?')
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)

def add(update, context):
    print('Funcion add.')
    _id = str(update.effective_chat.id)
    context.chat_data[_id]['state'] = 'prod'
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)

# Remove handler
def remove_producto(update, context):
    print('Funcion remove_producto.')
    _id = str(update.effective_chat.id)
    del context.user_data[_id][update.message.text]
    context.bot.send_message(chat_id=update.effective_chat.id, text='Eliminaste: ' + update.message.text)
    show_menu(update, context)
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)

def remove_this(update, context):
    print('Funcion remove_producto.')
    item = button = update.callback_query.data
    _id = str(update.effective_chat.id)
    del context.user_data[_id][item]
    context.bot.send_message(chat_id=update.effective_chat.id, text='Eliminaste: ' + item)
    show_menu(update, context)
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)


def remove(update, context):
    print('Funcion remove.')
    _id = str(update.effective_chat.id)
    context.chat_data[_id]['state'] = 'remove'
    show_button_remover(update, context)
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)

# Messajes handler (without command)
def responder_super(update, context):
    _id = str(update.effective_chat.id)
    if context.chat_data[_id]['state'] == 'prod':
        get_producto(update.message.text, context, update.effective_chat.id)
    elif context.chat_data[_id]['state'] == 'cant':
        get_cantidad(update, context)
    elif context.chat_data[_id]['state'] == 'remove':
        remove_producto(update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='No entiendo :/')

def super(update, context):
    print('Funcion super.')
    print(type(context.user_data))
    print(type(context.chat_data))
    _id = str(update.effective_chat.id)
    try:
        chat_data = context.chat_data[_id]
    except:
        context.chat_data[_id] = {}
        chat_data = context.chat_data[_id]
    try:
        user_data = context.user_data[_id]
    except:
        context.user_data[_id] = {}
        user_data = context.user_data[_id]

    chat_data['state'] = 'nuevo'
    chat_data['funcion'] = 'super'
    show_menu(update, context)
