#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""server_flask_evarilos_metrics.py: the PDM service."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2015, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"


import protobuf_json
from flask import Flask, jsonify
from flask import Response
from flask import abort
from flask import make_response
from flask import request, current_app
from pymongo import Connection
from flask import url_for
import experiment_results_pb2
import json
import urllib2
from functools import wraps
import pymongo
from functools import update_wrapper
from datetime import timedelta

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            try: 
	    	h['Access-Control-Allow-Methods'] = get_methods()
	    except:
		h['Access-Control-Allow-Methods'] = 'OPTIONS'
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = Flask(__name__)

#######################################################################################################
# Home - Hello World! I'm alive!!!!!
#######################################################################################################
@app.route("/")
@crossdomain(origin='*')
def hello():
    response = {'PDM Service': 'This is a prototype of the webservices for the EVARILOS project',
                'Databases': url_for("databases", _external = True)}
    return json.dumps(response)

#######################################################################################################
# Task 1: Get the list of all databases [GET]
#######################################################################################################
@app.route('/evarilos/metrics/v1.0/database', methods = ['GET'])
@crossdomain(origin='*')
def databases():

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 12345)
    except:
        return json.dumps("Unable to connect to the database!")
      
    db_names = connection.database_names() 
    db_list = {}
    for iter_id in db_names:
        if iter_id != 'local':
            db_list[iter_id] = url_for("database", db_id = iter_id, _external = True)
    return json.dumps(db_list)

#######################################################################################################
# Task 2: Get the list of all experiments in the database [GET]
#######################################################################################################
@app.route('/evarilos/metrics/v1.0/database/<db_id>/experiment', methods = ['GET'])
@crossdomain(origin='*')
def database(db_id):

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 12345)
    except:
        return json.dumps("Unable to connect to the database!")
    
    db_names = connection.database_names()
    if db_id in db_names:
        db = connection[db_id]
    else:
        return json.dumps("No such database!")

    coll_names = db.collection_names()
    coll_list = {}
    for iter_id in coll_names:
        if iter_id != 'system.indexes':
            coll_list[iter_id] = url_for("experiment", db_id = db_id, coll_id = iter_id, _external = True)
    return json.dumps(coll_list)

#######################################################################################################
# Task 4: Get the experiment [GET]
#######################################################################################################
@app.route('/evarilos/metrics/v1.0/database/<db_id>/experiment/<coll_id>', methods = ['GET'])
@crossdomain(origin='*')
def experiment(db_id, coll_id): 

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 12345)
    except:
        return json.dumps("Unable to connect to the database!")
      
    db = connection[db_id]   
    collection = db[coll_id]
    
    try:
        message_collection = collection.find_one({})
    except:
        return json.dumps("Unable to read data from the experiment!")
    
    if message_collection is None:
        return json.dumps("No data with this ID in the experiment!")

    message_collection['_id'] = str(message_collection['_id'])

    if request.data == 'protobuf':
        pb_message = protobuf_json.json2pb(experiment_results_pb2.Experiment(), message_collection)
        pb_message_string = pb_message.SerializeToString()
        return pb_message_string
    else:
        return json.dumps(message_collection)


#######################################################################################################
# Task 5: Add a message into the experiment [POST]
#######################################################################################################
@app.route('/evarilos/metrics/v1.0/database/<db_id>/experiment/<coll_id>', methods = ['POST'])
@crossdomain(origin='*')
def store_message(db_id, coll_id):
    
    #experiment_collection = experiment_results_pb2.Experiment()

    try:
        experiment_collection = json.loads(request.data)
        #print experiment_collection
        #experiment_collection.ParseFromString(request.data)
    except:
        return json.dumps('Experiment is not well defined!')

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 12345)
    except:
        return json.dumps("Unable to connect to the database!")

    db_names = connection.database_names()
    if db_id in db_names:
        db = connection[db_id]
    else:
        return json.dumps("No such database!")  
    
    coll_names = db.collection_names()
    if coll_id in coll_names:
        collection = db[coll_id]
    else:
        return json.dumps("No such experiment in the database!")
    
    try:
        collection.insert(experiment_collection)
        #collection.insert(protobuf_json.pb2json(experiment_collection))
    except:
        return json.dumps("Unable to store data into the database!")

    return json.dumps('Data stored!')

#######################################################################################################
# Task 6: Creating a new experiment in the database [POST]
#######################################################################################################
@app.route('/evarilos/metrics/v1.0/database/<db_id>/experiment', methods = ['POST'])
@crossdomain(origin='*')
def create_collection(db_id):
    
    coll_id = request.data

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 12345)
    except:
        return json.dumps("Unable to connect to the database!")

    db_names = connection.database_names()
    if db_id in db_names:
        db = connection[db_id]
    else:
        return json.dumps("No such database!")  
    
    coll_names = db.collection_names()
    if coll_id in coll_names:
        return json.dumps("Collection already exists!")
    
    try:
        db.create_collection(coll_id)
    except:
        return json.dumps("Unable to create an experiment")

    return json.dumps('Experiment successfully created!')

