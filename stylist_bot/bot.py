import os
from dotenv import load_dotenv
from telegram import Update, Bot, ReplyKeyboardMarkup, InputMediaPhoto, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters, \
    CallbackQueryHandler
import django

from stylist_bot.config import main_keyboard, GREETING_MESSAGE, services_keyboard, questionnaire_keyboard, \
    contacts_keyboard, FREE_CONSULT_CAPTURE, MY_EMAIL, TG, FREE_CONSULT_PICTURE_URL, \
    sign_in_keyboard, SIGN_IN_TEXT, SIGN_IN_TEXT_AFTER_NAME, SIGN_IN_TEXT_BEFORE_NAME, \
    APPEARANCE_AND_STYLE_CONSULTATION_URL, APPEARANCE_AND_STYLE_CONSULTATION_CAPTURE, SORTING_WARDROBE_CAPTURE, \
    SORTING_WARDROBE_URL, CAPSULE_WARDROBE_URL, CAPSULE_WARDROBE_CAPTURE, BIG_STYLE_UPGRADE_URL, \
    BIG_STYLE_UPGRADE_CAPTURE, CHOOSING_FOR_IMPORTANT_EVENT_URL, CHOOSING_FOR_IMPORTANT_EVENT_CAPTURE, return_keyboard, \
    choose_service_buttons, CHOOSE_SERVICE_TEXT, email_and_service_keyboard, service_and_return_keyboard, \
    name_and_service_keyboard, email_keyboard, name_keyboard, name_and_email_keyboard, cancel_keyboard

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "juliyatko_bot_v2.settings")
django.setup()

from stylist_bot.models import TelegramUser, SignIn

load_dotenv()
TOKEN = os.getenv("TOKEN")

MAIN_MENU, SERVICES, CUSTOM_MENU, EMAIL_INPUT, NAME_INPUT = range(5)
END = ConversationHandler.END


def return_to_main_menu(update: Update):
    reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text("Головне меню", reply_markup=reply_markup)


