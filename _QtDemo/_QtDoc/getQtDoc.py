# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-02 09:33:19'

"""

"""

import os
import time
import urllib2
try:
    from pymel.util.external.BeautifulSoup import BeautifulSoup, NavigableString
except ImportError:
    from BeautifulSoup import BeautifulSoup, NavigableString

DIR = os.path.dirname(__file__)

base_url = 'https://doc.qt.io/qtforpython/overviews/'

def retrieveLink(url,index=1,content=''):

    opener = urllib2.build_opener()
    try:
        response = opener.open(url)
    except urllib2.HTTPError:
        print ("url error",url)
        return content
    response_text = response.read()

    soup = BeautifulSoup(response_text, convertEntities='html')
    tag = next(iter(soup.findAll(['h4'])[1:]),None)
    if not tag:
        return content
    p = tag.findNext('p')
    title = p.a.string
    href = base_url + p.a.get('href')
    content += "[%s](%s)    \n" % (title,href)
    print (index,title,href)
    index += 1
    with open(os.path.join(DIR,"_overviews.md"),'w') as f:
        f.write(content)
    # if index >= 3:
    #     return content
    return retrieveLink(href,index,content)

curr = time.time()
content = retrieveLink(base_url+'animation.html')
print("elpased time :",time.time() - curr)

with open(os.path.join(DIR,"overviews.md"),'w') as f:
    f.write(content)