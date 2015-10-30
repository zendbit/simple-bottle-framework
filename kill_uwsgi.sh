ps aux | grep 'uwsgi.ini' | awk '{print $2}' | xargs -r kill -9
