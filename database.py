from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Flask-SQLAlchemy is an extension for Flask that aims to 
# simplify using SQLAlchemy with Flask by providing defaults 
# and helpers to accomplish common tasks. 

# Flask-SQLAlchemy has a disadvantage in it  
# makes using the database outside of a Flask context difficult. 

# https://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4
postgres_database_url='postgresql://path.db'
engine=create_engine(postgres_database_url)

Base=declarative_base()