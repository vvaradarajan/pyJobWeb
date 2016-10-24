# -*- coding: utf-8 -*-
'''
Created on Oct 15, 2016

@author: acer
'''
# -*- coding: UTF-8 -*-
"""
app1.py: First Python-Flask webapp
"""
from flask import Flask, render_template  # Import class Flask from module flask
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from jobInfo import getStatus
import time
#Restful resource
class Jobs(Resource):
    def get(self,jobs):
        return ji.getStatus()
        

lfNM="C:/junk/junk.lock"
dfNM="C:/junk/report.txt"
#os.remove(lfNM)
ji=getStatus.jobStatus(lfNM,dfNM)
app = Flask(__name__)    # Construct an instance of Flask class
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
    return render_template(path)
api.add_resource(Jobs, '/restful/<jobs>')
if __name__ == '__main__':  # Script executed directly?
   app.run()  # Launch built-in web server and run this Flask webapp