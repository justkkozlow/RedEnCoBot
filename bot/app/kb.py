from django.conf import settings
from django.urls import reverse
from telebot import types
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from app.models import EquipmentCategory

callback_data_values = []


def get_contact_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Отправить контакт', request_contact=True))
    return keyboard


def client_status_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(text='🙂Физическое лицо', callback_data='Физическое лицо'),
        InlineKeyboardButton(text='😎Юридическое лицо', callback_data='Юридическое лицо')
    )
    return keyboard


def client_target_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    equipment_categories = EquipmentCategory.objects.all()
    for category in equipment_categories:
        callback_data = category.title.lower()
        callback_data_values.append(callback_data)
        keyboard.add(
            InlineKeyboardButton(text=category.button_text, callback_data=callback_data)
        )
    full_catalog_callback_data = 'full_equipment_catalog'
    callback_data_values.append(full_catalog_callback_data)

    keyboard.add(
        InlineKeyboardButton(text='Хочу посмотреть всё что вы можете предложить',
                             callback_data=full_catalog_callback_data)
    )

    return keyboard


def personal_preferences_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text='Рассматриваю как дополнительный доход', callback_data='spin_off'),
        InlineKeyboardButton(text='Строю себе дом, не хочу нанимать технику', callback_data='building_for_self'),
        InlineKeyboardButton(text='Занимаюсь прокладыванием эл. сетей', callback_data='laying'),
        InlineKeyboardButton(text='Строю дома на продажу', callback_data='building_for_sale'),
        InlineKeyboardButton(text='Занимаюсь ландшафтными работами и озеленением', callback_data='landscape_works'),
        InlineKeyboardButton(text='Занимаюсь установкой септиков и прокладыванием коммуникаций',
                             callback_data='install'),
        InlineKeyboardButton(
            text='Техника нужна как подсобный рабочий. Почистить территорию от снега или погрузка/разгрузка',
            callback_data='worker'),
        InlineKeyboardButton(text='Обслуживание коммунальных сетей. Сфера ЖКХ', callback_data='service'),
        InlineKeyboardButton(text='Просто для себя/для души', callback_data='for_self'),
    )
    return keyboard


def budget_keyboard(previous_state):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text='До 600 тыс. руб.', callback_data='up_to_600t'),
        InlineKeyboardButton(text='До 1,5 млн. руб.', callback_data='up_to_1.5m'),
        InlineKeyboardButton(text='До 3 млн. руб', callback_data='up_to_3m'),
        InlineKeyboardButton(text='Не ограничен', callback_data='not_limited'),
    )
    keyboard.add(back_button(previous_state))

    return keyboard


def missing_catalog_keyboard(general_catalog, previous_state):
    markup = InlineKeyboardMarkup()
    for item in general_catalog:
        web_app_url = f'https://{settings.ALLOWED_HOSTS[0]}' + reverse('app:general-catalog-pdf-view',
                                                                       args=[item.pk])
        keyboard = InlineKeyboardButton(text='Посмотреть весь каталог', web_app=types.WebAppInfo(url=web_app_url))
        markup.add(keyboard)
    markup.add(contact_button())
    markup.add(back_button(previous_state))
    return markup


def generate_equipment_markup(equipment, previous_state):
    markup = InlineKeyboardMarkup()
    for item in equipment:
        web_app_url = f'https://{settings.ALLOWED_HOSTS[0]}' + reverse('app:equipment-pdf-view',
                                                                       args=[item.pk])
        keyboard = InlineKeyboardButton(text=item.title, web_app=types.WebAppInfo(url=web_app_url))
        markup.add(keyboard)
    markup.add(back_button(previous_state))
    return markup


def contact_button():
    text = 'Посмотреть контакт'
    callback_data = 'contact'
    button = InlineKeyboardButton(text=text, callback_data=callback_data)
    return button


def back_button_in_contact(previous_state):
    markup = InlineKeyboardMarkup()
    return markup.add(back_button(previous_state))


def back_button(previous_state):
    text = 'Назад'
    callback_data = f'back_to_{previous_state}'
    button = InlineKeyboardButton(text=text, callback_data=callback_data)
    return button
