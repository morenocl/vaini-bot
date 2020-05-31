from telegram import InlineKeyboardButton
from super import add, remove, info, back, remove_this


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
        return remove_this

question_list = {
    'add': 'Que agregamos a la lista del super?',
    'remove': 'Quitemos algo',
    'info': 'Tu lista es:',
    'back': 'Saliste del super',
}

def button_func(update, context):
    id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id
    button = update.callback_query.data
    try:
        text = question_list[button]
    except KeyError:
        text = 'Elija'
    context.bot.edit_message_text(text=text, chat_id=id, message_id=message_id, reply_markup={})
    f = get_func_button(button)
    f(update, context)
