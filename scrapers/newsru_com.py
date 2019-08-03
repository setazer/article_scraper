from scrape import BasicScraper


class MeduzaScraper(BasicScraper):
    domain = 'newsru.com'
    article_body_selector = 'div.article-text'