#######################################################################################################
# Task 7: Creating a new database [POST]
#######################################################################################################
@app.route('/evarilos/metrics/v1.0/database', methods = ['POST'])
@crossdomain(origin='*')
def create_database():
    
    db_id = request.data

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 12345)
    except:
        return json.dumps("Unable to connect to the database!")

    db_names = connection.database_names()
    if db_id in db_names:
        return json.dumps("Database already exists!")  
    
    try:
        db = connection[db_id]
        coll = db.create_collection('test_tmp')
    except:
        return json.dumps("Unable to create new database")

    db.test_tmp.drop()
    return json.dumps('Database successfully created!')


#######################################################################################################
# Task 8: Delete the database [DELETE]
#######################################################################################################
@app.route('/evarilos/metrics/v1.0/database/<db_id>', methods = ['DELETE'])
@crossdomain(origin='*')
def delete_database(db_id):

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 12345)
    except:
        return json.dumps("Unable to connect to the database!")


    db_names = connection.database_names()
    if db_id not in db_names:
        return json.dumps("Database doesn't exist!")  
    
    try:
        connection.drop_database(db_id)
    except:
        return json.dumps("Unable to delete the database")

    return json.dumps('Database successfully deleted!')


#######################################################################################################
# Task 9: Delete the experiment from the database [DELETE]
#######################################################################################################
@app.route('/evarilos/metrics/v1.0/database/<db_id>/experiment/<coll_id>', methods = ['DELETE'])
@crossdomain(origin='*')
def delete_collection(db_id, coll_id):

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 12345)
    except:
        return json.dumps("Unable to connect to the database!")


    db_names = connection.database_names()
    if db_id not in db_names:
        return json.dumps("Database doesn't exist!")  
    
    db = connection[db_id]
    coll_names = db.collection_names()
    if coll_id not in coll_names:
        return json.dumps("Experiment doesn't exist!")  

    try:
        db.drop_collection(coll_id)
    except:
        return json.dumps("Unable to delete the experiment")

    return json.dumps('Experiment successfully deleted!')

#######################################################################################################
# Task 11: Replace the experiment [PUT]
#######################################################################################################
@app.route('/evarilos/metrics/v1.0/database/<db_id>/experiment/<coll_id>', methods = ['PUT'])
@crossdomain(origin='*')
def replace_location(db_id, coll_id):

    experiment_collection = experiment_results_pb2.Experiment()

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 12345)
    except:
        return json.dumps("Unable to connect to the database!")

    try:
        experiment_collection.ParseFromString(request.data)
    except:
        return json.dumps('Message is not well defined!')

    db_names = connection.database_names()
    if db_id not in db_names:
        return json.dumps("Database doesn't exist!")  
    
    db = connection[db_id]
    coll_names = db.collection_names()
    if coll_id not in coll_names:
        return json.dumps("Collection doesn't exist!")  

    collection = db[coll_id]
    try:
        collection_backup = collection.find_one({})
        collection.remove()
    except:
        return json.dumps("Unable to read data from the database!")

    try:
        collection.insert(protobuf_json.pb2json(experiment_collection))
    except:
        collection.insert(collection_backup)
        return json.dumps("Unable to store data into the database!")

    return json.dumps('Message successfully replaced!')

#######################################################################################################
# Task 13: Change the collection name [PATCH]
#######################################################################################################
@app.route('/evarilos/metrics/v1.0/database/<db_id>/experiment/<coll_id>', methods = ['PATCH'])
@crossdomain(origin='*')
def change_collection(db_id, coll_id):

    new_name = request.data

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 12345)
    except:
        return json.dumps("Unable to connect to the database!")

    db_names = connection.database_names()
    if db_id not in db_names:
        return json.dumps("Database doesn't exist!")  
    
    db = connection[db_id]
    coll_names = db.collection_names()
    if coll_id not in coll_names:
        return json.dumps("Experiment doesn't exist!")  
    if new_name in coll_names:
        return json.dumps("New name already exist!")

    collection = db[coll_id]
    try:
        collection.rename(new_name)
    except:
        return json.dumps("Unable to change the name of the experiment!")
    return json.dumps("Experiment's name changed!")


#######################################################################################################
# Additional help functions
#######################################################################################################

# Error handler
@app.errorhandler(404)
@crossdomain(origin='*')
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404) 

# Creating the URIs
def make_public_task(function):
    new_function = {}
    for field in function:
        if field == 'id':
            new_function['uri'] = url_for('get_function', function_id = function['id'], _external = True)
        else:
            new_function[field] = function[field]
    return new_function

# Enabling DELETE, PUT, etc.
class RequestWithMethod(urllib2.Request):
    """Workaround for using DELETE, PUT, PATCH with urllib2"""
    def __init__(self, url, method, data=None, headers={}, origin_req_host=None, unverifiable=False):
        self._method = method
        urllib2.Request.__init__(self, url, data, headers, origin_req_host, unverifiable)

    def get_method(self):
        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self) 

#######################################################################################################
# Start tehs erver on port 50001
#######################################################################################################

if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug = True, port = 5001)

