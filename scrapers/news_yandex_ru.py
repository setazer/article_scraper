from scrape import BasicScraper


class YandexNewsScraper(BasicScraper):
    domain = 'news.yandex.ru'
    article_body_selector = 'div.doc__content'