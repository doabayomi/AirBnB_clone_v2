#!/usr/bin/env bash
# Server setup script
if ! command -v nginx &> /dev/null
then
	sudo apt-get -y update
	sudo apt-get -y install nginx
	ufw allow 'Nginx HTTP'
	sudo sed -i "/listen 80 default_server;/a add_header X-Served-By $HOSTNAME;" /etc/nginx/sites-available/default
	sudo service nginx restart
fi

mkdir -p /data/web_static/releases/test/ /data/web_static/shared/

# Dummy HTML file
touch /data/web_static/releases/test/index.html
echo "<html><head></head><body>HBNB Setup</body></html>" > /data/web_static/releases/test/index.html

# Symbolic link 
ln -sf /data/web_static/releases/test/ /data/web_static/current

#Give ownership to user and group "ubuntu"
sudo chown -R ubuntu:ubuntu /data/

nginx_config="/etc/nginx/sites-available/default"
web_static_path="/data/web_static/current"

# Check if the location block already exists in the configuration
if ! grep -q "location /hbnb_static/" "$nginx_config"
then
	# Use awk to insert the location block inside the server block
	sudo awk -v web_static_path="$web_static_path" '
		/server_name _;/ {
			print $0
			getline
			print "        location /hbnb_static/ {"
			print "            alias " web_static_path "/;"
			print "            index index.html index.htm;"
			print "        }"
			next
		}
		{ print $0 }
	' "$nginx_config" | sudo tee "$nginx_config" > /dev/null

fi
sudo systemctl restart nginx
