#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""changeExperiment.py: Change the data in an experiment in the PDM service."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2015, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"

import sys
import urllib2
from generateURL import RequestWithMethod
import json

# The URL where server listens
apiURL = 'http://localhost:5001/'

# The name of the database
db_id = 'test_db'

# The name of an experiment in the database
exp_id = 'test_exp'

obj = json.dumps({"experiment_description": 'test_01'})

req = RequestWithMethod(apiURL + 'evarilos/metrics/v1.0/database/' + db_id + '/experiment/' + exp_id, 'PATCH', headers={"Content-Type": "application/json"}, data = obj)
resp = urllib2.urlopen(req)
print json.loads(resp.read())