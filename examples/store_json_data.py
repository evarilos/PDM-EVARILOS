#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""store_json_data.py: Store the json data in an experiment in the PDM service."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2015, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"

import sys
import urllib2
import json
import time
from generateURL import RequestWithMethod

# The URL where server listens
apiURL = 'http://localhost:5001/'

# The name of a database

db_id = 'test_db'

# The name of an experiment in the database
exp_id = 'test_exp'

# Open file for reading
file_name = 'data/<filename>'
f = open(file_name, 'r')

obj = json.dumps(json.loads(f.read()))

req = RequestWithMethod(apiURL + 'evarilos/metrics/v1.0/database/' + db_id  + '/experiment/' + exp_id, 'POST', headers={"Content-Type": "application/json"}, data = obj)
response = urllib2.urlopen(req)
message = json.loads(response.read())
print message
