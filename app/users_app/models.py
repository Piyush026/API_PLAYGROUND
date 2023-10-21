from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


# from sqlalchemy import Column, Integer, String
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import MetaData
#
# Base = declarative_base()
#
# engine = create_engine('sqlite:///test.db')
# Session = sessionmaker(bind=engine)
#
# metadata = MetaData()
#
# Base.metadata = metadata
#
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     password = Column(String)



"""https://github.com/anandtripathi5/alembic-multidatabase"""