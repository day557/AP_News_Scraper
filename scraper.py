import requests
from bs4 import BeautifulSoup
import datetime


class Scraper:
    def __init__(self, db):
        self.session = requests.Session()
        self.urls = []
        self.db = db
        self.phrases = self.db.get_phrases()
        self.keywords = self.db.get_keywords()

    def scrape_urls(self, url):
        main_page_response = self.session.get(url)
        soup = BeautifulSoup(main_page_response.content, 'html.parser')
        for tag in soup.select('a[href^="/hub"]'):
            hub_url = ('https://apnews.com' + tag['href'])
            hub_response = self.session.get(hub_url)
            soup = BeautifulSoup(hub_response.content, 'html.parser')
            for link in (a for a in soup.select('a[class^="Component-headline"]') if "/video/" not in a['href']):
                self.urls.append('https://apnews.com' + link['href'])

    def scrape_articles(self):
        for url in self.urls:
            urls_in_db = self.db.get_urls()
            if url in urls_in_db:
                continue

            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            headline = soup.find('h1').get_text().strip()
            paragraphs = soup.find_all('p')
            article_text = ''

            for paragraph in paragraphs:
                article_text += paragraph.get_text().strip()

            keyword_counts = {
                keyword: article_text.lower().count(keyword.lower())
                for keyword in self.keywords
                if keyword.lower() in article_text.lower().split()
            }

            top_keyword = max(keyword_counts, key=keyword_counts.get) if keyword_counts else None
            category_id = self.db.get_category_id(top_keyword) if top_keyword else None

            for phrase in self.phrases:
                if phrase.lower() in article_text.lower():
                    count = article_text.lower().count(phrase.lower())
                    category = self.db.get_keyword_category(category_id) if category_id else None
                    date = datetime.datetime.now().strftime('%Y-%m-%d')
                    self.db.insert_article(headline, url, phrase, count, category, date)
