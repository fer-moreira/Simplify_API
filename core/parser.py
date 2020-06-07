# utf-8

from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
from requests.exceptions import ConnectionError

import codecs, sys, bs4, json

from datetime import datetime
from dateutil import parser

class PageParser (object):
    def __init__ (self, url):
        self._json = {}
        self.url = url


    def get_meta (self,soup,property,param):
        if soup.find("meta",property=property):
            element = soup.find("meta", property=property)
            return element[param]
        else:
            return ""
    
    def get_pubdate (self, soup):
        if soup.find("meta", property="article:published_time"):
            element = soup.find("meta", property="article:published_time")["content"]
        elif soup.find("meta", property="bt:pubDate"):
            element = soup.find("meta", property="bt:pubDate")["content"]
        elif soup.find("meta", property="DC.date.issued"):
            element = soup.find("meta", property="DC.date.issued")["content"]
        elif soup.find("meta", property="pubdate"):
            element = soup.find("meta", property="pubdate")["content"]
        else:
            element = ""


        if element != "":
            d = parser.parse(str(element))
            element = str(datetime.strftime(d, "%h %d %Y - %H:%M"))

        return element
     
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
            favico_uri = "https://www.google.com/s2/favicons?domain={0}".format(domain)
            return favico_uri
        
        except:
            favico_uri = "https://www.google.com/s2/favicons?domain={0}".format("google.com")
            return favico_uri

            

    # THIS FUNCTION PARSE THE ARTICLE FROM HTML TO A PYTHON DICT
    def get_body (self,article):
        article_body    = []
        article_paragraphs = article.find_all(['p','figure'])
        for paragraph in article_paragraphs:
            if paragraph.find("img"):
                img_uri = paragraph.find('img')
                wanted_classes = ['src', 'data-src']

                if img_uri:
                    classes_list = list(img_uri.attrs.keys())
                    have_wanted = [x in classes_list for x in wanted_classes]
                    
                    for id, value in enumerate(have_wanted):
                        if value:
                            content = str(img_uri.attrs[wanted_classes[id]])

                            if len(content) < 5:
                                pass
                            else:
                                alt = str(img_uri.attrs.get('alt'))
                                article_body.append({
                                    'is_img' : True,
                                    'content' : content,
                                    "alt": alt
                                })
            else:
                ptext = paragraph.text
                if not ptext in ['Advertisement','Supported by','ads','ad','anúncio', 'transcript']:
                    props = []

                    strongs = paragraph.find_all("strong")
                    links = paragraph.find_all("a")

                    if strongs:
                        for s in strongs:
                            text = str(s.text)
                            steps = len(text)
                            startindex = str(ptext).find(str(text))
                            tag_type = 'strong'

                            props.append({
                                'start':startindex,
                                'steps':steps,
                                'type':tag_type,
                                'text':text
                            })
                    if links:
                        for a in links:
                            text = str(a.text)
                            steps = len(text)
                            startindex = str(ptext).find(str(text))
                            tag_type = 'link'

                            props.append({
                                'start':startindex,
                                'steps':steps,
                                'type':tag_type,
                                'text':text,
                                'href': a['href'] if a.has_attr('href') else ''
                            })

                    article_body.append(
                        {
                            'is_img':False,
                            'content':ptext,
                            'props':props
                        }
                    )


        return {'data':article_body}

    
    def dump_json (self):
        page = requests.get(self.url)
        self.page = BeautifulSoup(page.content, 'html.parser')
        article = self.page.find('article')

        
        temp_origin     = self.get_meta(self.page, "og:site_name", 'content')
        site_name       = temp_origin if not temp_origin == "" else self.url_domain 

        article_data = self.get_body(article)
            
        full_json = {
            'code' : 200,
            'original_post'       : str(self.url),
            'site_name'           : site_name,
            'site_favicon'        : self.get_favico(),
            "article_pubdate"     : self.get_pubdate(self.page),
            'article_title'       : self.get_meta(self.page,"og:title","content"),
            'article_description' : self.get_meta(self.page, "og:description", 'content'),
            'article_image'       : self.get_meta(self.page, "og:image", 'content'),
            'article_body'        : article_data.pop('data',''),
        }

        self._json = json.dumps(full_json, ensure_ascii=False)

        return self._json