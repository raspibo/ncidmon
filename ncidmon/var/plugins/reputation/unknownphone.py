#!/usr/bin/python
import sys
from lxml import html
import requests
url='http://it.unknownphone.com/search.php?num=' + sys.argv[1] 
#print url
page = requests.get(url)
tree = html.fromstring(page.content)
#score = tree.xpath('img[@class="scoreimage"]/text()')
score = tree.xpath('//div[@class="comment_content"]/text()')
if len(score) > 0 :
	print 1
	sys.exit(1)
else : 
	print 0
	sys.exit(0)
