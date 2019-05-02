# -*- coding: utf-8 -*-
import urllib
import os
import requests
import random
#from urllib import  request
from bs4 import BeautifulSoup
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

def _get_html(url_address):
    """
    通过url_address得到网页内容
    :param url_address: 请求的网页地址
    :return: html
    """
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",

    ]
    agent = random.choice(user_agents)
    headers = {'User-Agent':agent,
               'Referer': 'http://desk.zol.com.cn/1920x1080/'}

    req = urllib.request.Request(url=url_address, headers=headers)
    return urllib.request.urlopen(req)
    #req=requests.get(url_address,headers=headers)
    return req

#
def _get_soup(html):
    """
    把网页内容封装到BeautifulSoup中并返回BeautifulSoup
    :param html: 网页内容
    :return:BeautifulSoup
    """
    if None == html:
        return
    return BeautifulSoup(html.read(), "html.parser")


def _get_page_title(soup):
    #print(soup.find(id_="titleName").get_text())
    return soup.find(id="titleName").get_text()

def _get_img_dirs(soup):
    """
    获取所有相册标题及链接
    :param soup: BeautifulSoup实例
    :return: 字典（ key:标题， value:内容）
    """
    if None == soup:
        return
    #print(soup.text)
    lis = soup.find(class_="pic-list2 clearfix").findAll(name='li') # findAll(name='a') # attrs={'class':'lazy'}
    #print(type(lis))
    if None != lis:
        img_dirs = {};
        #print(lis.find('a'))
        for li in lis:
            try:
                #print(type(li))
                links =li.find('a')

                k = links.find('img').attrs['alt']
                #print(k)
                t = links.attrs['href']
                #print(t)
                img_dirs[k] = 'http://desk.zol.com.cn/'+t;
            except Exception as e:
                continue
        print(img_dirs)
        return img_dirs


def _download_albums(dir, albums):
    for a in albums:
        _download_imgs(dir, a, albums.get(a))



def _download_imgs(dir, t, l):
    if None == t or None == l:
        return
    print("创建相册：" + dir + "/" + t + " " + l)
    name=t
    t = dir + "/" + t
    print(l)
    try:
        os.mkdir(t)
    except Exception as e:
        print("文件夹："+t+"，已经存在")

    print("开始获取相册《" + name + "》")

    dir_html = _get_html(l)
    dir_soup = _get_soup(dir_html)
    img_page_url = _get_dir_img_page_url(l, dir_soup)

    # 获取相册下的图片
    for photo_web_url in img_page_url:
        try:
            _download_img_from_page(t, photo_web_url)
        except Exception as e:
            print("下载失败：" + "message:"+e)



def _download_img_from_page(t, page_url):
    dir_html = _get_html(page_url)
    dir_soup = _get_soup(dir_html)

    # 得到当前页面的图片
    main_image = dir_soup.findAll(id='bigImg')
    #print(main_image)
    if None != main_image:
        for image_parent in main_image:
            img_url = image_parent.attrs['src']
            #print(imgs)
            filename = img_url.split('/')[-1]
            print("开始下载:" + img_url + ", 保存为："+filename)
            _save_file(t, filename, img_url)



def _save_file(d, filename, img_url):
    print(img_url)
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",

    ]
    agent = random.choice(user_agents)
    headers = {'User-Agent': agent,
               'Referer': 'http://desk.zol.com.cn/1920x1080/'}
    img = requests.get(img_url,headers=headers)
    name = str(d+"/"+filename)
    try:
        with open(name, "wb") as code:
            code.write(img.content)
    except Exception as e:
        print("下载失败："+img_url + ", message:"+e)


def _get_dir_img_page_url(l, dir_soup):
    """
    获取相册里面的图片数量
    :param l: 相册链接
    :param dir_soup:
    :return: 相册图片网址
    """
    # showImg > li:nth-child(1)
    links = dir_soup.find(id='showImg')
    #print(links)
    url_list = []
    for li in links:
        lin = 'http://desk.zol.com.cn/'+li.find('a')['href']
        #print(lin)
        url_list.append(lin)
    return url_list




