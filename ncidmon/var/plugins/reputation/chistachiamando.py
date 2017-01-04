#!/usr/bin/python
import sys
from lxml import html
import requests
url='https://www.chistachiamando.it/numero-telefono/' + sys.argv[1] 
#print url
page = requests.get(url)
tree = html.fromstring(page.content)
score = tree.xpath('//div[@class="gaugeInfo"]/strong/text()')
#score = tree.xpath('//span[@id="percent1"]/text()')
try:
	score=score[0].split(" ")[0]
except IndexError:
	score=0
if score == "negativa" :
	print 1
	sys.exit(1)
else : 
	print 0
	sys.exit(0)
