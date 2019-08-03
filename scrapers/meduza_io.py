from scrape import BasicScraper


class MeduzaScraper(BasicScraper):
    domain = 'meduza.io'
    article_body_selector = 'div.GeneralMaterial-article'