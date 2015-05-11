#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""createNewDatabase.py: Create a new database in the PDM service."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2015, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"

import sys
import urllib2
import json

# The URL where server listens
apiURL = 'http://localhost:5001/'

# Database name 
db_id = 'test_db'

req = urllib2.Request(apiURL + 'evarilos/metrics/v1.0/database', headers={"Content-Type": "application/json"}, data = db_id)
resp = urllib2.urlopen(req)
response = json.loads(resp.read())
print response	