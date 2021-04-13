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
# SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)

def get_bike_data():
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