import os
import urllib.parse as urlparse
import click
import importdir
from scrape import BasicScraper, UnknownScraper

importdir.do("scrapers", globals())  #  импорт всех доступных скрэперов


class WebScraper:
    def __init__(self, url):
        for scraper in BasicScraper.__subclasses__():
            if scraper.domain and scraper.domain in url:
                self.Scraper = scraper(url)
                break
        else:
            self.Scraper = UnknownScraper(url)


    def parse(self):
        parsed_content = self.Scraper.process()
        if not parsed_content:
            click.echo(f'Не удалось распарсить ссылку "{self.Scraper.url}"')
            return
        # destination_filename = 'out.txt'
        destination_filename = self.complication_1_transform()
        with open(destination_filename, 'w') as f:
            f.write(parsed_content)
        click.echo(f'Обработка завершена. Файл сохранён по адресу:\n{destination_filename}')

    def complication_1_transform(self):  # Усложнение задачи 1
        parted_url = urlparse.urlparse(self.Scraper.url)
        domain = parted_url.netloc
        path = parted_url.path
        page_path, ext = os.path.splitext(path)
        if page_path.endswith('/'):
            page_path = page_path[:-1]
        new_filename = os.path.join(*f'{domain}{page_path}.txt'.split('/'))
        new_path = os.path.split(new_filename)[0]
        cur_path = os.getcwd()
        os.makedirs(os.path.join(cur_path, new_path), exist_ok=True)
        result_filename = os.path.join(cur_path, new_filename)
        return result_filename

@click.command()
@click.argument('url')
def main(url):
    ws = WebScraper(url)
    ws.parse()

if __name__ == '__main__':
    main()
