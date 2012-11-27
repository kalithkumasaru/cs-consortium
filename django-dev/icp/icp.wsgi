import os
import sys

path = '/var/django-dev/'
if path not in sys.path:
	sys.path.append(path)
path = '/var/django-dev/icp'
if path not in sys.path:
	sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'icp.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

