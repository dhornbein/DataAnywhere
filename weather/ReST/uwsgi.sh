sudo uwsgi -s /var/lib/uwsgi_sock/uwsgi.sock --chdir /usr/local/DataAnywhere/DA_apps/weather/ReST -w flask_ReST:app --touch-reload . --daemonize /var/log/uwsgi.log --chmod-socket 666
