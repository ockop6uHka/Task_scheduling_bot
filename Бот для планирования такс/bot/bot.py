import telebot
from database.db import add_task, get_all_tasks, delete_task_by_id, delete_all_tasks

bot = telebot.TeleBot('Your Token')


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет! Я бот для управления задачами. Чтобы добавить задачу, используй команду /add. "
                              "Чтобы посмотреть список задач, используй команду /list. "
                              "Чтобы удалить задачу, используй команду /delete. "
                              "Чтобы удалить все задачи, используй команду /delete_all.")


@bot.message_handler(commands=['add'])
def add(message):
    bot.send_message(message.chat.id, "Добавьте описание задачи")
    bot.register_next_step_handler(message, process_add_task)


def process_add_task(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if text:
        try:
            add_task(text)
            bot.send_message(chat_id, f"Задача '{text}' успешно добавлена.")
        except Exception as Er:
            bot.send_message(chat_id, "Ошибка при добавлении задачи.")
            print(Er)
    else:
        bot.send_message(chat_id, "Пожалуйста, укажите корректное описание задачи.")

@bot.message_handler(commands=['list'])
def list_tasks(message):
    chat_id = message.chat.id
    try:
        tasks = get_all_tasks()
        if tasks:
            tasks_text = "Список задач:\n"
            for task in tasks:
                tasks_text += f"{task.id} {task.description} {str(task.created_at)[:str(task.created_at).find('.')]}\n"
            bot.send_message(chat_id, tasks_text)
        else:
            bot.send_message(chat_id, "Список задач пуст.")
    except Exception as Er:
        bot.send_message(chat_id, "Ошибка при получении списка задач.")
        print(Er)


@bot.message_handler(commands=['delete'])
def delete(message):
    bot.send_message(message.chat.id, "Введите номер задачи, которую хотите удалить")

    bot.register_next_step_handler(message, process_task_id_input)


def process_task_id_input(message):
    try:
        task_id = int(message.text)

        if delete_task_by_id(task_id):
            bot.send_message(message.chat.id, f"Задача с id {task_id} успешно удалена.")
        else:
            bot.send_message(message.chat.id, f"Задача с id {task_id} не найдена.")
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный формат id задачи.")


@bot.message_handler(commands=['delete_all'])
def delete_all(message):
    chat_id = message.chat.id
    try:
        delete_all_tasks()
        bot.send_message(chat_id, "Все задачи успешно удалены.")
    except Exception as Er:
        bot.send_message(chat_id, "Ошибка при удалении всех задач.")
        print(Er)


bot.polling(none_stop=True, timeout=20)






