#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""getExperiments.py: get a list of all experiments in a database in the PDM service."""

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

# The name of the database
db_id = 'test_db'

req = urllib2.Request(apiURL + 'evarilos/metrics/v1.0/database/' + db_id  + '/experiment', headers={"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
collections = json.loads(resp.read())
print collections.keys()