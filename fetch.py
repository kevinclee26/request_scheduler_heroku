import requests
import time
import secrets
import sys
import os

from sqlalchemy.orm import Session
from models import *

def get_bike_data(engine):
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