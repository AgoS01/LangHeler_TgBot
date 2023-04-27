import openai
from data.users import User
from telegram.ext import CommandHandler, Application, MessageHandler, filters
from telegram import ReplyKeyboardRemove
import sqlite3
import random
from data import db_session


application = Application.builder().token(BOT_TOKEN).build()


# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
async def start(update, context):
    idtg = update.effective_message.chat_id
    db_sess = db_session.create_session()
    users = User()
    users.id = idtg
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
    )


async def help(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def dialog_run(update, context):
    """Отправляет сообщение когда получена команда /help"""
    ran = random.randint(0, 100)
    db_sess = db_session.create_session()
    users = User()
    users.context = update.message
    await update.message.reply_text(f"{ran}\tтест")


async def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    await update.message.reply_text(update.message.text)



def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("dialog", dialog_run))

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(filters.TEXT, echo)

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)
    # Запускаем приложение.
    application.run_polling()

# Зарегистрируем их в приложении перед
# регистрацией обработчика текстовых сообщений.
# Первым параметром конструктора CommandHandler я
# вляется название команды.
if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    text_handler = User()
    text_handler.context = "duewuvbeiuw"
    db_sess = db_session.create_session()
    db_sess.add(text_handler)
    db_sess.commit()
    main()