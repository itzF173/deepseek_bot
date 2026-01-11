import telebot
import requests
from supabase import create_client
from datetime import datetime
#1 eng = 0.3 token
#1m tokens = 0.42$
supabase = create_client(
    "https://witesqdiflxmnsxebrig.supabase.co",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdGVzcWRpZmx4bW5zeGVicmlnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjYzMjgzMDQsImV4cCI6MjA4MTkwNDMwNH0.QdHeB6ZbOt-IpA43Nchy5p6d2onv05pPb1XOj24OjW8"
)

TOKEN = "8244416237:AAHezGXRITlbKHsNQXFJIFWG2dNheB8gR70"
bot = telebot.TeleBot(TOKEN)
API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_KEY = "sk-06d469e0b76e41929d9fb8081b188907"#"sk-30e22cb3ff8e43cba5a0880105d431dc"

MAX_TOKENS = 300
user_usage = {}
def check_daily_limit(user_id):
    #Проверка лимита запросов в день
    today = datetime.now().date().isoformat()

    # Впервые зашел в бота
    if user_id not in user_usage:
        user_usage[user_id] = {'date': today, 'count': 1}
        return True
    # Если наступил след. день. сбросить лимит запросов
    if user_usage[user_id]['date'] != today:
        user_usage[user_id] = {'date': today, 'count': 1}
        return True

    # Если лимит исчерпан
    if user_usage[user_id]['count'] >= 10:  # Максимум 10 вопросов в день
        return False

    user_usage[user_id]['count'] += 1
    return True
def askDeepseek(question):
    """Запрос к DeepSeek API с оптимизацией токенов"""

    # Обрезаем вопрос если слишком длинный
    if len(question) > 300:
        question = question[:300] + "..."

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "Ты полезный помощник. Отвечай максимально кратко и по делу. Ограничь ответ 3-4 предложениями. Используй не больне 600 букв в ответе"
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "max_tokens": MAX_TOKENS,  # Экономим токены
        "temperature": 0.5,  # Уменьшил температуру для более предсказуемых ответов
        "stream": False
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"Ошибка API: {response.status_code}, {response.text}")
            return f"Ошибка: {response.status_code}. Попробуйте позже."

    except requests.exceptions.Timeout:
        return "Время ожидания истекло. Попробуйте снова."
    except Exception as e:
        print(f"Ошибка в askDeepseek: {e}")
        return "Произошла ошибка при обработке запроса."


@bot.message_handler(commands=['ai'])
def deepseekSearch(message):
    """Обработчик команды /ai"""
    user_id = message.from_user.id

    # Проверяем лимит
    if not check_daily_limit(user_id):
        bot.send_message(
            message.chat.id,
            "❌ Вы превысили дневной лимит в 10 вопросов. Попробуйте завтра!"
        )
        return

    # Получаем вопрос
    user_question = message.text.replace("/ai", "").strip()

    if not user_question:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, напишите вопрос после команды /ai\nПример: /ai Что такое ИИ?"
        )
        return

    # Отправляем статус "печатает"
    bot.send_chat_action(message.chat.id, 'typing')

    # Получаем ответ от DeepSeek
    deepseekAnswer = askDeepseek(user_question)

    # Отправляем ответ
    bot.send_message(message.chat.id, deepseekAnswer)


@bot.message_handler(commands=['start'])
def start(message):

    welcome_text = "Привет"
    bot.send_message(message.chat.id, welcome_text)
# @bot.message_handler(commands=['start'])
# def start(message):
#
#     user = message.from_user
#     print(user.first_name)
#     print(user.username)
#     print(user.id)
#     supabase.table("users").insert({
#         'telegram_id': user.id,
#         'username': user.username,
#         'first_name': user.first_name
#     }).execute()
#
#     bot.send_message(message.chat.id, "Its a finance traker")


bot.infinity_polling()





# message = {
#     'message_id': 123,
#     'chat': {
#         'id': 123456789,  # ID чата
#         'type': 'private'
#     },
#     'from': {  # <-- Вот откуда from_user!
#         'id': 987654321,      # telegram_id пользователя
#         'is_bot': False,
#         'first_name': 'Иван',
#         'last_name': 'Иванов',
#         'username': 'ivan_ivanov',
#         'language_code': 'ru'
#     },
#     'date': 1705312800,
#     'text': '/start'
# }