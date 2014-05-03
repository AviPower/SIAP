"""
WSGI config for SIAP project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SIAP.settings")

#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()

import os
import sys

sys.path.append('/home/alvarenga/PycharmProject/SIAP')
sys.path.append('/home/alvarenga/PycharmProject/SIAP/SIAP/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SIAP.settings")


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()