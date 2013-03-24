---
layout: home
title: Server Setup
---

# Server Setup

## Security first

These are optional but very highly recommended tools and tips to secure your server from standard attacks. 

### Add a common group

A common group allows you and other developers to work together easily on the same machine, on common files. 

> groupadd dev

### Set umask

A group-writable umask allows other developers in your group to write to your files. 

> edit /etc/bashrc

    if [ $UID -ne 0 ]; then
       umask 002

### Add your username (and other developers usernames). Set a default password.

> adduser -g dev your_username && passwd your_username

> adduser -g dev someone_else && passwd someone_else

Notice how the users belong to the group dev. This is important.

### Change the sudo file

This allows you to execute root commands without having to know the root password.

> yum -y install sudo

> vi /etc/sudoers

> your_username	ALL=(ALL) 	ALL

> esc, then :w!

> \:q

Note that ALL allows you to do all commands without restriction. You can restrict other user's access. See the sudo command syntax for details.

### denyhosts

> yum -y install denyhosts (or apt-get install denyhosts for Ubuntu/Debian OS)

> edit /etc/denyhosts.conf

> set this variable/value: BLOCK_SERVICE = ALL

> service denyhosts restart

### fail2ban

> yum -y install fail2ban (or apt-get install fail2ban for Ubuntu/Debian OS)

> edit 

### htpasswd

We\'re going to use this a bit later (in nginx), so install it at this time.

> yum -y install httpd-tools (or apt-get install apache2-tools)

## Application setup

Create a directory under /usr/local. Call it DA, DataAnywhere, app, whatever you wish:

> sudo mkdir /usr/local/DA

> sudo chmod -R g+w /usr/local/DA

> sudo chgrp dev /usr/local/DA

Set an htpasswd user/password for each person/org which will have access:

> cd /usr/local/DA

> sudo htpasswd ./htpa

1. [Bash history of server setup](https://github.com/dhornbein/DataAnywhere/blob/master/occupysandy/system/latest_hist.txt)

*More coming soon*
