# Author: tntC4stl3
# Name: ComicDownloader.py
# Special thanks to zhairen
# https://groups.google.com/forum/?fromgroups=#!topic/python-cn/ro8vr-Gqvjk

# -*- coding: utf-8 -*-
import re, os, time
import chardet
import urllib2, json
import Queue, threading
from bs4 import BeautifulSoup

comic_name = "OnePiece"

# get current directory
global root_path, store_path
root_path = os.getcwd()
store_path = root_path + '\\%s' % comic_name
# Create a folder in the directory of the script
try:
    os.mkdir(store_path)
except:
    print "The folder is already existed."
        
thread_num = 15
jobs = Queue.Queue(0)

class MultiChapter(threading.Thread):
    """multi threading"""
    def __init__(self, chapter_list):
        self._chapter_list = chapter_list
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self._chapter_list.empty():
                break
            else:
                self.chapter = self._chapter_list.get(timeout = 3)
                chapter_path = store_path + '\\%s' % self.chapter[0]
                print "create %s" % chapter_path
                os.mkdir(chapter_path)
                self._pic_url(self.chapter)

    def _pic_url(self, chapter_list):
        print "%s begin" % self.name

        # 10.28
        # three attemps to open chapter page
        attemps = 1
        while attemps <= 3:
            try:
                content = urllib2.urlopen(chapter_list[1], timeout = 120).read()
                m = re.search('var pages = pages = .*', content)
                if m:
                    break
            except:
                attemps += 1
        if attemps>3:
            return None
        
        # Find the part likes var pages = pages = '[xxx]'
        # m = re.search('var pages = pages = .*', content)
        # We only need the '[xxx]' part
        pages = re.search('\[.*\]', m.group(0))

        # need to know the suffix
        if re.search('\.jpg', m.group(0)):
            flag = 1
        else:
            flag = 2
        
        # Thank google python-cn
        self.jpg_list = json.loads(pages.group(0))
        self._download_jpg(self.jpg_list, chapter_list[0], flag)    

    # Download jpgs
    def _download_jpg(self, jpg_list, name, flag):
        root_url = 'http://imgfast.manhua.178.com/'
        num = 0
        
        if flag == 1:
            suffix = ".jpg"
        else:
            suffix = ".png"
        
        for url in jpg_list:
            jpg_url = root_url + url.replace('\/','/')
            
            # do URI encode to jpg_url, do not encode :?=/
            # 10.28 add encode('utf8') to ensure the url can be opened by urlopen
            jpg_url = urllib2.quote(jpg_url.encode('utf8'),":?=/")
            
            attemps = 1
            while attemps <= 3:
                f = open('OnePiece\%s\%d%s' %(name, num, suffix), 'wb')
                try:
                    content = urllib2.urlopen(jpg_url, timeout=120).read()
                    if content:
                        f.write(content)
                        break
                except:
                    print "Open %s failed %d" %(jpg_url, attemps)
                    attemps += 1
            #except:
            #    print "Download %s failed!" % jpg_url
            f.close()
            num += 1
        print "%s done!" % self.name

# Get all released OnePiece chapter
def chapter_url(url):
    content = urllib2.urlopen(url, timeout=10).read()
    
    # detect the encode of the site
    code = chardet.detect(content)
    
    # get the part contains the chapter urls
    char_part = BeautifulSoup(content, from_encoding=code['encoding'])
    char_part =  char_part('div', class_='cartoon_online_border')

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
        t = MultiChapter(jobs).start()
        time.sleep(3)
            
if __name__ == "__main__":
    chapter_url('http://manhua.178.com/haizeiwang')
