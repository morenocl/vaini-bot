from telegram import InlineKeyboardButton
from super import add, remove, info


def back(update, context):
    print('Funcion back.')
    context.bot.send_message(text='Usaste back',\
                    chat_id=update.effective_chat.id,\
                    message_id=update.callback_query.message.message_id)

def exit(update, context):
    print('Funcion exit.')
    context.bot.send_message(text='Usaste exit',\
                    chat_id=update.effective_chat.id,\
                    message_id=update.callback_query.message.message_id)

def get_func_button(button):
    if button == 'add':
        return add
    elif button == 'remove':
        return remove
    elif button == 'info':
        return info
    elif button == 'back':
        return back
    else:
        return invalid_button

question_list = {
    'add': 'Que agregamos a la lista del super?',
    'remove': 'Que quitamos?',
    'info': 'Tu lista es:',
    'back': 'Saliste del super',
}

def button_func(update, context):
    id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id
    button = update.callback_query.data
    text = question_list[button]
    context.bot.edit_message_text(text=text, chat_id=id, message_id=message_id, reply_markup={})
    f = get_func_button(button)
    f(update, context)
