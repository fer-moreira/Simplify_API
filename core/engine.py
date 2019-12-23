# utf-8

from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
from requests.exceptions import ConnectionError
import codecs
import sys
import bs4
import json

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
        if soup.find_all("meta",property=property):
            element = soup.find_all("meta", property=property)
            return element
        else:
            return []


    @property
    def url_domain (self):
        try: return urlparse(self.url).netloc
        except: return ""

    def get_favico (self):
        try:
            domain = self.url_domain
            favico_uri = "https://{0}/favicon.ico".format(domain)
            return favico_uri
        except:
            return ""
            


    @property
    def dump_json (self):
        page = self.scrap_soup
        article = page.find('article')

        title           = self.get_meta(page,"og:title","content")
        pre_title       = self.get_meta(page, "og:description", 'content')
        post_image      = self.get_meta(page, "og:image", 'content')
        post_image_alt  = self.get_meta(page, "og:image:alt", 'content')
        temp_origin     = self.get_meta(page, "og:site_name", 'content')
        site_origin     = temp_origin if not temp_origin == "" else self.url_domain 
        _keys           = self.get_keywords(page, "article:tag")
        site_image      = self.get_favico()
        keywords        = []
    

        if _keys:
            for k in _keys:
                key_content = str(k['content']).split(',')
                keywords = keywords + key_content

        raw_paragraphs_by_source = page.findAll('p')
        raw_paragraphs_by_article = article.findAll('p')

        # if len(raw_paragraphs_by_source) > len(raw_paragraphs_by_article):  
        #     raw_paragraphs = raw_paragraphs_by_source
        # else: 
        raw_paragraphs = raw_paragraphs_by_article

        paragraphs_config = []

        for p in raw_paragraphs:
            if not p.text in ['Advertisement','Supported by', 'Publicidade']:
                if p.find('a') and p.find('a')['href']: 
                    _link = str(p.find('a')['href'])
                else: _link = ''
                
                p_json = {
                    'text':p.text,
                    'strong': True if p.find("strong") or p.find("b") else False,
                    'a': True if p.find("a") else False,
                    'a_link': _link
                }
                paragraphs_config.append(p_json)
            else: pass

        full_json = {
            'origin'      : str(self.url),
            'title'       : title,
            'pre_title'   : pre_title,
            'site_origin' : site_origin,
            'site_image'  : site_image,
            'post_image'  : post_image,
            'post_img_alt': post_image_alt,
            'keywords'    : keywords,
            'body'        : paragraphs_config,
        }

        self._json = json.dumps(full_json,ensure_ascii=False)

        return self._json

    @property
    def dump_html (self):
        _json = (json.loads(self.dump_json))

        keywords = ''
        paragraph_text = " "
        origin = _json.pop('origin','')
        title = _json.pop('title','')
        title_img = _json.pop('post_image','')
        pretitle = _json.pop('pre_title','')
        origin = _json.pop('site_origin','')
        origin_img = _json.pop('site_image','')

        ks = _json.pop('keywords',[])

        for k in ks: keywords += "<p>| %s |</p>"%str(k)
        ps = _json.pop('body','')

        for p in ps:
            p_text = ""
            text = p.pop('text','')
            strong = p.pop('strong',False)
            islink = p.pop('a',False)
            link = p.pop('a_link','') 

            if strong:
                if islink:  p_text = "<p><a href={1}><strong>{0}</strong></a></p>".format(text,link)
                else:       p_text = "<p><strong>{0}</strong></p>".format(text)
            elif not strong and islink:
                p_text = "<p><a href={1}>{0}</a></p>".format(text,link)
            else:
                p_text = "<p>{0}</p>".format(text)
            paragraph_text += p_text


        html_text = '''
        <img src="{favico}">
        <h3>{origin}</h3>
        <h1>{title}</h1>
        <h2>{ptitle}</h2>
        <img src="{full}">
        <div style="display: flex;">{keywords}</div>
        {parag}
        '''.format(
            origin=origin,
            title=title,
            ptitle=pretitle,
            favico=origin_img,
            full=title_img,
            keywords=keywords,
            parag=paragraph_text
        )

        return html_text
