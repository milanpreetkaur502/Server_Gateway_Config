#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/usr/share/apache2/default-site/htdocs/Gateway_Manager")

from Gateway_Manager import app as application
application.secret_key = 'Add your secret key'
