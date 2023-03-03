import pymysql.cursors
import init_data


class Database:
    init_keywords = init_data.keywords()
    init_phrases = init_data.phrases()
    init_categories = init_data.categories()
    sql_create_table_articles = "CREATE TABLE IF NOT EXISTS news_articles (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, headline VARCHAR(255), url VARCHAR(255), phrase VARCHAR(255), count INT, category VARCHAR(255), date DATE)"
    sql_create_table_phrases = "CREATE TABLE IF NOT EXISTS phrases (phrase VARCHAR(255) UNIQUE)"
    sql_create_table_categories = "CREATE TABLE IF NOT EXISTS categories (category_id INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(255) NOT NULL, UNIQUE (category))"
    sql_create_table_keywords = "CREATE TABLE IF NOT EXISTS keywords (keyword_id INT AUTO_INCREMENT PRIMARY KEY, keyword VARCHAR(255) UNIQUE NOT NULL, category_id INT, FOREIGN KEY (category_id) REFERENCES categories(category_id))"
    sql_insert_init_phrases = "INSERT IGNORE INTO phrases (phrase) VALUES (%s)"
    sql_insert_init_categories = "INSERT IGNORE INTO categories (category) VALUES (%s)"
    sql_insert_init_keywords = "INSERT IGNORE INTO keywords (keyword, category_id) VALUES (%s, %s)"
    sql_insert_article = "INSERT INTO news_articles (headline, url, phrase, count, category, date) VALUES (%s, %s, %s, %s, %s, %s)"

    def __init__(self, host, user, password, database):
        self.db = pymysql.connect(
            host=host,
            user=user,
            password=password,
            cursorclass=pymysql.cursors.DictCursor,
            database=database
        )
        self.create_tables()

    def create_tables(self):
        with self.db.cursor() as cursor:
            cursor.execute(self.sql_create_table_articles)
            cursor.execute(self.sql_create_table_phrases)
            cursor.execute(self.sql_create_table_categories)
            cursor.execute(self.sql_create_table_keywords)
            self.db.commit()

        self.insert_init_phrases()
        self.insert_init_categories()
        self.insert_init_keywords()

    def insert_init_phrases(self):
        with self.db.cursor() as cursor:
            cursor.executemany(self.sql_insert_init_phrases, [(phrase,) for phrase in self.init_phrases])
            self.db.commit()

    def insert_init_categories(self):
        with self.db.cursor() as cursor:
            cursor.executemany(self.sql_insert_init_categories, [(category,) for category in self.init_categories])
            self.db.commit()

    def insert_init_keywords(self):
        with self.db.cursor() as cursor:
            cursor.executemany(self.sql_insert_init_keywords, [(keyword[0], keyword[1]) for keyword in self.init_keywords])
            self.db.commit()

    def insert_article(self, headline, url, phrase, count, category, date):
        with self.db.cursor() as cursor:
            cursor.execute(self.sql_insert_article, (headline, url, phrase, count, category, date))
            self.db.commit()

    def get_urls(self):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT url FROM news_articles")
            results = cursor.fetchall()
            return [result['url'] for result in results]

    def insert_phrases(self, phrases):
        sql_insert = "INSERT INTO phrases (phrase) VALUES (%s)"
        for phrase in phrases:
            phrases_in_db = self.get_phrases()
            if phrase in phrases_in_db:
                continue
            with self.db.cursor() as cursor:
                cursor.execute(sql_insert, (phrase))
                self.db.commit()

    def get_phrases(self):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT phrase FROM phrases")
            results = cursor.fetchall()
            return [result['phrase'] for result in results]

    def get_categories(self):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT category FROM categories")
            results = cursor.fetchall()
            return [result['category'] for result in results]

    def get_keywords(self):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT keyword FROM keywords")
            results = cursor.fetchall()
            return [result['keyword'] for result in results]

    def get_keyword_category(self, id):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT category FROM categories where category_id =%s", (id))
            results = cursor.fetchall()
            return [result['category'] for result in results]

    def get_category_id(self, keyword):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT category_id, keyword FROM keywords WHERE keyword = %s", (keyword,))
            results = cursor.fetchall()
            return [result['category_id'] for result in results]
