NCIDmon
=======

Basic NCID command line client written in Python 2
This is a fork of https://github.com/shrick/ncidmon with some chenges for italian market.

**SYNOPSIS**

    ncidmon.py [OPTIONS]
    python2 -m ncidmon [OPTIONS]

**DESCRIPTION**

Retrieve call log, notify recent call and optionally listen/notify for
incoming calls. Built-in webserver provides list of all recent calls.

Optional arguments:

    <host>:<port>

Name or address and port or service name of NCID server.

    --listen

Listen for incoming calls. Can be used for running in background, e.g.
automatically started in user session. Recent calls are shown on standard
output, with notifications enabled also per on screen notification.
A web-based call list is also provided, per default on [http://localhost:8080](http://localhost:8080).

    --http <host>:<port>
    
Name or address and port or service name to use for internal call list
web server. The call list is only available in listening mode and if the
specified port can be bound.

    --disable-notifications

Show no notifcations for recent call and incoming calls. To be used for instant
checks of recent calls. With notifications enabled recent and/or incoming call
information are displayed per popup. The amount of information depends on the
capabilities of your local notification OSD server.

    -d, --debug

Print debug output.

    -h, --help

Show usage and exit.

**DEPENDENCIES**

- twisted (https://twistedmatrix.com/trac/)
- pynotify (only if notifications are not disabled per command line)

**COMPATIBILITY**

- developed with Python 2.7 (last version check returned 2.7.6)

**TODO**

- [ ] limit log entries output on console by configurable time span
- [ ] restructure (file and folder hierarchy)
- [x] command line options for NCID and HTTP server addresses
- [ ] maybe two twisted protocol implementations for simple request and continuous listening mode
- [ ] support wildcard numbers (corporate telephone system)
- [ ] i18n using gettext
- [ ] direct execution from zip file
- [x] config command line options (using arparse) overriding application defaults
- [ ] workaround EasyBox day/month inversion
- [ ] python setup infrastructure
- [ ] porting to Python 3
- [ ] connection timeout

**INSTALLATION**

If you want to use as daemon, put files under system dir es: /usr/ncidmon/

    cd /usr
    git clone https://github.com/raspibo/ncidmon

add link to systemd startup daemons

    sudo ln -s /usr/ncidmon/ncidmon/ncidmon.service /lib/systemd/system/ncidmon.service
    sudo systemctl enable ncidmon.service
    sudo systemctl start ncidmon.service

**BLACKILIST AND WHITELIST UTILITY**

Control blacklist and whitelist with 2 methods:

*MANUAL BY WEB INTERFACE* 

You can control call list on web interface and add a caller on black or white list files under ncidmon/ncidmon/var/plugins/. 
These files are used to populate /etc/ncidd/ncidd.blacklist or /etc/ncidd/ncidd.whitelist

*REPUTATION SCRIPTS*

Under dir reputation ncidmon/ncidmon/var/plugins/reputation/  you can find some useful script to determine reputation of unknown caller. 
Some of these use lxml library, install following instruction on library site http://lxml.de/

You can add files to integrate more functions, place it on this dir.

Every reputation script can exit whit 0 or 1 value. 
1 value indicate negative reputation found 
0 value indicate positive or no negative reputation

If one of plugins exit whit 1 value is automatically added on /etc/ncidd/ncidd.blacklist else no action is taken.

If a caller is added on blacklist the hang is active from the next call.

A simple and particular script....   

    #!/usr/bin/python
    import sys
    print 1
    sys.exit(1)

useful to add every caller to blackilist after first call.
