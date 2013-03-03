sudo uwsgi -s /var/lib/uwsgi_sock/uwsgi.sock --chdir /usr/local/shared/DataAnywhere/occupysandy/ReST -w flask_os_data:app --touch-reload . --daemonize /var/log/uwsgi.log --chmod-socket 666
