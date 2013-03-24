---
layout: home
title: Server Setup
---

# Server Setup

## Security first

These are optional but very highly recommended tools and tips to secure your server from standard attacks. 

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


Check log paths in the /etc/fail2ban/jail.conf file, and make sure they point to /var/log/nignx, /var/log/secure, etc. accoring to what is being parsed. If these are incorrect, fail2ban should issue a warning upon startup, but check to be sure. fail2ban uses regex filters to look for attack patterns in log files, so it is essentail that it is looking in the right places. 

Follow the instructions to add nginx to fail2ban: http://serverfault.com/questions/420895/how-to-use-fail2ban-for-nginx

If this is too complex, leave fail2ban as-is, and at least it will protect against default attacks.

Restart fail2ban: 

	/etc/init.d/fail2ban restart

### htpasswd

We're going to use this a bit later (in nginx), so install it at this time.

	yum -y install httpd-tools (or apt-get install apache2-tools)

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

