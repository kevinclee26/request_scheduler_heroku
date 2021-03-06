from flask import Flask, jsonify, redirect, render_template
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import Session
import os

import fetch

from models import *

# from flask_sqlalchemy import SQLAlchemy
# Imports the method used for connecting to DBs

# USERNAME='postgres'
# PASS='postgres'
# SQLALCHEMY_DATABASE_URI=f'postgresql://{USERNAME}:{PASS}@localhost:5432/request_scheduler_heroku_db'

# SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI=os.environ.get('HEROKU_POSTGRESQL_BRONZE_URL').replace("://", "ql://", 1)

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

# Create a "Metadata" Layer That Abstracts our SQL Database
# ----------------------------------
# Create (if not already in existence) the tables associated with our classes.
Base.metadata.create_all(engine)
# db.create_all()

# Use this to clear out the db
# ----------------------------------
# Base.metadata.drop_all(engine)

# @app.route('/javascript')
# def template():
# 	return render_template('index.html', data_from_flask=configs)

@app.route('/')
def index(): 
	# Create a Session Object to Connect to DB
	# ----------------------------------
	# Session is a temporary binding to our DB
	session=Session(engine)
	results=session.query(Log.jobname, Log.processed, Log.bikes, Log.size).all()
	session.close()
	# return 'Welcome'
	# return jsonify([[each_field for each_field in each_log] for each_log in results])
	return render_template('index.html')

# @app.route('/get_data')
# def get_data():
# 	# Create a Session Object to Connect to DB
# 	# ----------------------------------
# 	# Session is a temporary binding to our DB
# 	session=Session(engine)
# 	new_log=Log(**fetch.get_bike_data())
# 	session.add(new_log)
# 	session.commit()
# 	session.close()
# 	return redirect("/")

@app.route('/api/jobs')
def jobs_status():
	session=Session(engine)
	results=session.query(Log.processed, Log.bikes).order_by(desc(Log.processed)).limit(200).all()
	session.close()
	# return jsonify([each_result['processed'] for each_result in results])
	return jsonify([{'processed': each_result[0], 'bikes': each_result[1]} for each_result in results])

if __name__=='__main__': 
	app.run(debug=True)