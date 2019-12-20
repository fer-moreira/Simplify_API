# utf-8

from bs4 import BeautifulSoup
import requests
import codecs

class PageReader (object):
    def __init__ (self):
        self._json = {}
        self._html = ''''''

        self.file = codecs.open("debug.html","w","utf-8")

    @property
    def url (self):
        return self._url
    
    @url.setter
    def url (self,value):
        self._url = value

    @property
    def dump_json (self):
        page = self.scrap_soup

        header = page.find('head')
        article = page.find('article')

        title       = page.find("meta", property="og:title")['content']
        pre_title   = page.find("meta", property="og:description")['content']
        post_image  = page.find("meta", property="og:image")['content']
        site_origin = page.find("meta", property="og:site_name")['content']
        _keys       = page.find_all("meta",property="article:tag")

        keywords = []

        for k in _keys:
            key_content = str(k['content']).split(',')
            keywords = keywords + key_content

        raw_paragraphs = article.find_all("p")
        paragraphs_config = []


        for p in raw_paragraphs:
            p_json = {}
            
            if not p.find("strong") == None:
                pass

                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI
                # VOCÊ PAROU AQUI


        self.file.write(str(paragraphs))

        self._json = {
            'title'       : title,
            'pre_title'   : pre_title,
            'site_origin' : site_origin,
            'post_image'  : post_image,
            'keywords'    : keywords,
            'body'        :'paragraphs'
        }
        return self._json

    @property
    def scrap_soup (self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    @property
    def dump_html (self):
        return '<p>sex</p>'
