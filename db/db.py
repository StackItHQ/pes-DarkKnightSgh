import mysql.connector
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class MySheetData(Base):
    __tablename__ = 'sheet_data'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Integer)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine('mysql+mysqlconnector://root:sirigowri2508@localhost/google_sheet_sync')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
