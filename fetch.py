import requests
import time
import secrets
import sys
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import *

# USERNAME='postgres'
# PASS='postgres'
# SQLALCHEMY_DATABASE_URI=f'postgresql://{USERNAME}:{PASS}@localhost:5432/request_scheduler_heroku_db'

# session.close() will give the connection back to the connection pool of Engine 
# and doesn't close the connection.
# engine.dispose() will close all connections of the connection pool.
# Engine will not use connection pool if you set poolclass=NullPool. So the 
# connection (SQLAlchemy session) will close directly after session.close().

# SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

# Create Database Connection
# ----------------------------------
# Creates a connection to our DB
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Create a "Metadata" Layer That Abstracts our SQL Database
# ----------------------------------
# Create (if not already in existence) the tables associated with our classes.
Base.metadata.create_all(engine)

def get_bike_data():
    # Create a Session Object to Connect to DB
    # ----------------------------------
    # Session is a temporary binding to our DB
    session=Session(engine)
    # request url
    request_url='https://gbfs.spin.pm/api/gbfs/v1/washington_dc/free_bike_status'
    jobname=secrets.token_urlsafe(16)
    response=requests.get(request_url)
    data=response.json()
    new_log={'jobname': jobname, 
             'processed': time.time(), 
             'bikes': len(data['data']['bikes']), 
             'size': sys.getsizeof(data)}
    session.add(Log(**new_log))
    session.commit()
    session.close()
    return None