__author__ = 'ads'
# !/usr/bin/env python

import apt
import sys
import os
import lsb_release
from string import Template

release = lsb_release.get_distro_information()['CODENAME']
os.system(
    "echo \"deb http://ppa.launchpad.net/nginx/stable/ubuntu " + release + " main\" | sudo tee /etc/apt/sources.list.d/nginx-stable.list")
os.system("apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C300EE8C")
os.system("apt-get update")
# Mysql Password
while True:
    mysql_pass = raw_input("MySql password >")
    confirm_mysql_pass = raw_input("Confirm Mysql password >")
    if mysql_pass == confirm_mysql_pass:
        os.system("sudo debconf-set-selections <<< \'mysql-server mysql-server/root_password password \'" + mysql_pass)
        os.system(
            "sudo debconf-set-selections <<< \'mysql-server mysql-server/root_password_again password \'" + mysql_pass)
        break
    else:
        print "Sorry , Passwords do not match, try again"

# List of packages you want to install
packages_to_install = ["mysql-server", "php5-mysql", "nginx", "php5-fpm"]

cache = apt.cache.Cache()
cache.update()

for package_name in packages_to_install:
    package = cache[package_name]
    if package.is_installed:
        print "{package} already installed".format(package=package)
    else:
        package.mark_install()
    try:
        cache.commit()
    except Exception, arg:
        print >> sys.stderr, "Sorry, package installation failed [{err}]".format(err=str(arg))

# Packages installed

# GETTING DOMAIN NAME
domain_name = raw_input("domain_name >")
os.system("echo \"127.0.0.1     \"" + domain_name)

# PHP config Setup

os.system("sed \'s/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/\' /etc/php5/fpm/php.ini")
# os.system("sed \'s/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/\' /etc/php5/fpm/pool.d/www.conf")
os.system("service php5-fpm restart")
# PHP done

# WordPress config Setup
os.system("wget http://wordpress.org/latest.tar.gz")
os.system("tar -xzvf latest.tar.gz")
os.system("chmod 744 database.sh")
os.system("bash database.sh " + mysql_pass)
# Leaving wordpress details for now

# continuing
os.system("mkdir -p /usr/share/nginx/html")
os.system("cp -r ~/wordpress/* /usr/share/nginx/html")
os.system("chown www-data:www-data /usr/share/nginx/html/* -R ")
os.system("usermod -a -G www-data root")
os.system("cp /etc/nginx/sites-available/default /etc/nginx/sites-available/wordpress")
# wordpress shit finished

# Nginx config setup
os.system("mv /etc/nginx/sites-enabled/default /etc/nginx/sites-enabled/default.backup")
os.system("python nginx_conf_generator.py " + domain_name + " >> /etc/nginx/sites-available/wordpress")
os.system("chmod 744 /etc/nginx/sites-available/wordpress")
os.system("ln -s /etc/nginx/sites-available/wordpress /etc/nginx/sites-enabled/wordpress")
os.system("service nginx restart")



