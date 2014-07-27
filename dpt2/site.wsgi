import os
import sys
import imp

sys.path.append(os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
imp.find_module('settings')
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
