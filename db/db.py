import mysql.connector
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

URL='mysql+mysqlconnector://root:sirigowri2508@localhost/google_sheet_sync'
engine=create_engine(URL)
Session = sessionmaker(bind=engine)
session = Session()
Base=declarative_base()

class MySheetData(Base):
   __tablename__ = 'sheet_data'
   id = Column(Integer, primary_key=True, index=True)
   name = Column(String(100))
   age = Column(Integer)
   updated_at = Column(DateTime)




