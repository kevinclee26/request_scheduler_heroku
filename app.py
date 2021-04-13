from flask import Flask, jsonify, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os

import fetch

# import models
# from models import Log, Base
from models import *

# from flask_sqlalchemy import SQLAlchemy
# Imports the method used for connecting to DBs
# from sqlalchemy import create_engine

# USERNAME='postgres'
# PASS='postgres'

# SQLALCHEMY_DATABASE_URI=f'postgresql://{USERNAME}:{PASS}@localhost:5432/request_scheduler_heroku_db'
# SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

request_url='https://gbfs.spin.pm/api/gbfs/v1/washington_dc/free_bike_status'

app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql://{SQLALCHEMY_DATABASE_URI}'
# app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql://{USERNAME}:{PASS}@localhost:5432/request_scheduler_heroku_db'

# respond to FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future. 
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db=SQLAlchemy(app)
# The _BoundDeclarativeMeta metaclass is a subclass of SQLAlchemy's DeclarativeMeta, 
# it simply adds support for computing a default value for __tablename__ (the table name) and also to handle binds.
# The base.query property enables Flask-SQLAlchemy based models to access a query object as Model.query instead of SQLAlchemy's session.query(Model).
# The _QueryProperty query class is also subclassed from SQLAlchemy's query. 
# The Flask-SQLAlchemy subclass adds three additional query methods that do not exist in SQLAlchemy: get_or_404(), first_or_404() and paginate().

# Create Database Connection
# ----------------------------------
# Creates a connection to our DB
engine = create_engine(SQLALCHEMY_DATABASE_URI)
# conn = engine.connect()

# Create a "Metadata" Layer That Abstracts our SQL Database
# ----------------------------------
# Create (if not already in existence) the tables associated with our classes.
# db.create_all()
Base.metadata.create_all(engine)
# Use this to clear out the db
# ----------------------------------
# Base.metadata.drop_all(engine)

@app.route('/')
def index(): 
	# Create a Session Object to Connect to DB
	# ----------------------------------
	# Session is a temporary binding to our DB
	session=Session(engine)
	results=session.query(Log.jobname, Log.processed, Log.bikes, Log.size).all()
	session.close()
	# return 'Welcome'
	return jsonify([[each_field for each_field in each_log] for each_log in results])

@app.route('/get_data')
def get_data():
	# Create a Session Object to Connect to DB
	# ----------------------------------
	# Session is a temporary binding to our DB
	session=Session(engine)
	new_log=Log(**fetch.get_bike_data())
	session.add(new_log)
	session.commit()
	session.close()
	return redirect("/")

if __name__=='__main__': 
	app.run(debug=True)