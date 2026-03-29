import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import MACHINES


def main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🔧 Запись на ТО", callback_data="type_to"))
    markup.add(InlineKeyboardButton("🛠️ Не срочный ремонт", callback_data="type_repair"))
    markup.add(InlineKeyboardButton("🚨 Критическая поломка", callback_data="type_critical"))
    return markup


def cars_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    for car in MACHINES:
        markup.add(InlineKeyboardButton(car, callback_data=f"car_{car}"))
    markup.add(InlineKeyboardButton("⬅️ В главное меню", callback_data="main_menu"))
    return markup


def back_to_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🏠 Новое обращение", callback_data="main_menu"))
    return markup