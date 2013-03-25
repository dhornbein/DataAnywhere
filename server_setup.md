---
layout: home
title: Server Setup
---

# Server Setup

## Security first

These are optional but very highly recommended tools and tips to secure your server from standard attacks. 
All edit commands are shown using vim syntax. Feel free to repalce it with your editor of choice,

### Add a common group

A common group allows you and other developers to work together easily on the same machine, on common files. 

 	groupadd dev

### Set umask

A group-writable umask allows other developers in your group to write to your files. 

 	edit /etc/bashrc

    if [ $UID -ne 0 ]; then
       umask 002

### Add your username (and other developers usernames). Set a default password.

	adduser -g dev your_username && passwd your_username
	adduser -g dev someone_else && passwd someone_else

Notice how the users belong to the group dev. This is important.

### Change the sudo file

This allows you to execute root commands without having to know the root password.

 	yum -y install sudo

	vi /etc/sudoers

	your_username	ALL=(ALL) 	ALL

	esc, then :w!

	:q

Note that ALL allows you to do all commands without restriction. You can restrict other user's access. See the sudo command syntax for details.

### denyhosts

	yum -y install denyhosts (or apt-get install denyhosts for Ubuntu/Debian OS)

	edit /etc/denyhosts.conf

	set this variable/value: BLOCK_SERVICE = ALL

	service denyhosts restart

### fail2ban

	yum -y install fail2ban (or apt-get install fail2ban for Ubuntu/Debian OS)

	edit /etc/fail2ban/jail.conf

Change all instances of fail2ban@example.com to your email address.

	:1,$ s/fail2ban@example.com/you@your_email.org/g

	:wq


Check log paths in the /etc/fail2ban/jail.conf file, and make sure they point to /var/log/nginx, /var/log/secure, etc. accoring to what is being parsed. If these are incorrect, fail2ban should issue a warning upon startup, but check to be sure. fail2ban uses regex filters to look for attack patterns in log files, so it is essentail that it is looking in the right places. 

Follow the instructions to add nginx to fail2ban: http://serverfault.com/questions/420895/how-to-use-fail2ban-for-nginx

If this is too complex, leave fail2ban as-is, and at least it will protect against default attacks.

Restart fail2ban: 

	/etc/init.d/fail2ban restart

### htpasswd

We're going to use this a bit later (in nginx), so install it at this time.

	yum -y install httpd-tools (or apt-get install apache2-tools)

### iptables

On Fedora, run a utility called system-config-firewall. The only open inbound ports should be 22 and 80.
On Ubuntu, the ufw utility can be used.

## Application setup

Create a directory under /usr/local. Call it DA, DataAnywhere, app, whatever you wish:

	sudo mkdir /usr/local/DA

	sudo chmod -R g+w /usr/local/DA

	sudo chgrp dev /usr/local/DA

Set an htpasswd user/password for each person/org which will have web access
Note that peopl with web access do not need shell access. They only need to be added to this file:

	cd /usr/local/DA

	# -c means CREATE: only use it the first time.
	sudo htpasswd -c ./htpasswd your_username 

	sudo htpasswd ./htpasswd another_username

### prep for nginx and uWSGI

This is necessary so that we can run uWSGI as a user other than root, and that nginx can route requests to uWSGI as they come in

	mkdir /var/log/uwsgi
	chown root:dev /var/log/uwsgi
        chmod g+w /var/log/uwsgi

	mkdir /var/lib/uwsgi_sock
	chown root:dev /var/lib/uwsgi_sock
        chmod g+w /var/lib/uwsgi_sock


### nginx

These settings can replace the default settings in /etc/nginx/conf.d/default.conf 
(or /etc/nginx/sites-enabled/default.conf depending on your system):

	#
	# The default server
	#
	server {
	    listen       80 default_server;
	    server_name  _;
	
	    #charset koi8-r;
	
	    error_page  404              /404.html;
	    location = /404.html {
	        root   /usr/share/nginx/html;
	    }
	
	    # redirect server error pages to the static page /50x.html
	    #
	    error_page   500 502 503 504  /50x.html;
	    loc	ation = /50x.html {
	        root   /usr/share/nginx/html;
	    }
	
	    send_timeout 300;
	
	    location / {
	      auth_basic            "Yes?";
	      auth_basic_user_file  /usr/local/DA/htpasswd;
	
	      include uwsgi_params;
	      uwsgi_pass unix:/var/lib/uwsgi_sock/uwsgi.sock;
	    }
	}

### uWSGI

Create a start_uWSGI.sh script. Add this to it:

	#!/bin/bash
	sudo uwsgi -s /var/lib/uwsgi_sock/uwsgi.sock --chdir /usr/local/DA -w flask_ReST:app --touch-reload . --daemonize /var/log/uwsgi/uwsgi.log --chmod-socket 666

Note that flask_ReST.py is the name of my main flask app, and the name of your app can vary if you wish.

Make this script executable:

	chmod 755 start_uWSGI.sh

Run the script (not as root! Running as root creates a security hole):

        ./start_uWSGI.sh

Errors can be found in the /var/log/uwsgi/*log file

Similarly create a stop_uWSGI.sh script:

	#!/bin/bash
	killall -9 /usr/bin/uwsgi-core 2>/dev/null
	killall -9 /usr/bin/uwsgi 2>/dev/null
	killall	 -9 uwsgi 2>/dev/null

Make this script executable:

	chmod 755 stop_uWSGI.sh

Now you are ready to start writing the main application in flask.
