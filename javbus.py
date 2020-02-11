import re
from pyquery import PyQuery as pq  # need install
from lxml import etree  # need install
from bs4 import BeautifulSoup  # need install
import json
from ADC_function import *


def getActorPhoto(htmlcode):  # //*[@id="star_qdt"]/li/a/img
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find_all(attrs={'class': 'star-name'})
    d = {}
    for i in a:
        l = i.a['href']
        t = i.get_text()
        html = etree.fromstring(get_html(l), etree.HTMLParser())
        p = str(html.xpath('//*[@id="waterfall"]/div[1]/div/div[1]/img/@src')).strip(" ['']")
        p2 = {t: p}
        d.update(p2)
    return d


def getTitle(htmlcode):  # 获取标题
    doc = pq(htmlcode)
    title = str(doc('div.container h3').text()).replace(' ', '-')
    try:
        title2 = re.sub('n\d+-', '', title)
        return title2
    except:
        return title


def getStudio(htmlcode):  # 获取厂商
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[5]/a/text()')).strip(" ['']")
    return result


def getYear(htmlcode):  # 获取年份
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[2]/text()')).strip(" ['']")
    return result


def getCover(htmlcode):  # 获取封面链接
    doc = pq(htmlcode)
    image = doc('a.bigImage')
    return image.attr('href')


def getRelease(htmlcode):  # 获取出版日期
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[2]/text()')).strip(" ['']")
    return result


def getRuntime(htmlcode):  # 获取分钟
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find(text=re.compile('分鐘'))
    return a


def getActor(htmlcode):  # 获取女优
    b = []
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find_all(attrs={'class': 'star-name'})
    for i in a:
        b.append(i.get_text())
    return b


def getNum(htmlcode):  # 获取番号
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[1]/span[2]/text()')).strip(" ['']")
    return result


def getDirector(htmlcode):  # 获取导演
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[4]/a/text()')).strip(" ['']")
    return result


def getOutline(htmlcode):  # 获取演员
    doc = pq(htmlcode)
    result = str(doc('tr td div.mg-b20.lh4 p.mg-b20').text())
    return result


def getSerise(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[6]/a/text()')).strip(" ['']")
    return result


def getSerise_uncensored(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[5]/a/text()')).strip(" ['']")
    return result


def getCover_small(number):
    htmlcode = get_html('https://avsox.host/cn/search/' + number)
    html = etree.fromstring(htmlcode, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//*[@id="waterfall"]/div/a/@href')).strip(" ['']")
    if result1 == '' or result1 == 'null' or result1 == 'None':
        htmlcode = get_html('https://avsox.host/cn/search/' + number.replace('-', '_'))
        html = etree.fromstring(htmlcode, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
        result1 = str(html.xpath('//*[@id="waterfall"]/div/a/@href')).strip(" ['']")
        if result1 == '' or result1 == 'null' or result1 == 'None':
            htmlcode = get_html('https://avsox.host/cn/search/' + number.replace('_', ''))
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('//*[@id="waterfall"]/div/a/div[1]/img/@src')).strip(" ['']")
    return result


def getTag(htmlcode):  # 获取演员
    tag = []
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find_all(attrs={'class': 'genre'})
    for i in a:
        if 'onmouseout' in str(i):
            continue
        tag.append(i.get_text())
    return tag


def main(number):
    htmlcode = get_html('https://www.javbus.com/' + number)
    try:
        dww_htmlcode = get_html("https://www.dmm.co.jp/mono/dvd/-/detail/=/cid=" + number.replace("-", ''))
    except:
        dww_htmlcode = ''
    try:
        dic = {
            'title': str(re.sub('\w+-\d+-', '', getTitle(htmlcode))),
            'studio': getStudio(htmlcode),
            'year': str(re.search('\d{4}', getYear(htmlcode)).group()),
            'outline': getOutline(dww_htmlcode).replace('\n', ''),
            'runtime': getRuntime(htmlcode),
            'director': getDirector(htmlcode),
            'actor': getActor(htmlcode),
            'release': getRelease(htmlcode),
            'number': getNum(htmlcode),
            'cover': getCover(htmlcode),
            'imagecut': 1,
            'tag': getTag(htmlcode),
            'label': getSerise(htmlcode),
            'actor_photo': getActorPhoto(htmlcode),
            'website': 'https://www.javbus.com/' + number,
            'source': 'javbus.py',
        }
    except:
        if htmlcode == 'ProxyError':
            dic = {
                'title': '',
                'website': 'timeout',
            }
        else:
            dic = {
                'title': '',
                'website': '',
            }
    js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'), )  # .encode('UTF-8')
    return js


def main_uncensored(number):
    htmlcode = get_html('https://www.javbus.com/' + number)
    if getTitle(htmlcode) == '':
        htmlcode = get_html('https://www.javbus.com/' + number.replace('-', '_'))
    try:
        dic = {
            'title': str(re.sub('\w+-\d+-', '', getTitle(htmlcode))).replace(getNum(htmlcode) + '-', ''),
            'studio': getStudio(htmlcode),
            'year': getYear(htmlcode),
            'outline': '',
            'runtime': getRuntime(htmlcode),
            'director': getDirector(htmlcode),
            'actor': getActor(htmlcode),
            'release': getRelease(htmlcode),
            'number': getNum(htmlcode),
            'cover': getCover(htmlcode),
            'tag': getTag(htmlcode),
            'label': getSerise_uncensored(htmlcode),
            'imagecut': 3,
            'cover_small': getCover_small(number),
            'actor_photo': getActorPhoto(htmlcode),
            'website': 'https://www.javbus.com/' + number,
            'source': 'javbus.py',
        }
        if dic['cover_small'] == '':
            dic['imagecut'] = 0
    except:
        if htmlcode == 'ProxyError':
            dic = {
                'title': '',
                'website': 'timeout',
            }
        else:
            dic = {
                'title': '',
                'website': '',
            }
    js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'), )  # .encode('UTF-8')
    return js

# print(main('SSNI-658'))
# print(main_uncensored('051119-917'))
