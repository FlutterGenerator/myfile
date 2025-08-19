#!/usr/bin/env python3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# Ваш API-ключ от КиноПоиск
API_KEY = "MB78FH4-30W466F-MBMYQZQ-W1MM099"

# Функция для поиска фильма на КиноПоиск
def search_movie(title):
    url = f"https://api.kinopoisk.dev/v1.3/movie?token={API_KEY}&name={title}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка успешного ответа от сервера
        data = response.json()

        if data.get('docs'):
            movie = data['docs'][0]
            movie_info = (
                f"Название: {movie['name']}\n"
                f"Год: {movie.get('year', 'Не указан')}\n"
                f"Жанры: {', '.join([genre['name'] for genre in movie.get('genres', [])])}\n"
                f"Описание: {movie.get('description', 'Нет описания')}\n"
                f"Рейтинг КиноПоиска: {movie.get('rating', {}).get('kp', 'Нет данных')}\n"
                f"Ссылка для бесплатного просмотра (с рекламой): https://www.sspoisk.ru/film/{movie['id']}/"
            )
            return movie_info
        else:
            return "Фильм не найден."

    except requests.exceptions.RequestException as e:
        return f"Ошибка при подключении к API: {e}"
    except ValueError:
        return "Не удалось обработать ответ от сервера."

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Напиши название фильма, и я найду его на КиноПоиске для бесплатного просмотра.")

# Обработчик сообщений для поиска фильмов
async def find_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    title = update.message.text
    movie_info = search_movie(title)
    await update.message.reply_text(movie_info)

def main():
    TOKEN = "7510380907:AAHVBZvzQRT9uZo20TtqvH_cca1z-3-rqoI"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_movie))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
