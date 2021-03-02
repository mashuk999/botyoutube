import urllib.request
import xmltodict
from bs4 import BeautifulSoup
# from . import models
import re


def findArticle():
    
    xmlFormat = getLatestXML()
    
    jsonFormat = (xmltodict.parse(xmlFormat))['rss']['channel']['item']

    jsonFormat = getUniqueArticle(jsonFormat)

    if jsonFormat is None:
        return 0,0,0,0

    url = jsonFormat['guid']['#text']
    
    web_page = getArticleWebpage(url)
    
    content = scrapArticle(web_page)
    YTtitle = getYoutubeTitle(url)

    

    return jsonFormat['title'], jsonFormat['description'], content, YTtitle

def getUniqueArticle(jsonFormat):
    for item in jsonFormat:
        if len(getYoutubeTitle(item['guid']['#text'])) <= 100:
            try:
                obj = models.uploadedVideos.objects.get(title=item['title'])
            except models.uploadedVideos.DoesNotExist:
                return item
    return None

def getLatestXML():

    req = urllib.request.Request(
    'https://www.amarujala.com/rss/etawah.xml',
    data=None,

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    }
    )

    return urllib.request.urlopen(req)

def getArticleWebpage(url):
    req = urllib.request.Request(
    url, 
    data=None, 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    }
    )

    return urllib.request.urlopen(req)

def scrapArticle(web_page):
    soup = BeautifulSoup(web_page, 'html.parser')
    content =  soup.find("div", {"class": "article-desc ul_styling",})
    contentn = content.find("div", {"class": "article-desc ul_styling",})
    if contentn is not None:
        content = contentn

    for divs in content.findAll("div"):
        divs.extract()
    for divs in content.findAll("blockquote"):
        divs.extract()

    return content.get_text()

def getYoutubeTitle(s):
    s = s.split('/')[-1]
    s = s.replace('-',' ')
    return str(re.sub(r"[A-Za-z]+('[A-Za-z]+)?",lambda mo: mo.group(0).capitalize(),s))