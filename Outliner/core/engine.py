# utf-8

from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
import codecs
import sys

class PageReader (object):
    def __init__ (self):
        self._json = {}

    @property
    def scrap_soup (self):
        try:
            page = requests.get(self.url)
            soup = BeautifulSoup(page.content, 'html.parser')
            return soup
        except ConnectionError:
            print("Parece que você não está conectado a uma internet!!")
            sys.exit()

    @property
    def url (self):
        return self._url
    
    @url.setter
    def url (self,value):
        self._url = value

    @property
    def dump_json (self):
        page = self.scrap_soup

        article = page.find('article')

        title       = page.find("meta", property="og:title")['content']
        pre_title   = page.find("meta", property="og:description")['content']
        post_image  = page.find("meta", property="og:image")['content'] if page.find("meta", property="og:image") else ''
        site_origin = page.find("meta", property="og:site_name") if page.find("meta", property="og:site_name") else ''
        _keys       = page.find_all("meta",property="article:tag")
        temp_favico = page.find("link", rel="shortcut icon")['href']
        site_image = ''
        keywords = []
        
        # ========= FUNCTION TO GET THE FAVICON URL RIGHT =====================
        if not 'http' in temp_favico and not '.com' in temp_favico:
            domain = str(self.url).split("//")[1].split("/")[0]
            site_image = "http://{d}{fav}".format(d=domain,fav=temp_favico)
        elif '.com' in temp_favico:
            if temp_favico[:2] == '//':
                site_image = "http://" + temp_favico[2:]
            elif temp_favico[0] == '/':
                site_image = "http://" + temp_favico[1:]
        else:
            site_image = temp_favico
        # ======================================================================

        for k in _keys:
            key_content = str(k['content']).split(',')
            keywords = keywords + key_content

        raw_paragraphs_by_source = page.findAll('p')
        raw_paragraphs_by_article = article.findAll('p')

        if len(raw_paragraphs_by_source) > len(raw_paragraphs_by_article):  raw_paragraphs = raw_paragraphs_by_source
        else: raw_paragraphs = raw_paragraphs_by_article

        paragraphs_config = []

        for p in raw_paragraphs:
            if p.find('a'): _link = str(p.find('a')['href'])
            else: _link = ''
            
            p_json = {
                'text':p.text,
                'strong': True if p.find("strong") or p.find("b") else False,
                'a': True if p.find("a") else False,
                'a_link': _link
            }
            paragraphs_config.append(p_json)

        self._json = {
            'title'       : title,
            'pre_title'   : pre_title,
            'site_origin' : site_origin,
            'site_image'  : site_image,
            'post_image'  : post_image,
            'keywords'    : keywords,
            'body'        : paragraphs_config,
        }

        return self._json



    @property
    def dump_html (self):
        _json = dict(self.dump_json)

        keywords = ''
        paragraph_text = " "
        title = _json.pop('title','')
        title_img = _json.pop('post_image','')
        pretitle = _json.pop('pre_title','')
        origin = _json.pop('site_origin','')
        origin_img = _json.pop('site_image','')

        ks = _json.pop('keywords',[])

        for k in ks: keywords += "<p>| %s |</p>\n"%str(k)
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
        <h1>{title}</h1>
        <h2>{ptitle}</h2>
        <h3>{site}</h3>
        <img src="{favico}">
        <img src="{full}">
        <div style="display: flex;">{keywords}</div>
        {parag}
        '''.format(
            title=title,
            ptitle=pretitle,
            site=origin,
            favico=origin_img,
            full=title_img,
            keywords=keywords,
            parag=paragraph_text
        )

        return html_text
