#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""storeData.py: Store the data in an experiment in the PDM service."""

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
import protobuf_json
import experiment_results_pb2
from generateURL import RequestWithMethod

# The URL where server listens
apiURL = 'http://localhost:5001/'

# The name of a database

db_id = 'test_db'

# The name of an experiment in the database
exp_id = 'test_exp'

experiment_results = experiment_results_pb2.Experiment() 
experiment_results.timestamp_utc = int(time.time())
experiment_results.experiment_id = 1

# Define the scenario of the experiment
experiment_results.scenario.testbed_label = 'test_testbed' 				# Label the testbed 
experiment_results.scenario.testbed_description = 'test'                # Give the description
experiment_results.scenario.experiment_description = 'test'             # Describe experiment
experiment_results.scenario.receiver_description = 'test'               # Describe receiver(s)
experiment_results.scenario.sender_description = 'test'                 # Describe your sender(s)
experiment_results.scenario.interference_description = 'test'           # Describe interference scenario

experiment_results.primary_metrics.accuracy_error_2D_average = 0.0;       # Average 2D error of the geo. accuracy of all points in the experiment
experiment_results.primary_metrics.accuracy_error_2D_variance = 0.0;      # 2D error variance of the geo. accuracy of all points in the experiment
experiment_results.primary_metrics.accuracy_error_2D_min = 0.0;           # Min 2D error of the geo. accuracy of all points in the experiment
experiment_results.primary_metrics.accuracy_error_2D_max = 0.0;           # Max 2D error of the geo. accuracy of all points in the experiment
experiment_results.primary_metrics.accuracy_error_2D_median = 0.0;
experiment_results.primary_metrics.accuracy_error_2D_rms = 0.0;
experiment_results.primary_metrics.accuracy_error_2D_75_percentile = 0.0;
experiment_results.primary_metrics.accuracy_error_2D_90_percentile = 0.0;
experiment_results.primary_metrics.accuracy_error_3D_average = 0.0;       # Average 3D error of the geo. accuracy of all points in the experiment
experiment_results.primary_metrics.accuracy_error_3D_variance = 0.0;      # 3D error variance of the geo. accuracy of all points in the experiment
experiment_results.primary_metrics.accuracy_error_3D_min = 0.0;           # Min 3D error of the geo. accuracy of all points in the experiment
experiment_results.primary_metrics.accuracy_error_3D_max = 0.0;           # Max 3D error of the geo. accuracy of all points in the experiment
experiment_results.primary_metrics.accuracy_error_2D_median = 0.0;
experiment_results.primary_metrics.accuracy_error_2D_rms = 0.0;
experiment_results.primary_metrics.accuracy_error_2D_75_percentile = 0.0;
experiment_results.primary_metrics.accuracy_error_2D_90_percentile = 0.0;
experiment_results.primary_metrics.room_accuracy_error_average = 0.0;     # Average room accuracy error
experiment_results.primary_metrics.latency_average = 0.0;                 # Average latency
experiment_results.primary_metrics.latency_variance = 0.0;                # Latency variance
experiment_results.primary_metrics.latency_min = 0.0;                     # Latency min
experiment_results.primary_metrics.latency_max = 0.0;                     # Latency max
experiment_results.primary_metrics.latency_median = 0.0;
experiment_results.primary_metrics.latency_rms = 0.0;
experiment_results.primary_metrics.latency_75_percentile = 0.0;
experiment_results.primary_metrics.latency_90_percentile = 0.0;


obj = json.dumps(protobuf_json.pb2json(experiment_results))

req = RequestWithMethod(apiURL + 'evarilos/metrics/v1.0/database/' + db_id  + '/experiment/' + exp_id, 'POST', headers={"Content-Type": "application/json"}, data = obj)
response = urllib2.urlopen(req)
message = json.loads(response.read())
print message
