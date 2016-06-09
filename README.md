# flicButton

chown pi:pi flix.sh && chmod +x flix.sh
sudo cp flix.sh /etc/init.d/
sudo update-rc.d flix.sh defaults
sudo /etc/init.d/flix.sh start
