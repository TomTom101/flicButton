# flicButton

chown pi:pi fliclifx.sh && chmod +x fliclifx.sh
sudo cp fliclifx.sh /etc/init.d/
sudo update-rc.d fliclifx.sh defaults
/etc/init.d/fliclifx.sh start
