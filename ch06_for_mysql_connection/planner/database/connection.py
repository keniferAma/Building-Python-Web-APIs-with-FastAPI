from sqlalchemy import create_engine # used to set up the database connection. 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



URL_DATABASE = 'mysql+pymysql://root:comic0413@localhost:3306/blogapplication'

engine = create_engine(URL_DATABASE)
"""This line creates an engine that provides a source of database connectivity. 
The engine is created using the database URL you defined"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""This line creates a session factory bound to the engine. 
A session is essentially a conversation between your application and the database. """

Base = declarative_base()
"""This line creates a base class for declarative models. 
In SQLAlchemy, a model is a Python class that represents a database table. 
The declarative_base function creates a base class that your models will inherit from."""