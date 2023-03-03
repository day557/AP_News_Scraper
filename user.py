import matplotlib.pyplot as plt
import pandas as pd
from scraper import Scraper


class User:
    def __init__(self, db):
        self.db = db
        self.scraper = Scraper(db)

    def add_phrase(self, phrase):
        if isinstance(phrase, list) or isinstance(phrase, tuple):
            self.db.insert_phrases(list(phrase))
        elif isinstance(phrase, str):
            phrase_list = [phrase]
        else:
            raise ValueError("Invalid phrase type: {}".format(type(phrase)))
        self.db.insert_phrases(phrase_list)

    def list_urls(self):
        return self.db.get_urls()

    def list_categories(self):
        return self.db.get_categories()

    def run_scraper(self, url):
        self.scraper.scrape_urls(url)
        self.scraper.scrape_articles()

    def plot_phrase_occurrences(self, phrase):
        query = "SELECT date FROM news_articles WHERE phrase=%s"
        with self.db.db.cursor() as cursor:
            cursor.execute(query, (phrase,))
            results = cursor.fetchall()

            dates = [result['date'] for result in results]
            date_counts = {}

            for date in dates:
                if date not in date_counts:
                    date_counts[date] = 0
                date_counts[date] += 1

            x = list(date_counts.keys())
            y = list(date_counts.values())

            plt.plot(x, y)
            plt.xlabel('Date')
            plt.ylabel('Occurrences')
            plt.title(f'Occurrences of "{phrase}"')
            plt.show()

    def plot_monthly_phrase_occurrence(self, phrase):
        query = "SELECT DATE_FORMAT(date, '%Y-%m') AS month, COUNT(*) AS count FROM news_articles WHERE phrase = %s GROUP BY month"
        with self.db.db.cursor() as cursor:
            cursor.execute(query, (phrase,))
            results = cursor.fetchall()

        df = pd.DataFrame(results, columns=['month', 'count'])
        df['month'] = pd.to_datetime(df['month'])

        plt.plot(df['month'], df['count'])
        plt.xlabel('Month')
        plt.ylabel('Occurrences')
        plt.title('Monthly occurrences of "{}"'.format(phrase))
        plt.show()
