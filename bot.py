import feedparser
import asyncio
from telegram import Bot
from datetime import datetime

# Твой токен от BotFather
BOT_TOKEN = "7758500745:AAGF3Vr0GLbQgk_XudSHGxZVbC33Spwtm3o"

# ID канала Telegram (если канал приватный или username не работает)
CHANNEL_ID = -1002650552114  # числовой ID без кавычек

# Ссылки на фиды скидок
RSS_FEEDS = [
    "https://slickdeals.net/newsearch.php?searchin=first&rss=1&sort=popularity&filter=Amazon",
    "https://www.hotukdeals.com/tag/amazon.rss"
]

# Создаем объект бота
bot = Bot(token=BOT_TOKEN)

# Список уже опубликованных ссылок
posted_links = set()

# Файл для логов
LOG_FILE = "bot_log.txt"

def log_message(message: str):
    """Запись сообщений в лог-файл с таймштампом"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

async def fetch_and_post_deals():
    # Тестовое сообщение при запуске
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text="✅ SaleHunt Bot успешно запущен и следит за скидками!")
        log_message("✅ Тестовое сообщение отправлено.")
    except Exception as test_error:
        log_message(f"❌ Ошибка при отправке тестового сообщения: {test_error}")

    while True:
        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    link = entry.link
                    title = entry.title
                    if link not in posted_links:
                        posted_links.add(link)
                        message = f"🔥 {title}\n\n👉 [Посмотреть предложение]({link})"
                        try:
                            await bot.send_message(
                                chat_id=CHANNEL_ID,
                                text=message,
                                parse_mode='Markdown',
                                disable_web_page_preview=False
                            )
                            print(f"✅ Опубликовано: {title}")
                            log_message(f"✅ Опубликовано: {title}")
                        except Exception as send_error:
                            print(f"❌ Ошибка отправки сообщения: {send_error}")
                            log_message(f"❌ Ошибка отправки сообщения: {send_error}")
            except Exception as feed_error:
                print(f"❌ Ошибка загрузки фида: {feed_error}")
                log_message(f"❌ Ошибка загрузки фида: {feed_error}")

        # Проверять новые предложения каждые 30 минут
        await asyncio.sleep(30 * 60)

# Запуск
if name == "__main__":
    print("🚀 Бот запущен и следит за скидками!")
    log_message("🚀 Бот запущен.")
    asyncio.run(fetch_and_post_deals())