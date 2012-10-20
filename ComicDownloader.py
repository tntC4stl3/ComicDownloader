# Author: tntC4stl3
# Name: ComicDownloader.py

# -*- coding: utf8 -*-
import re, os
import chardet
import urllib2, threading
import Queue
from bs4 import BeautifulSoup

# get current directory
global root_path
root_path = os.getcwd()

comic_name = "OnePiece"

thread_num = 10
jobs = Queue.Queue(0)

class MultiChapter(threading.Thread):
    """multi threading"""
    def __init__(self, chapter_list):
        self._chapter_list = chapter_list
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self._chapter_list.qsize() > 0:
                chapter = self._chapter_list.get()
                jpg_url(chapter)
            else:
                break


    

# Download piscs
def download_pics(pic_list, name, flag):
    root_url = 'http://imgfast.manhua.178.com/'
    num = 1

    if flag == 1:
        suffix = ".jpg"
    elif flag == 2:
        suffix = ".png"
        
    root_path = root_path + '\\%s' % comic_name
    os.mkdir(root_path)
    path = root_path + '\\%s' % name
    os.mkdir(path)
    for url in jpg_list:
        jpg_url = root_url + url.replace('\/','/')
        print jpg_url
        content = urllib2.urlopen(jpg_url).read()
        f = open('OnePiece\%s\%d%s' %(name, num, suffix), 'wb')
        f.write(content)
        f.close()
        num += 1

# Get all jpg urls in one chapter    
def jpg_url(chapter_list):
    content = urllib2.urlopen(chapter_list[1]).read()

    # Find the part contains the jpg relative urls
    m = re.search('var pages = pages = .*', content)

    # some pictures are .jpg, some are .png
    if re.findall('\"\w.*jpg\"', m.group(0)):
        test = re.findall('\"\w.*jpg\"', m.group(0))
        flag = 1
    else:
        test = re.findall('\"\w.*png\"', m.group(0))
        flag = 2
    pic_list = test[0].replace('"','').split(',')
        
    download_pic(pic_list, chapter_list[0], flag)

"""
# Get all jpg urls in one chapter    
def jpg_url(chapter_list):
    for i in range(len(chapter_list)):
        content = urllib2.urlopen(chapter_list[i][1]).read()

        # Find the part contains the jpg relative urls
        m = re.search('var pages = pages = .*', content)
        test = re.findall(r'o.*jpg', m.group(0))
        jpg_list = test[0].split('","')
        
        download_jpg(jpg_list, chapter_list[i][0])"""

"""
# Get all released OnePiece chapter
def chapter_url(url):
    try:
        content = urllib2.urlopen(url, timeout = 10).read()
    except urllib2.URLError, e:
        raise MyException("There was an error: %r" % e)
    
    # detect the encode of the site
    code = chardet.detect(content)
    
    # get the part contains the chapter urls
    char_part = BeautifulSoup(content, from_encoding=code['encoding'])
    char_part =  char_part('div', class_='cartoon_online_border')

    # get the chapter name and url, store in chapter_list
    # chapter[0][0] means chapter 1's name
    # chapter[0][1] means chapter 1's url
    chapter_list = []
    for part in char_part:
        soup = BeautifulSoup(str(part))
        for link in soup.find_all('a'):
            chapter = []
            chapter.append(link.get_text())
            chapter.append(link.get('href'))
            chapter_list.append(chapter)
    jpg_url(chapter_list)"""

# Get all released OnePiece chapter
def chapter_url(url):
    try:
        content = urllib2.urlopen(url, timeout = 10).read()
    except urllib2.URLError, e:
        raise MyException("There was an error: %r" % e)
    
    # detect the encode of the site
    code = chardet.detect(content)
    
    # get the part contains the chapter urls
    char_part = BeautifulSoup(content, from_encoding=code['encoding'])
    char_part =  char_part('div', class_='cartoon_online_border')

    # get the chapter name and url, store in chapter_list
    # chapter[0][0] means chapter 1's name
    # chapter[0][1] means chapter 1's url
    chapter_list = []
    for part in char_part:
        soup = BeautifulSoup(str(part))
        for link in soup.find_all('a'):
            chapter = []
            chapter.append(link.get_text())
            chapter.append(link.get('href'))
            chapter_list.append(chapter)
    for chapter in chapter_list:
        jobs.put(chapter)
    for x in range(thread_num):
        MultiChapter(jobs).start()
            
if __name__ == "__main__":
    chapter_url('http://manhua.178.com/haizeiwang')
