import telebot
from django.conf import settings
from telebot import types

from app import text, kb
from app.models import Client, EquipmentCatalog, EquipmentCategory, GeneralCatalog
from app.state import UserStateManager

state_manager = UserStateManager()
state_manager.create_table()
state_manager.create_selected_category_table()
bot = telebot.TeleBot(settings.TOKEN_BOT)

equipment_categories = EquipmentCategory.objects.all()

categories = {}
for cat in equipment_categories:
    categories[cat.title.lower()] = {
        'title': cat.title,
    }


@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    try:
        client = Client.objects.get(user_id=user_id)
        client.full_name = full_name
        client.username = username
        client.save()
    except Client.DoesNotExist:
        client = Client.objects.create(user_id=user_id, full_name=full_name, username=username)
    state_manager.clear_table()
    bot.send_message(message.chat.id,
                     f'{message.from_user.first_name}, {text.CLIENT_PHONE_MESSAGE}',
                     reply_markup=kb.get_contact_keyboard())


@bot.message_handler(content_types=['contact'])
def get_personal_status(message: types.Message):
    if message.contact is not None:
        user_id = message.from_user.id
        client = Client.objects.get(user_id=user_id)
        client.contact_phone = message.contact.phone_number
        client.save()
        bot.send_message(message.chat.id,
                         text.CLIENT_STATUS_PRE_MESSAGE,
                         reply_markup=types.ReplyKeyboardRemove()
                         )
        bot.send_message(message.chat.id, text.CLIENT_STATUS_MESSAGE,
                         reply_markup=kb.client_status_keyboard())


@bot.callback_query_handler(func=lambda callback: callback.data in ['Физическое лицо', 'Юридическое лицо'])
def personal_equipment(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    client_status = callback.data
    client = Client.objects.get(user_id=user_id)
    client.client_status = client_status
    client.save()
    if callback.data in callback.data:
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                              text=text.PREFERENCES_MESSAGE, reply_markup=kb.personal_preferences_keyboard())


@bot.callback_query_handler(func=lambda callback: callback.data in text.PREFERENCES_LIST)
def personal_preferences(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    state_manager.set_user_state(user_id, 'personal_equipment')
    user_id = callback.from_user.id
    client_preferences_text = None
    preferences_keyboard = kb.personal_preferences_keyboard()
    for button_row in preferences_keyboard.keyboard:
        for button in button_row:
            if button.callback_data == callback.data:
                client_preferences_text = button.text
                break
    if client_preferences_text:
        client, created = Client.objects.get_or_create(user_id=user_id)
        client.preferences = client_preferences_text
        client.save()

    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                          text=text.WHAT_EQUIPMENT_MESSAGE, reply_markup=kb.client_target_keyboard())


@bot.callback_query_handler(func=lambda callback: callback.data in kb.callback_data_values)
def personal_tareget(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    state_manager.set_user_state(user_id, 'personal_equipment')
    previous_state = state_manager.get_user_state(user_id)
    selected_categrory = callback.data
    if callback.data == 'full_equipment_catalog':
        equipment = EquipmentCatalog.objects.all()
        markup = kb.generate_equipment_markup(equipment, previous_state)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                              text=text.CHOOSE_EQUIPMENT_MESSAGE, reply_markup=markup)
    else:
        if selected_categrory in kb.callback_data_values:
            selected_category = callback.data
            state_manager.save_user_selected_category(user_id, selected_category)

        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                              text=text.WHAT_BUDGET_MESSAGE,
                              reply_markup=kb.budget_keyboard(previous_state))


@bot.callback_query_handler(
    func=lambda callback: callback.data in ['up_to_600t', 'up_to_1.5m', 'up_to_3m', 'not_limited'])
def get_equipment(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    state_manager.set_user_state(user_id, 'perfences')
    previous_state = state_manager.get_user_state(user_id)
    selected_category = state_manager.get_user_selected_category(user_id)
    if selected_category in categories:
        category = categories[selected_category]
        title = category['title']
        equipment = EquipmentCatalog.objects.filter(card__title=title)
        if callback.data == 'up_to_600t':
            equipment = equipment.filter(price_below_600k=True)
        elif callback.data == 'up_to_1.5m':
            equipment = equipment.filter(price_below_1_5m=True)
        elif callback.data == 'up_to_3m':
            equipment = equipment.filter(price_below_3m=True)
        if equipment.exists():
            markup = kb.generate_equipment_markup(equipment, previous_state)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                  text=text.CHOOSE_EQUIPMENT_MESSAGE,
                                  reply_markup=markup)
        else:
            state_manager.set_user_state(user_id, 'perfences')
            general_catalog = GeneralCatalog.objects.all()
            markup = kb.missing_catalog_keyboard(general_catalog, previous_state)
            bot.edit_message_text(chat_id=callback.message.chat.id,
                                  message_id=callback.message.message_id,
                                  text=text.MISS_CATALOG, reply_markup=markup)

    else:
        bot.send_message(chat_id=callback.message.chat.id, text='Ошибка: неверная категория')


@bot.callback_query_handler(func=lambda callback: callback.data == 'contact')
def send_contact_info(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    state_manager.set_user_state(user_id, 'perfences')
    previous_state = state_manager.get_user_state(user_id)
    markup = kb.back_button_in_contact(previous_state)
    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                          text=text.CONTACT_MESSAGE, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('back_to_'))
def go_back(callback: types.CallbackQuery):
    previous_state = callback.data.replace('back_to_', '')
    if previous_state == 'personal_equipment':
        personal_preferences(callback)
    elif previous_state == 'perfences':
        personal_tareget(callback)
    else:
        bot.send_message(chat_id=callback.message.chat.id, text='Ошибка: невозможно вернуться назад')


if __name__ == "__main__":
    bot.polling()
