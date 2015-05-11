#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""changeExperimentName.py: Change the name of an experiment in the PDM service."""

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

# The old name of an experiment in the database
exp_id = 'test_exp_01'

# The new name of an experiment in the database
new_name = 'test_exp_02'

req = RequestWithMethod(apiURL + 'evarilos/metrics/v1.0/database/' + db_id + '/experiment/' + exp_id, 'PATCH', headers={"Content-Type": "application/json"}, data = new_name)
resp = urllib2.urlopen(req)
response = json.loads(resp.read())
print response