#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# apt-get twisted-twisted  or  apt-get python-twisted-core
from twisted.web import resource

# application
from .cidentry import CIDEntry
from .misc import CONFIG

import os
from urlparse import urlparse

import datetime

class CallListServer(resource.Resource):
    
    isLeaf = True
    
    
    def __init__(self):
        self._header = ""
        self.update_call_list()
    
    

    def update_call_list(self, call_list=None):
        '''update rendered HTML list'''
        blacklistlink =""
        whitelistlink =""
        
        if not call_list:
            self._rendered_call_list = ''
        else:
            self._rendered_call_list = '<ol reversed>'
            
            for entry in reversed(
                    sorted(call_list)):
                number = entry.get_number()
                if number.isdigit():
                    # we have a telephone number: make it clickable
                    tel = '<a href="tel:{0}">{1}</a>'.format(
                        number, number)
                    caller = entry.resolve_number()
                    if caller is None:
                        # the caller is unknown: build lookup links
                        caller = 'Check caller reputation: &#10140;&nbsp;' + ', '.join(
                            '<a href="{0}" target="_blank">{1}</a>'.format(
                                url.format(number=number), name)
                            for name, url in CONFIG['NUMBER_LOOKUP_PAGES'])
                        if number in open('/usr/ncidmon/ncidmon/var/lists/it/ncidmon.blacklist').read():
			    blacklistlink = 'Remove from blacklist:&nbsp;<a href="/?number=' + number +'&action=rem&listfile=blacklist">' + number + '</a>'
                            print number + " Trovato in blacklist"
                        else:
			    blacklistlink = 'Add to blacklist:&nbsp;<a href="/?number=' + number +'&action=add&listfile=blacklist">' + number + '</a>'
                            if number in open('/usr/ncidmon/ncidmon/var/lists/it/ncidmon.whitelist').read():
			        whitelistlink = 'Remove from whitelist:&nbsp;<a href="/?number=' + number +'&action=rem&listfile=whitelist">' + number + '</a>'
                                print number + " Trovato in whitelist"
                                blacklistlink =""
                            else:
			        whitelistlink = 'Add to whitelist:&nbsp;<a href="/?number=' + number +'&action=add&listfile=whitelist">' + number + '</a>'
                else:
                    # no telephone number, unknown caller, lookup not possible
                    tel = number  # 'Anonymous' or similiar
                    caller = '&mdash;'   # '---' or similiar
                
                self._rendered_call_list += '''
                    <li>
                        {0}
                        <p><name>{1}</name></p>
                        <p><date>{2}</date> <time>{3}</time></p>
                        <p><name>{4}</name></p>
                        <p><name>{5}</name></p>
                    </li>
                    '''.format(
                    tel, caller, entry.get_pretty_date(),
                    entry.get_pretty_time(), blacklistlink, whitelistlink)
                blacklistlink ="" 
                whitelistlink =""

            self._rendered_call_list += '</ol>'
 
    
    def render_GET(self, request):
	if request.method == 'GET':     
            if request.args.get('action') is not None :
                 if request.args.get('action')[0] == "add":
    	            number = request.args.get('number')
	            listfile = request.args.get('listfile')
                    print "Adding number to " + str(listfile[0])  + " " + str(number[0])
	            try:
	                fp = open("/usr/ncidmon/ncidmon/var/lists/it/ncidmon." + str(listfile[0]) ,'a')
                        os.system("/usr/bin/ncidutil '/etc/ncid/ncidd." + str(listfile[0]) + "' " + str(listfile[0].title()) + " add " + str(number[0]) + " '#Block caller added from ncidmonweb'")
    	            except IOError as e:
                        if e.errno :
                            print "File access error"
                        raise
	            else:
                        with fp:
                            fp.write(number[0]) 
                            fp.write("\n")
		            fp.close() 
	    if request.args.get('action') is not None :
        	    if request.args.get('action')[0] == "rem" :
                        print "Action=REM"
	                number = request.args.get('number')
	                listfile = request.args.get('listfile')
                        print "Removing number from blacklist " + str(number[0])
	                try:
	                    fp = open("/usr/ncidmon/ncidmon/var/lists/it/ncidmon." + str(listfile[0]) ,'r')
                            os.system("/usr/bin/ncidutil '/etc/ncid/ncidd." + str(listfile[0]) + "' " + str(listfile[0].title()) + " remove " + str(number[0]))
    	                except IOError as e:
                            if e.errno :
                                print "File access error"
                            raise
	                else:
                            with fp:
                                lines = fp.readlines()
                                fp.close()
                                fp = open("/usr/ncidmon/ncidmon/var/lists/it/ncidmon." + str(listfile[0]) ,"w")
                                for line in lines:
                                    if line!=str(number[0])+"\n":
                                        fp.write(line)
                                fp.close()

        return PAGE_HEADER + str(datetime.datetime.now()) + self._rendered_call_list + PAGE_FOOTER


PAGE_HEADER = '''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Call list</title>
        <style>
            div {
              margin: 10px
            }

            h2 {
              font: 400 32px/1.5 Helvetica, Verdana, sans-serif;
              margin: 0;
              padding: 0;
            }
            
            ol li {
              position: relative;
              font: bold italic 12px/1.5 Helvetica, Verdana, sans-serif;
              padding-left: 20px;
              margin-bottom: 20px;
              border-left: 1px solid #999;
            }
            
            ol li p {
              font: 10px/1.5 Helvetica, sans-serif;
              padding-left: 40px;
              color: #000;
            }
            
            a[href] {
                font: 12px/1.5 Helvetica, sans-serif;
            }
            
            a[href^="tel:"] {
                color: tomato;
                font: 14px/1.5 Helvetica, sans-serif;
            }
            
            a[href^="tel:"]:before {
                content: "\\260E";
            }
            
            name {
              font: 16px/1.5 Helvetica, sans-serif;
            }
            
            date {
              font: 12px/1.5 Helvetica, sans-serif;
              color: #555;
            }
            
            time {
              font: 12px/1.5 Helvetica, sans-serif;
              color: #888;
            }
        </style>
    </head>
    <body>
        <div>
            <h2>Recent incoming calls</h2>
'''

PAGE_FOOTER = '''
        </div>
    </body>
</html>
'''

