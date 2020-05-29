from telegram.ext import CommandHandler
import sys


# handlers
add_handler = None
remove_handler = None
info_handler = None

# Info handler
def info(update, context):
    print('Funcion info.')
    lista, msj = '',  ''
    if len(context.user_data) != 0:
        for k in context.user_data:
            lista += str(context.user_data[k]) + ' ' + k + ',\n'
        msj = 'Tu lista:\n' + lista[:-2] + '.'
    else:
        msj = 'La lista esta vacia.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=msj)
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
        context.user_data[ultimo_prod] = cant
        context.chat_data['ultimo'] = None
        context.chat_data['state'] = 'nuevo'
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(cant) + ' ' + ultimo_prod + '!')
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)

def get_producto(producto, context, id):
    print('Funcion get_producto.')
    context.user_data[producto] = 1
    context.chat_data['ultimo'] = producto
    context.chat_data['state'] = 'cant'
    context.bot.send_message(chat_id=id, text='Agregaste: '+producto+' x1. Mas de uno?')
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)

def add(update, context):
    print('Funcion add.')
    if len(context.args) == 0:
        context.chat_data['state'] = 'prod'
        context.bot.send_message(chat_id=update.effective_chat.id, text='Que agregamos a la lista del super?')
    else:
        producto = ' '.join(context.args)
        get_producto(producto, context, update.effective_chat.id)
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)

# Remove handler
def remove_producto(producto, context, id):
    print('Funcion remove_producto.')
    del context.user_data[producto]
    context.bot.send_message(chat_id=id, text='Eliminaste: ' + producto)
    print('chat: ', context.chat_data)
    print('user: ', context.user_data)

def remove(update, context):
    print('Funcion remove.')
    if len(context.args) == 0:
        context.chat_data['state'] = 'remove'
        context.bot.send_message(chat_id=update.effective_chat.id, text='Que quitamos?')
    else:
        producto = ' '.join(context.args)
        remove_producto(producto, context, update.effective_chat.id)
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

# Manage commands of super
def agregar_comandos_super(dispatcher):
    global add_handler, remove_handler, info_handler
    add_handler = CommandHandler('add', add)
    dispatcher.add_handler(add_handler)
    remove_handler = CommandHandler('remove', remove)
    dispatcher.add_handler(remove_handler)
    info_handler = CommandHandler('info', info)
    dispatcher.add_handler(info_handler)

def quitar_comandos_super(dispatcher):
    dispatcher.remove_handler(add_handler)
    dispatcher.remove_handler(remove_handler)
    dispatcher.remove_handler(info_handler)

def comandos_super(context, dispatcher, id):
    if context.chat_data['funcion'] == 'super':
        del context.chat_data['state']
        context.chat_data['funcion'] = 'iii'
        quitar_comandos_super(dispatcher)
        context.bot.send_message(chat_id=id, text='Saliste al super')
    else:
        context.chat_data['state'] = 'nuevo'
        context.chat_data['funcion'] = 'super'
        agregar_comandos_super(dispatcher)
        context.bot.send_message(chat_id=id, text='Entraste al super')
