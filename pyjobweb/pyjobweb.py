# -*- coding: utf-8 -*-
'''
Created on Oct 15, 2016

@author: acer
'''
# -*- coding: UTF-8 -*-
"""
app1.py: First Python-Flask webapp
"""
from flask import Flask, render_template, send_from_directory  # Import class Flask from module flask
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from jobInfo import getStatus
import time
#Fake properties file
import configparser
import os
import sys

#Restful resource
class Jobs(Resource):
    def get(self,mNM):
        print ("Vasan: "+mNM)
        return getattr(ji,'get'+mNM)(); #calls ji.get<mNM>. mNM should be a method of ji 
#main env is set here
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
print(dir_path)        
file = open(dir_path+'/pyjobweb.properties', encoding="utf_8")
config = configparser.ConfigParser()
config.read_file(file, source='pyjobweb.properties')
print(config['windows']['jobRptfile'])
if os.name=='nt':
    section='windows'
else:
    section='unix'

ji=getStatus.jobStatus(config[section])
app = Flask(__name__)    # Construct an instance of Flask class
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)
api = Api(app)
@app.route('/')   # Register index() as route handler for root URL '/'
@cross_origin()
def index():
    """Route handler (or View Function) for root URL '/'"""
    return render_template('index.html')
    #return 'Hello, world!'
@app.route('/web/<path>')   # Register index() as route handler for root URL '/'
@cross_origin()
def urlPages(path):
    return send_from_directory(dir_path+"/nonTemplates",path) # Send files without jinja templating (interferes with angular)
api.add_resource(Jobs, '/restful/<mNM>')
if __name__ == '__main__':  # Script executed directly?
   app.run(host='0.0.0.0')  # Launch built-in web server and run this Flask webapp