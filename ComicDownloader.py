# Author: tntC4stl3
# Name: OnePiece.py

# -*- coding: utf8 -*- 
import urllib2
from bs4 import BeautifulSoup
import re, os
import chardet

# get current directory
global root_path
root_path = os.getcwd()

# Download jpgs
def download_jpg(jpg_list, name):
    root_url = 'http://imgfast.manhua.178.com/'
    num = 0
    path = root_path + '/OnePiece/%s/' % name
    os.mkdir(path)
    for url in jpg_list:
        jpg_url = root_url + url.replace('\/','/')
        print jpg_url
        content = urllib2.urlopen(jpg_url).read()
        f = open('OnePiece\%s\%d.jpg' %(name, num), 'wb')
        f.write(content)
        f.close()
        num += 1

# Get all jpg urls in one chapter    
def jpg_url(chapter_list):
    for i in range(len(chapter_list)):
        content = urllib2.urlopen(chapter_list[i][1]).read()

        # Find the part contains the jpg relative urls
        m = re.search('var pages = pages = .*', content)
        test = re.findall(r'o.*jpg', m.group(0))
        jpg_list = test[0].split('","')
        
        download_jpg(jpg_list, chapter_list[i][0])

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
    jpg_url(chapter_list)
            
if __name__ == "__main__":
    chapter_url('http://manhua.178.com/haizeiwang/')
