__author__ = 'ads'
#!/usr/bin/env python

import apt
import sys
import os
import lsb_release

release = lsb_release.get_distro_information()['CODENAME']
os.system("echo \"deb http://ppa.launchpad.net/nginx/stable/ubuntu " + release + " main\" | sudo tee /etc/apt/sources.list.d/nginx-stable.list")
os.system("apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C300EE8C")
os.system("apt-get update")
packages_to_install = ["mysql-server","php5-mysql","nginx","php5-fpm"]

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

with open("/etc/php5/fpm/php.ini", "a") as php_config:
        php_config.write("cgi.fix_pathinfo=0")

os.system("service php5-fpm restart")
