#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static
# Install Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx

# Set up directories
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared
sudo touch /data/web_static/releases/test/index.html

# Create a simple HTML content for testing
echo "<html>
  <head>
    <title>AirBnB clone</title>
  </head>
  <body>
    <p>0x03. AirBnB clone - Deploy static</p>
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Set ownership to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_content="server {
    listen 80 default_server;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html;
    }
    location / {
        try_files \$uri \$uri/ =404;
    }
}"
echo "$config_content" | sudo tee /etc/nginx/sites-available/default > /dev/null

# Restart Nginx
sudo service nginx restart

echo "i am done boss."

