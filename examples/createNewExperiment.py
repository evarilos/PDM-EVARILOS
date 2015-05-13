#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""createNewExperiment.py: Create a new experiment in the PDM service."""

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

# The name of the experiment in the database
exp_id = 'test_exp'

req = urllib2.Request(apiURL + 'evarilos/metrics/v1.0/database/' + db_id  + '/experiment', headers={"Content-Type": "application/json"}, data = exp_id)
resp = urllib2.urlopen(req)
response = json.loads(resp.read())
print response	