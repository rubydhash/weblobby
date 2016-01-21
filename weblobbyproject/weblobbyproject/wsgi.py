import os, os.path, sys, site

ALLDIRS = ['/usr/local/pythonenv/weblobby/lib/python2.6/site-packages', '/usr/local/pythonenv/weblobby/weblobbyproject']

# Remember original sys.path.
prev_sys_path = list(sys.path) 

# Add each new site-packages directory.
for directory in ALLDIRS:
  site.addsitedir(directory)

# Reorder sys.path so new directories at the front.
new_sys_path = [] 
for item in list(sys.path): 
    if item not in prev_sys_path: 
        new_sys_path.append(item) 
        sys.path.remove(item) 
sys.path[:0] = new_sys_path 

sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'weblobbyproject.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
