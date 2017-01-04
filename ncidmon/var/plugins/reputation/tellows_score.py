#!/usr/bin/python
import sys
from lxml import html
import requests
url='https://www.tellows.it/num/' + sys.argv[1] 
#print url
page = requests.get(url)
tree = html.fromstring(page.content)
#score = tree.xpath('img[@class="scoreimage"]/text()')
score = tree.xpath('//img[@class="scoreimage"]/@alt')
score=int(score[0].split(" ")[2])
if score > 6 :
	print 1
	sys.exit(1)
else :
	print 0
	sys.exit(0)
