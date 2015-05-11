#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""deleteExperiment.py: Delete an experiment in the PDM service."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2015, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"

import sys
import urllib2
import json
from generateURL import RequestWithMethod

# The URL where server listens
apiURL = 'http://localhost:5001/'

# The name of a database
db_id = 'test_db'

# The name of an experiment in the database
exp_id = 'test_exp'

req = RequestWithMethod(apiURL + 'evarilos/metrics/v1.0/database/' + db_id + '/experiment/' + coll_id, 'DELETE', headers={"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
response = json.loads(resp.read())
print response	