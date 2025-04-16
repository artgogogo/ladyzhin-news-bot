import requests
from bs4 import BeautifulSoup
import telebot
import time

# === НАЛАШТУВАННЯ ===
BOT_TOKEN = '🔑 ВСТАВ СЮДИ СВІЙ ТОКЕН'
CHANNEL_ID = '@ladyzhin1'
CHECK_INTERVAL = 600  # кожні 10 хв = 600 сек

# зберігаємо опубліковані новини, щоб не дублювати
posted_links = set()

# === ФУНКЦІЯ ПАРСИНГУ САЙТУ ===

def get_ladyzhyn_news():
    url = 'https://ladyzhyn.news/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = soup.select('article')
    news = []

    for a in articles:
        title_tag = a.find('h2')
        if title_tag and a.find('a'):
            title = title_tag.get_text(strip=True)
            link = a.find('a')['href']
            if not link.startswith('http'):
                link = 'https://ladyzhyn.news' + link
            news.append((title, link))
    return news

def get_ladrada_news():
    url = 'https://ladrada.gov.ua/publichna-informatsiia/novyny-hromady.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = soup.select('.itemContainer .itemTitle a')
    news = []

    for a in articles:
        title = a.get_text(strip=True)
        link = a['href']
        if not link.startswith('http'):
            link = 'https://ladrada.gov.ua' + link
        news.append((title, link))
    return news

def get_20minut_news():
    url = 'https://vn.20minut.ua/tag/ladyzhin.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = soup.select('.article-card.clearfix a')
    news = []

    for a in articles:
        title = a.get('title')
        link = a.get('href')
        if title and link:
            if not link.startswith('http'):
                link = 'https://vn.20minut.ua' + link
            news.append((title.strip(), link))
    return news

# === ІНІЦІАЛІЗАЦІЯ БОТА ===

bot = telebot.TeleBot(BOT_TOKEN)

def send_news():
    all_news = get_ladyzhyn_news() + get_ladrada_news() + get_20minut_news()
    new_items = []

    for title, link in all_news:
        if link not in posted_links:
            posted_links.add(link)
            new_items.append(f"{title}\n{link}")

    for item in new_items:
        try:
            bot.send_message(CHANNEL_ID, item)
            time.sleep(1)  # затримка щоб уникнути ліміту
        except Exception as e:
            print(f"Помилка надсилання: {e}")

# === ЦИКЛ ПЕРЕВІРКИ ===

print("Бот запущено. Перевірка новин кожні 10 хвилин...")
while True:
    send_news()
    time.sleep(CHECK_INTERVAL)
    
