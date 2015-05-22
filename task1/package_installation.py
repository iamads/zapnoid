__author__ = 'ads'
# !/usr/bin/env python

import apt
import sys
import os
import lsb_release

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
#os.system("sed \'s/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/\' /etc/php5/fpm/pool.d/www.conf")
os.system("service php5-fpm restart")
#PHP done

# WordPress config Setup


# Nginx config setup
os.system("service nginx restart")


