uwsgi --stop /var/run/uwsgi-tapjoysite.pid
sleep 10
uwsgi -x uwsgi.xml
