#!/usr/bin/python
import sys
from lxml import html
import requests
url='https://it.unknowndial.com/numero/' + sys.argv[1] 
#print url
page = requests.get(url)
tree = html.fromstring(page.content)
#score = tree.xpath('img[@class="scoreimage"]/text()')
score = tree.xpath('//span[@class="red"]/text()')
if len(score) > 1 :
	print 1 
	sys.exit(1)
else : 
	print 0
	sys.exit(0)
