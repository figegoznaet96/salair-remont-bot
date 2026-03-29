import telebot
from telebot.types import Message, CallbackQuery
from datetime import datetime

from config import TOKEN, MECHANIC_ID, LOGIST_IDS, logger, MACHINES
from keyboards import main_menu, cars_keyboard, back_to_menu

bot = telebot.TeleBot(TOKEN)

user_state = {}
user_data = {}


@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    user_state[chat_id] = "waiting_car"
    user_data[chat_id] = {}
    bot.send_message(
        chat_id,
        "👋 Добро пожаловать, водитель!\n\nСначала выберите свою машину:",
        reply_markup=cars_keyboard()
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: CallbackQuery):
    chat_id = call.message.chat.id
    data = call.data

    if data == "main_menu":
        user_state[chat_id] = "waiting_car"
        user_data[chat_id] = {}
        bot.edit_message_text(
            "👋 Добро пожаловать, водитель!\n\nСначала выберите свою машину:",
            chat_id, call.message.message_id,
            reply_markup=cars_keyboard()
        )
        return

    if data.startswith("car_"):
        car = data[4:]
        user_data[chat_id]["car"] = car
        bot.edit_message_text(
            f"✅ Машина выбрана: <b>{car}</b>\n\nТеперь выберите тип заявки:",
            chat_id, call.message.message_id,
            parse_mode="HTML"
        )
        bot.send_message(chat_id, "Выберите тип заявки:", reply_markup=main_menu())
        return

    if data.startswith("type_"):
        if data == "type_to":
            user_state[chat_id] = "waiting_mileage"
            user_data[chat_id]["type"] = "Запись на ТО"
            bot.edit_message_text("Укажите текущий пробег (только цифры):", chat_id, call.message.message_id)
        elif data == "type_repair":
            user_state[chat_id] = "waiting_description"
            user_data[chat_id]["type"] = "Не срочный ремонт"
            bot.edit_message_text("Опишите поломку:", chat_id, call.message.message_id)
        elif data == "type_critical":
            user_state[chat_id] = "waiting_description"
            user_data[chat_id]["type"] = "Критическая поломка"
            bot.edit_message_text(
                "⚠️ <b>ВНИМАНИЕ!</b>\nАвтомобиль НЕ МОЖЕТ продолжить движение.\n\nОпишите поломку подробно:",
                chat_id, call.message.message_id, parse_mode="HTML"
            )

    bot.answer_callback_query(call.id)


@bot.message_handler(content_types=['text'])
def handle_text(message: Message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)

    if state == "waiting_mileage":
        if message.text.isdigit():
            user_data[chat_id]["mileage"] = message.text
            user_state[chat_id] = "waiting_city"
            bot.send_message(chat_id, "Напишите название ближайшего города или сервиса:")
        else:
            bot.send_message(chat_id, "❗ Введите только цифры!")

    elif state == "waiting_description":
        user_data[chat_id]["description"] = message.text
        user_state[chat_id] = "waiting_city"
        bot.send_message(chat_id, "Напишите название ближайшего города или сервиса:")

    elif state == "waiting_city":
        user_data[chat_id]["city"] = message.text.strip()
        user_data[chat_id]["photos"] = []           # список для нескольких фото
        user_state[chat_id] = "waiting_photo"

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("Готово", "Без фото")
        bot.send_message(
            chat_id,
            "📸 Прикрепите фото к заявке (можно несколько).\n"
            "Когда закончите — нажмите «Готово» или «Без фото»:",
            reply_markup=markup
        )

    # Обработка кнопок "Готово" и "Без фото"
    elif state == "waiting_photo":
        if message.text in ["Готово", "Без фото"]:
            user_data[chat_id]["photo"] = user_data[chat_id]["photos"] if user_data[chat_id]["photos"] else None
            send_application(chat_id, message)
        else:
            bot.send_message(chat_id, "Нажмите «Готово» или «Без фото»")

    else:
        bot.send_message(chat_id, "Пожалуйста, используйте кнопки 👇", reply_markup=cars_keyboard())


@bot.message_handler(content_types=['photo'])
def handle_photo(message: Message):
    chat_id = message.chat.id
    if user_state.get(chat_id) == "waiting_photo":
        photo_id = message.photo[-1].file_id
        user_data[chat_id]["photos"].append(photo_id)
        count = len(user_data[chat_id]["photos"])
        bot.send_message(chat_id, f"✅ Фото добавлено ({count} шт.)")


def send_application(chat_id, message):
    d = user_data[chat_id]
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    text = f"🚨 НОВАЯ ЗАЯВКА\n\nТип: {d['type']}\n"
    text += f"Водитель: @{message.from_user.username or 'без_юзернейма'} (ID: {message.from_user.id})\n"
    text += f"Машина: {d.get('car', 'Не выбрана')}\n"
    text += f"Город: {d['city']}\n"
    if "mileage" in d:
        text += f"Пробег: {d['mileage']} км\n"
    if "description" in d:
        text += f"Описание: {d['description']}\n"
    text += f"\nОтправлено: {now}"

    # Отправка админам
    for admin_id in [MECHANIC_ID] + LOGIST_IDS:
        try:
            if d.get("photo"):
                for i, photo_id in enumerate(d["photo"]):
                    if i == 0:
                        bot.send_photo(admin_id, photo_id, caption=text)
                    else:
                        bot.send_photo(admin_id, photo_id)
            else:
                bot.send_message(admin_id, text)
        except Exception as e:
            logger.error(f"Ошибка отправки: {e}")

    # Подтверждение водителю
    bot.send_message(
        chat_id,
        "✅ Заявка успешно отправлена!\nМеханик свяжется с вами в ближайшее время.",
        reply_markup=back_to_menu()
    )
    user_state[chat_id] = None
    bot.send_message(chat_id, " ", reply_markup=telebot.types.ReplyKeyboardRemove())


if __name__ == "__main__":
    logger.info("Бот запущен!")
    bot.infinity_polling()
