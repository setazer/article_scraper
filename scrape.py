import requests
from lxml import etree
from lxml.cssselect import CSSSelector


class BasicScraper:
    domain = None
    article_body_selector = None
    def __init__(self, url):
        self.url = url

    def process(self):
        headers_mobile = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 '
                          '(KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}
        return self.parse(requests.get(url=self.url, headers=headers_mobile))

    @staticmethod
    def trim(text: str):
        while '\n\n' in text:
            text = text.replace('\n\n', '\n')
        return text

    def retrieve_text(self, el: etree._Element):
        paragraphs = []
        for sub_el in el:
            if isinstance(sub_el, etree._Comment):
                continue
            elif sub_el.tag in ('p', 'div'):
                if sub_el.text:
                    paragraphs.append(sub_el.text)
                if sub_el.tail:
                    paragraphs.append(sub_el.tail)
                paragraphs.extend(self.retrieve_text(sub_el))
                paragraphs.append('\n')
            elif sub_el.tag == 'a':
                if sub_el.text:
                    cur_text = f"{sub_el.text}[{sub_el.get('href')}]"
                    paragraphs.append(cur_text)
                if sub_el.tail:
                    paragraphs.append(sub_el.tail)
                paragraphs.extend(self.retrieve_text(sub_el))
            elif sub_el.tag != 'script':
                if sub_el.text:
                    paragraphs.append(sub_el.text)
                if sub_el.tail:
                    paragraphs.append(sub_el.tail)
                paragraphs.extend(self.retrieve_text(sub_el))
            else:
                paragraphs.extend(self.retrieve_text(sub_el))
        return paragraphs

    def format_text(self, text: str):
        formatted_text = ''
        lines = text.splitlines()
        for line in map(str.strip, lines):
            if not line:
                continue
            elif len(line) <= 80:
                formatted_line = ''.join((line, '\n'))
            else:
                words = line.split()
                line_words = []
                formatted_line = ''
                for word in words:
                    if len(' '.join((*line_words, word))) <= 80:
                        line_words.append(word)
                    else:
                        formatted_line = ''.join((formatted_line, ' '.join(line_words), '\n'))
                        line_words = [word]
                formatted_line = ''.join((formatted_line, ' '.join(line_words), '\n'))
            formatted_text = ''.join((formatted_text, formatted_line, '\n'))
        return formatted_text

    def parse(self, request):
        html = etree.HTML(request.text)
        body_sel = CSSSelector(self.article_body_selector)
        selected_elements = body_sel(html)
        paragraph_elements = self.retrieve_text(selected_elements)
        title_sel = CSSSelector('title')
        try:
            title = title_sel(html)[0].text
            paragraph_elements.insert(0, title + '\n')  # Заголовок страницы добавляется как заголовок статьи
        except IndexError:
            pass
        text = self.format_text(self.trim(''.join(paragraph_elements)))
        return text


class UnknownScraper(BasicScraper):
    article_body_selector = 'div[itemprop=articleBody]'  # замечено как хранилище по-умолчанию на нескольких сайтах