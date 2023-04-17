# Импортируем необходимые классы.
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN
from telegram import ReplyKeyboardMarkup
from translation import trns
from morphy import morph

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
reply_keyboard = [['/translate', '/donation'],
                      ['/morphology', '/pict_gen']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
current_func = 'dialog'
lang = 'en-ru'

async def start(update, context):
    await update.message.reply_text(
        "Чем могу помочь?",
        reply_markup=markup
    )
# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.


def echo(update, context):
    return update.message.text


async def help_command(update, context):
    await update.message.reply_text(
        "Я бот справочник")


async def midjourney(update, context):
    await update.message.reply_text(
        "здесь должна быть работа с картинками ai")


async def translate(update, context):
    global current_func
    current_func = 'translation-1'
    await update.message.reply_text("какие языки используем? (в формате en-ru). Пропустить: .")


async def morphology(update, context):
    global current_func
    current_func = 'morphology'
    await update.message.reply_text("введите слово или добавьте файл")


async def donation(update, context):
    await update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


async def downloader(update, context):
    file = await context.bot.get_file(update.message.document)
    await file.download_to_drive('data/trans.txt')
    await update.message.reply_text(trns(lang, file = True))
    current_func = 'morphology'



async def dialog(update, context): #заменить на болталку из прошлого бота
    global current_func, lang
    if current_func == 'dialog':
        print(update.message.text)
        await update.message.reply_text(update.message.text)
    elif current_func == 'morphology':
        print('mp:', update.message.text)
        await update.message.reply_text(morph(update.message.text))
        current_func = 'dialog'
    elif current_func == 'translation-1':
        print('lang:', update.message.text)
        await update.message.reply_text('Что перевести?')
        current_func = 'translation'
        lang = update.message.text
    elif current_func == 'translation':
        print("tr:", update.message.text)
        await update.message.reply_text(trns(update.message.text, lang))
        current_func = 'dialog'


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("morphology", morphology))
    application.add_handler(CommandHandler("donation", donation))
    application.add_handler(CommandHandler("translate", translate))
    application.add_handler(CommandHandler("midjourney", midjourney))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, dialog)
    application.add_handler(MessageHandler(filters.Document.ALL, downloader))
    application.add_handler(text_handler)  # Регистрируем обработчик в приложении.
    application.run_polling()

main()