def return_questionnaire_menu(update: Update):
    reply_markup = ReplyKeyboardMarkup(return_keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(text="Опис послуги 👇🏻", reply_markup=reply_markup)
    photo_url = FREE_CONSULT_PICTURE_URL
    photo_caption = f"{FREE_CONSULT_CAPTURE}"
    photo_media = InputMediaPhoto(media=photo_url, caption=photo_caption)
    update.message.reply_media_group(media=[photo_media])


def return_services_menu(update: Update):
    reply_markup = ReplyKeyboardMarkup(services_keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_html(f"Ви обрали послуги", reply_markup=reply_markup)


def return_contacts_menu(update: Update):
    reply_markup = ReplyKeyboardMarkup(contacts_keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(text=f"Якщо ви обрали потрібну вам послугу та хочете записатись"
                                   f" або у вас залишились питання — напишіть мені:\n"
                                   f"\n"
                                   f"✉️ Email: {MY_EMAIL}\n"
                                   f"\n"
                                   f"📱TG: {TG}",
                              reply_markup=reply_markup)


def sign_in(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(sign_in_keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(SIGN_IN_TEXT, reply_markup=reply_markup)
    return MAIN_MENU

def cancel(update: Update):
    reply_markup = ReplyKeyboardMarkup(sign_in_keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(SIGN_IN_TEXT_BEFORE_NAME, reply_markup=reply_markup)
    return MAIN_MENU



def name(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(cancel_keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(SIGN_IN_TEXT_BEFORE_NAME, reply_markup=reply_markup)
    return NAME_INPUT


def user_instance_existence_with_name(update: Update, user_instance: SignIn):
    if not user_instance.email and not user_instance.service_choice:
        reply_markup = ReplyKeyboardMarkup(email_and_service_keyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text(text=f"Дякую {user_instance.full_name}", reply_markup=reply_markup)
        return MAIN_MENU
    if user_instance.email and not user_instance.service_choice:
        reply_markup = ReplyKeyboardMarkup(service_and_return_keyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text(text=f"Дякую {user_instance.full_name}.", reply_markup=reply_markup)
        return MAIN_MENU
    if user_instance.service_choice and not user_instance.email:
        reply_markup = ReplyKeyboardMarkup(email_keyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text(text=f"Дякую {user_instance.full_name}.", reply_markup=reply_markup)
        return MAIN_MENU
    if user_instance.service_choice and user_instance.email:
        #TODO update text "You all set thank u"
        reply_markup = ReplyKeyboardMarkup(services_keyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text(text=f"Дякую, ви зареэструвались. Я з вами зв'яжусь.{user_instance.full_name}.", reply_markup=reply_markup)
        return MAIN_MENU

def leave_name(update, context):

    tg_id = update.effective_user.id
    tg_username = update.effective_user.username
    full_name = update.message.text
    email = None
    if full_name == "Відмінити":
        return sign_in(update, context)

    try:
        user_instance = SignIn.objects.get(tg_username=tg_username)
        user_instance.full_name = full_name
        user_instance.save()
        return user_instance_existence_with_name(update, user_instance)
    except SignIn.DoesNotExist:
        user_instance = SignIn(tg_username=tg_username, full_name=full_name, tg_id=tg_id)
        user_instance.save()
        return user_instance_existence_with_name(update, user_instance)
    return MAIN_MENU


def email(update, context):
    reply_markup = ReplyKeyboardMarkup(cancel_keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(text=SIGN_IN_TEXT_AFTER_NAME, reply_markup=reply_markup)
    return EMAIL_INPUT

def user_instance_existence_with_email(update: Update, user_instance: SignIn):
    if not user_instance.full_name and not user_instance.service_choice:
        reply_markup = ReplyKeyboardMarkup(name_and_service_keyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text(text=f"Дякую, ваш email: {user_instance.email}", reply_markup=reply_markup)
        return MAIN_MENU
    if user_instance.full_name and not user_instance.service_choice:
        reply_markup = ReplyKeyboardMarkup(service_and_return_keyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text(text=f"Дякую, ваш email: {user_instance.email}.", reply_markup=reply_markup)
        return MAIN_MENU
    if user_instance.service_choice and not user_instance.full_name:
        reply_markup = ReplyKeyboardMarkup(name_keyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text(text=f"Дякую, ваш email: {user_instance.email}.", reply_markup=reply_markup)
        return MAIN_MENU
    if user_instance.service_choice and user_instance.full_name:
        #TODO update text "You all set"
        reply_markup = ReplyKeyboardMarkup(services_keyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text(text=f"Дякую, ваш email: {user_instance.email}. Ви зареэструвались. Я з вами зв'яжусь.", reply_markup=reply_markup)
        return MAIN_MENU

def leave_email(update, context):
    tg_id = update.effective_user.id
    tg_username = update.effective_user.username
    email = update.message.text
    full_name = None
    if email == "Відмінити":
        return sign_in(update, context)

    try:
        user_instance = SignIn.objects.get(tg_username=tg_username)
        user_instance.email = email
        user_instance.save()
        return user_instance_existence_with_email(update, user_instance)

    except SignIn.DoesNotExist:
        user_instance = SignIn(tg_username=tg_username, email=email, full_name=full_name, tg_id=tg_id)
        user_instance.save()
        return user_instance_existence_with_email(update, user_instance)

    return MAIN_MENU


def send_info(update: Update, service_url, service_capture):
    photo_url = service_url
    photo_caption = f"{service_capture}"
    photo_media = InputMediaPhoto(media=photo_url, caption=photo_caption)
    update.message.reply_media_group(media=[photo_media])


def appearance_and_style_consultation(update: Update):
    reply_markup = ReplyKeyboardMarkup(return_keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(text="Опис послуги 👇🏻", reply_markup=reply_markup)
    return send_info(update, APPEARANCE_AND_STYLE_CONSULTATION_URL, APPEARANCE_AND_STYLE_CONSULTATION_CAPTURE)


def wardrobe_analysis(update: Update):
    reply_markup = ReplyKeyboardMarkup(return_keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(text="Опис послуги 👇🏻", reply_markup=reply_markup)
    return send_info(update, SORTING_WARDROBE_URL, SORTING_WARDROBE_CAPTURE)


def capsule_wardrobe(update: Update):
    reply_markup = ReplyKeyboardMarkup(return_keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(text="Опис послуги 👇🏻", reply_markup=reply_markup)
    return send_info(update, CAPSULE_WARDROBE_URL, CAPSULE_WARDROBE_CAPTURE)


def big_style_upgrade(update: Update):
    reply_markup = ReplyKeyboardMarkup(return_keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(text="Опис послуги 👇🏻", reply_markup=reply_markup)
    return send_info(update, BIG_STYLE_UPGRADE_URL, BIG_STYLE_UPGRADE_CAPTURE)


def important_event(update: Update):
    reply_markup = ReplyKeyboardMarkup(return_keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(text="Опис послуги 👇🏻", reply_markup=reply_markup)
    return send_info(update, CHOOSING_FOR_IMPORTANT_EVENT_URL, CHOOSING_FOR_IMPORTANT_EVENT_CAPTURE)


def choose_service(update: Update):
    reply_markup = InlineKeyboardMarkup(choose_service_buttons, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(CHOOSE_SERVICE_TEXT, reply_markup=reply_markup)
    return MAIN_MENU


def check_instance_existence(query: str, tg_username, tg_id, text: str):
    try:
        sign_in_instance = SignIn.objects.get(tg_username=tg_username)
        sign_in_instance.service_choice = text
        sign_in_instance.save()
        if sign_in_instance.full_name and sign_in_instance.email:
            #TODO update text "You all set"
            reply_markup = ReplyKeyboardMarkup(services_keyboard, resize_keyboard=True, one_time_keyboard=False)
            query.message.reply_text(text=f"Ви обрали послугу: {sign_in_instance.service_choice}", reply_markup=reply_markup)
            return MAIN_MENU
        if sign_in_instance.full_name and not sign_in_instance.email:
            reply_markup = ReplyKeyboardMarkup(email_keyboard, resize_keyboard=True, one_time_keyboard=False)
            query.message.reply_text(text=f"Ви обрали послугу: {sign_in_instance.service_choice}", reply_markup=reply_markup)
            return MAIN_MENU
        if not sign_in_instance.full_name and sign_in_instance.email:
            reply_markup = ReplyKeyboardMarkup(name_keyboard, resize_keyboard=True, one_time_keyboard=False)
            query.message.reply_text(text=f"Ви обрали послугу: {sign_in_instance.service_choice}", reply_markup=reply_markup)
        return MAIN_MENU

    except SignIn.DoesNotExist:
        sign_in_instance = SignIn(tg_id=tg_id, tg_username=tg_username, service_choice=text)
        sign_in_instance.save()
        reply_markup = ReplyKeyboardMarkup(name_and_email_keyboard, resize_keyboard=True, one_time_keyboard=False)
        query.message.reply_text(text=f"You need to feel email and name", reply_markup=reply_markup)
        return MAIN_MENU


def handle_inline_button(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    tg_username = update.effective_user.username
    tg_id = update.effective_user.id

    if data == 'consultation':
        return check_instance_existence(query, tg_username, tg_id, "Консультація по лініях зовнішності та стилю")

    elif data == "wardrobe_analysis":
        return check_instance_existence(query, tg_username, tg_id, "Розбір гардероба")

    elif data == "capsule_wardrobe":
        return check_instance_existence(query, tg_username, tg_id, "Капсульний гардероб")

    elif data == "wardrobe_update":
        return check_instance_existence(query, tg_username, tg_id, "Оновлений гардероб")

    elif data == "free_consultation":
        return check_instance_existence(query, tg_username, tg_id, "Безплатна консультація")

    elif data == "event_outfit":
        return check_instance_existence(query, tg_username, tg_id, "Підбір образу на важливу подію чи зйомку")

    query.answer()

    # You can also edit the message if needed
    # query.edit_message_text(text="You selected: " + data)

    return MAIN_MENU


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = user.id
    username = user.username

    telegram_user, created = TelegramUser.objects.get_or_create(
        user_id=user_id,
        defaults={'username': username}
    )
    reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True, one_time_keyboard=False)

    update.message.reply_html(f"Вітаю {user.mention_html()}, {GREETING_MESSAGE}", reply_markup=reply_markup)

    return menu(update, context)


def menu(update: Update, context: CallbackContext):
    message = update.message.text

    if message == "Послуги та вартість":
        return_services_menu(update)
    elif message == "Контакти":
        return_contacts_menu(update)
    elif message == "Безплатна консультація":
        return_questionnaire_menu(update)
    elif message == "Записатись":
        return sign_in(update, context)
    elif message == "👤 Ім'я":
        return name(update, context)
    elif message == "📩 Email":
        return email(update, context)
    elif message == "Консультація по лініях зовнішності та стилю":
        appearance_and_style_consultation(update)
    elif message == "Розбір гардероба":
        wardrobe_analysis(update)
    elif message == "Капсульний гардероб":
        return capsule_wardrobe(update)
    elif message == "Оновлений гардероб":
        return big_style_upgrade(update)
    elif message == "Підбір образу на важливу подію чи зйомку":
        return important_event(update)
    elif message == "Обрати послугу і записатись":
        return sign_in(update, context)
    elif message == "Обрати послугу":
        return choose_service(update)
    elif message == "Відмінити":
        return cancel(update)
    elif message == "👈🏻 Повернутись до головного меню":
        return_to_main_menu(update)
    elif message == "👈🏻 Повернутись":
        return_services_menu(update)

    return MAIN_MENU


def start_bot():
    bot = Bot(token=TOKEN)
    updater = Updater(bot=bot, use_context=True)
    dispatcher = updater.dispatcher

    menu_conversation_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text & ~Filters.command, menu)],
        states={
            MAIN_MENU: [MessageHandler(Filters.text & ~Filters.command, menu)],
            NAME_INPUT: [MessageHandler(Filters.text, leave_name)],
            EMAIL_INPUT: [MessageHandler(Filters.text, leave_email)],
        },
        fallbacks=[
            MessageHandler(Filters.regex('^(Ім\'я)$'), name),
            MessageHandler(Filters.regex('^(Email)$'), email)
        ]
    )

    dispatcher.add_handler(CallbackQueryHandler(handle_inline_button))

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(menu_conversation_handler)


    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    start_bot()