__author__ = 'ads'
from string import Template
import sys

template_file = open('nginx_conf_template')
src = Template(template_file.read())
domain = sys.argv[1]
d = {'domain': domain, 'uri': "$uri", 'x': "$", 'document_root': "$document_root",
     'fastcgi_script_name': "$fastcgi_script_name"}
result = src.substitute(d)
print result