from bs4 import BeautifulSoup
import requests

class PageReader (object):
    def __init__ (self):
        self._json = {}
        self._html = ''''''


    @property
    def url (self):
        return self._url
    
    @url.setter
    def url (self,value):
        self._url = value

    @property
    def dump_json (self):
        page = self.scrap_soup

        header = page.find('header')

        title = page.find("meta",  property="og:title")['content']
        pre_title = page.find("meta",  property="og:description")['content']
        site_origin = page.find("meta", property="og:site_name")['content']

        images = header.find_all('img')

        print(images)


        body = page.find('main')
        paragraphs = body.find_all('p')
        text_p = [p.text for p in paragraphs]
        

        self._json = {
            'title':title,
            'pre_title':pre_title,
            'body':'text_p'
        }
        return self._json

    @property
    def scrap_soup (self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup

    @property
    def dump_html (self):
        return 'article'
