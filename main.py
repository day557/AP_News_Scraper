from database import Database
from user import User

db = Database('localhost', 'admin', 'password', 'yourdatabase')

user = User(db)

# add to the search phrasesa.
user.add_phrase('refugees')

user.run_scraper('https://apnews.com')

print('Scrape Complete!')

# See a list of all the categories that have been stored.
user.list_categories()

# See a list of all the URLs that have been stored.
user.list_urls()

# See a chart that depicts the occurrence of a specific search phrase.
user.plot_phrase_occurrences('interest rate')
