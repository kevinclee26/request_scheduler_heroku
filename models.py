# Allow us to declare column types
from sqlalchemy import Column, Integer, String, Float
# from sqlalchemy.types import Date

# from database import Base

# Imports the methods needed to abstract classes into tables
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class Log(Base):
	__tablename__='logs'

	id=Column(Integer, primary_key=True, autoincrement=True)
	jobname=Column(String)
	processed=Column(Float)
	bikes=Column(Integer)
	size=Column(Float)

	# def __init__(self, jobname, processed, bikes, size): 
	# 	self.jobname=jobname
	# 	self.processed=processed
	# 	self.bikes=bikes
	# 	self.size=size

	def __repr__(self):
		return f'<Jobname> {self.jobname}' 