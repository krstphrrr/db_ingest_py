import psycopg2
import pandas as pd
import csv
import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dbstr='posgresql+psycopg2://kris:JDC@1912!@jornada-ldc2.jrn.nmsu.edu:5432/gisdb'

db = create_engine(dbstr)
base = declarative_base() #

class dataHeader(base):
    __tablename__ = 'dataHeader'
    PrimaryKey = Column(VARCHAR(100), primary_key = True)
    SpeciesState = Column(VARCHAR(2))
    PlotID = Column(TEXT)
    PlotKey = Column(VARCHAR(50))
    DBKey = Column(TEXT)
    EcologicalSiteId = Column(VARCHAR(50))
    Latitude_NAD83 = Column(NUMERIC)
    Longitude_NAD83 = Column(NUMERIC)
    State = Column(VARCHAR(2))
    County = Column(VARCHAR(50))
    DateEstablished = Column(DATE)
    DateLoadedInDb = Column(DATE)
    ProjectName = Column(TEXT)
    Source = Column(TEXT)
    LocationType = Column(VARCHAR(20))
    DateVisited = Column(DATE)
    Elevation = Column(NUMERIC)
    PercentCoveredByEcoSite = Column(NUMERIC)

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)
