import json
import os
from telebot import TeleBot, types
from dotenv import load_dotenv

load_dotenv()
bot = TeleBot(os.getenv("TOKEN"))
with open("database/strings.json", "r", encoding="utf-8") as file:
    strings = json.load(file)

global language, service, contact
language = "uz"
service = None
contact = None
contact_2 = None

@bot.message_handler(commands=["start"])
def register(message):
    print(str(message.chat.id))
    with open("database/base.json", "r", encoding="utf-8") as file:
        users = json.load(file)
    is_db = True
    for user in users:
        if user['id'] == message.chat.id:
            is_db = False
            break
    if is_db:
        users.append({
            'id': message.chat.id,
            'first_name': message.chat.first_name,
            'last_name': message.chat.last_name,
            'phone_number': None,
            'phone_number_2': None
        })
    with open("database/base.json", "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)
    text = strings[language]["start_message"]
    keyboard = types.ReplyKeyboardMarkup(True, row_width=2)
    services = strings[language]['services']
    for i in range(0, len(services), 2):
        if i == len(services) - 1:
            keyboard.row(
                types.KeyboardButton(services[i]))
        else:
            keyboard.row(
                types.KeyboardButton(services[i]),
                types.KeyboardButton(services[i + 1])
            )
    bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode="HTML")


@bot.message_handler(content_types=["text"])
def message_handler(message):
    global language, service, contact, contact_2

    if message.text in strings['uz']['services']:
        service = message.text
        index = strings['uz']['services'].index(message.text)
        text = {strings['uz']['services_reply_message'][index]}
        keyboard = types.ReplyKeyboardMarkup(True).add(
            types.KeyboardButton(strings['uz']['phone_number_button'], request_contact=True)
        )
        bot.send_message(message.chat.id, text)
        text = strings['uz']['phone_number_message']
        bot.send_message(message.chat.id, text, reply_markup=keyboard)

    elif message.text == strings['uz']['no_phone_number_button']:
        text = strings[language]['result_message']
        keyboard = types.ReplyKeyboardMarkup(True).add(
            types.KeyboardButton(strings[language]['mainmenu_button'])
        )
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
        handler_message = strings[language]['handler_message']
        text = f"<b>{handler_message[0]}</b>{message.chat.first_name}\n<b>{handler_message[1]}</b>{message.chat.last_name}\n<b>{handler_message[2]}</b>{service}\n<b>{handler_message[3]}</b>{contact}"
        bot.send_message(os.getenv("CHAT_ID"), text, parse_mode="HTML")
        contact = None

    elif message.text == strings['uz']['mainmenu_button']:
        text = strings['uz']['start_message']
        keyboard = types.ReplyKeyboardMarkup(True, row_width=2)
        services = strings[language]['services']
        for i in range(0, len(services), 2):
            keyboard.row(
                types.KeyboardButton(services[i]),
                types.KeyboardButton(services[i + 1])
            )
        bot.send_message(message.chat.id, text, reply_markup=keyboard)

    else:
        with open("database/base.json", "r", encoding="utf-8") as file:
            users = json.load(file)
        for i in range(len(users)):
            if users[i]['id'] == message.chat.id:
                if contact is None:
                    users[i]['phone_number'] = message.text
                    contact = message.text
                    text = strings[language]['other_phone_number_message']
                    keyboard = types.ReplyKeyboardMarkup(True).add(
                        types.KeyboardButton(strings[language]['no_phone_number_button'])
                    )
                    bot.send_message(message.chat.id, text, reply_markup=keyboard)
                else:
                    users[i]['phone_number_2'] = message.text
                    contact_2 = message.text
                    text = strings[language]['result_message']
                    keyboard = types.ReplyKeyboardMarkup(True).add(
                        types.KeyboardButton(strings[language]['mainmenu_button'])
                    )
                    bot.send_message(message.chat.id, text, reply_markup=keyboard)
                    handler_message = strings[language]['handler_message']
                    text = f"<b>{handler_message[0]}</b>{message.chat.first_name}\n<b>{handler_message[1]}</b>{message.chat.last_name}\n<b>{handler_message[2]}</b>{service}\n<b>{handler_message[3]}</b>{contact}\n<b>{handler_message[4]}</b>{contact_2}"
                    bot.send_message(os.getenv("CHAT_ID"), text, parse_mode="HTML")
                    contact = None
                    contact_2 = None
                break
        with open("database/base.json", "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4, ensure_ascii=False)


@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    global language, service, contact, contact_2
    with open("database/base.json", "r", encoding="utf-8") as file:
        users = json.load(file)
    for i in range(len(users)):
        if users[i]['id'] == message.chat.id:
            users[i]['phone_number'] = message.contact.phone_number
            contact = message.contact.phone_number
            text = strings[language]['other_phone_number_message']
            keyboard = types.ReplyKeyboardMarkup(True).add(
                types.KeyboardButton(strings[language]['no_phone_number_button'])
            )
            bot.send_message(message.chat.id, text, reply_markup=keyboard)
            break
    with open("database/base.json", "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)
    handler_message = strings[language]['handler_message']
    text = f"<b>{handler_message[0]}</b>{message.chat.first_name}\n<b>{handler_message[1]}</b>{message.chat.last_name}\n<b>{handler_message[2]}</b>{service}\n<b>{handler_message[3]}</b>{contact}"
    bot.send_message(os.getenv("CHAT_ID"),text, parse_mode="HTML")


bot.polling(True)
