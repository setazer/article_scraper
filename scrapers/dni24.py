from scrape import BasicScraper


class Dni24Scraper(BasicScraper):
    domain = 'dni24.com'
    article_body_selector = 'article'