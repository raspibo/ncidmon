#!/usr/bin/env python
# -*- coding: utf8 -*-

# system
from math import floor, log10


CONFIG = {
    'DEBUG'                 : False,           # print debug output?
    'NCID_HOST'             : 'localhost',   # name or IP of NCID server
    'NCID_PORT'             : 3333,            # configured NCID port
    'CONNECT_TIMEOUT'       : 5.0,             # connect timeout in seconds (currently unused)
    'HTTP_HOST'             : 'localhost',     # interface for internal call list web server
    'HTTP_PORT'             : 8080,            # port for internal call list web server
    'NCID_CLIENT_NAME'      : 'NCIDmon',       # name of this client for broadcasts
    'NOTIFICATION_ICON'     : r'phone',        # name of icon in notification windows
    'NUMBER_LOOKUP_PAGES'   : (                # (name, url) tuples for number lookup
        # replace search number in lookup URL by '{number}'
        (r'inelenco', r'http://www.inelenco.com/?dir=cerca&cerca={number}'),
        (r'tellows', r'https://www.tellows.it/num/{number}'),
        (r'it.unknownphone.com', r'http://it.unknownphone.com/search.php?num={number}'),
	(r'chistachiamando.it',r'https://www.chistachiamando.it/numero-telefono/{number}'), 
	(r'it.unknowndial.com',r'https://it.unknowndial.com/numero/{number}'), 
    ),
    'MAX_LOG_OUTPUT'        : 20,               # recent log entries count to output
    # TBD limit by days
    
    'DISABLE_NOTIFICATIONS' : False,
    'LISTEN'                : False,

}


def dprint(*args):
    if CONFIG['DEBUG']:
        print '[DEBUG]', ' '.join(str(a) for a in args)


def get_digits_count(value):
    return int(floor(log10(abs(int(value)))) + 1)
