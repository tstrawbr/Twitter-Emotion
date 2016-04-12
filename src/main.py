import os
import sys
import logging
import json
import pymongo
from flask import Flask, Response, render_template, request, redirect, url_for, send_from_directory, g, session
from test import test
MONGO_DB_URI = "mongodb://test_user:1234@ds053300.mlab.com:53300/emotwit2016"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client.emotwit2016



webapp = Flask(__name__)
@webapp.route("/")
def root():
	return render_template('index.html')



#API Routes
#General format is "/api/<endpoint here>"


@webapp.route("/api/test")
def api_test():
	data = test()
	js = json.dumps(data)
	return js

#server initializiation
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 33507))
    webapp.run(host='0.0.0.0', port=port, debug=True)
