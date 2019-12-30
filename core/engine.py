# utf-8

from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
from requests.exceptions import ConnectionError

import codecs, sys, bs4, json

from PIL import Image
from io import BytesIO,StringIO

class PageReader (object):
    def __init__ (self):
        self._json = {}

    @property
    def scrap_soup (self):
        try:
            page = requests.get(self.url)
            soup = BeautifulSoup(page.content, 'html.parser')
            return soup
        except ConnectionError: raise
        except AttributeError: raise

    @property
    def url (self):
        return self._url
    
    @url.setter
    def url (self,value):
        self._url = value


    def get_meta (self,soup,property,param):
        if soup.find("meta",property=property):
            element = soup.find("meta", property=property)
            return element[param]
        else:
            return ""

    def get_keywords (self,soup,property):
        try:
            keywords = []
            if soup.find_all("meta",property=property):
                elements = soup.find_all("meta", property=property)

                for e in elements:
                    keyvalue = e['content']
                    keys = str(keyvalue).split(',')
                    keywords += keys

                return keywords
            else:
                return []
        except TypeError:
            return []
            

    @property
    def url_domain (self):
        try: return urlparse(self.url).netloc
        except: return ""

    def try_request (self, url):
        try:
            req = requests.get(url, timeout=4)
            code = req.status_code
            req.close()
            return code
        except:
            return 404



    def get_favico (self):
        try:
            domain = self.url_domain
            high_res_favico = "https://{0}/apple-touch-icon.png".format(domain)
            low_res_favico = "https://{0}/favicon.ico".format(domain)


            if self.try_request(high_res_favico) == 200:
                favico_uri = high_res_favico
            elif self.try_request(low_res_favico) == 200:
                favico_uri = low_res_favico
            else:
                favico_uri = self.page.find("link", rel="shortcut icon")['href']

            return favico_uri
        except:
            favico_uri = self.page.find("link", rel="shortcut icon")['href']          
            return favico_uri if self.url_domain in favico_uri else "{0}{1}".format(self.url_domain,favico_uri)

            

    # THIS FUNCTION PARSE THE ARTICLE FROM HTML TO A PYTHON DICT
    def get_body (self,article):
        article_body    = []
        article_paragraphs = article.find_all('p')
        capitalized_char = ''
        p_index = 0
        for paragraph in article_paragraphs:
            if paragraph.find("img"):
                try: img_uri = paragraph.find('img')['src']
                except KeyError: pass
                
                try:
                    req = requests.get(img_uri)
                    info = Image.open(BytesIO(req.content))
                    size = info.size
                    info.close()
                    img_size = size
                except:
                    img_size = [0,0]

                if (img_size[0] + img_size[1]) > 100:
                    article_body.append({
                        'content':img_uri,
                        'is_img':True,
                        'resolution':{
                                'width':img_size[0],
                                'height':img_size[1]
                    }})
                else: pass
            else:
                if not paragraph.text in ['Advertisement','Supported by']:
                    if p_index == 0 and paragraph.text:
                        if len(str(paragraph.text)) > 0:
                            capitalized_char = str(paragraph.text)[0]
                        
                        article_body.append({'content':paragraph.text[1:],'is_img':False})
                    else:
                        article_body.append({'content':paragraph.text,'is_img':False})
                    p_index += 1

        return {'data':article_body, 'capital':capitalized_char}

    @property
    def dump_json (self):
        self.page = self.scrap_soup
        article = self.page.find('article')

        
        temp_origin     = self.get_meta(self.page, "og:site_name", 'content')
        site_name       = temp_origin if not temp_origin == "" else self.url_domain 

        article_data = self.get_body(article)
            
        full_json = {
            'code' : 200,
            'article_title'       : self.get_meta(self.page,"og:title","content"),
            'article_description' : self.get_meta(self.page, "og:description", 'content'),
            'article_image'       : self.get_meta(self.page, "og:image", 'content'),
            'article_capitalize'  : article_data.pop('capital', ''),
            'article_body'        : article_data.pop('data',''),
            'site_name'           : site_name,
            'site_favicon'        : self.get_favico(),
            'keywords'            : self.get_keywords(self.page, "article:tag"),
            'original_post'       : str(self.url),
        }

        self._json = json.dumps(full_json,ensure_ascii=False)

        return self._json