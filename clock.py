from apscheduler.schedulers.blocking import BlockingScheduler
import fetch
from sqlalchemy import create_engine
from models import *
import os

# USERNAME='postgres'
# PASS='postgres'
# SQLALCHEMY_DATABASE_URI=f'postgresql://{USERNAME}:{PASS}@localhost:5432/request_scheduler_heroku_db'

# session.close() will give the connection back to the connection pool of Engine 
# and doesn't close the connection.
# engine.dispose() will close all connections of the connection pool.
# Engine will not use connection pool if you set poolclass=NullPool. So the 
# connection (SQLAlchemy session) will close directly after session.close().

# SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI=os.environ.get('HEROKU_POSTGRESQL_BRONZE_URL').replace("://", "ql://", 1)

# Create Database Connection
# ----------------------------------
# Creates a connection to our DB
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Create a "Metadata" Layer That Abstracts our SQL Database
# ----------------------------------
# Create (if not already in existence) the tables associated with our classes.
Base.metadata.create_all(engine)

sched=BlockingScheduler()
fetch_freq_mins=1
process_freq_mins=15

@sched.scheduled_job('interval', minutes=fetch_freq_mins)
def data(): 
	fetch.get_bike_data(engine)
# 	fetch.all_scooter_data()
# 	# fetch.weather_data()
	print(f'This job is run every {fetch_freq_mins} minutes.')
	return None

# @sched.scheduled_job('internal', minutes=process_freq_mins)
# def process_logs():
# 	fetch.process_log()
# 	print(f'This job is run every {process_freq_mins} minutes.')
# 	return None

# # @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# # def scheduled_job():
# #     print('This job is run every weekday at 5pm.')

sched.start()