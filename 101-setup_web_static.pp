# Puppet manifest for setting up web servers for the deployment of web_static
# Install Nginx package
package { 'nginx':
  ensure => installed,
}

# Set up directories
file { '/data/web_static/releases/test':
  ensure => directory,
}

file { '/data/web_static/shared':
  ensure => directory,
}

file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html>
  <head>
    <title>AirBnB clone</title>
  </head>
  <body>
    <p>0x03. AirBnB clone - Deploy static</p>
  </body>
</html>',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
}

# Set ownership to ubuntu user and group recursively
file { '/data/':
  ensure  => directory,
  recurse => true,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "server {
    listen 80 default_server;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html;
    }
    location / {
        try_files \$uri \$uri/ =404;
    }
}",
}

# Restart Nginx service
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}

notify { 'i_am_done':
  message => 'I am done boss.',
}

