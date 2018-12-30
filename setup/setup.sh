
# setup virtual env
# add nginx conf
sudo service nginx reload

nano /etc/uwsgi/sites/cryptoboots.ini
# put wsgi.ini in file
sudo service uwsgi restart
