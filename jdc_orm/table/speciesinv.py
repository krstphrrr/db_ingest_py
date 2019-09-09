
from sqlalchemy import Column, Text, Date, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

from base import Base

class dataSpeciesInventory(Base):
    __tablename__='dataSpeciesInventory'
   LineKey = Column('LineKey', String)
   RecKey = Column('RecKey', String)
   DateModified = Column('DateModified', Date)
   FormType = Column('FormType', Text)
   FormDate = Column('FormDate', Date)
   Observer = Column('Observer', Text)
   Recorder = Column('Recorder', Text)
   DataEntry = Column('DataEntry', Text)
   DataErrorChecking = Column('DataErrorChecking', Text)
   SpecRichMethod = Column('SpecRichMethod', Integer)
   SpecRichMeasure = Column('SpecRichMeasure', Integer)
   SpecRichNbrSubPlots = Column('SpecRichNbrSubPlots', Integer)
   SpecRich1Container = Column('SpecRich1Container', Integer)
   SpecRich1Shape = Column('SpecRich1Shape', Integer)
   SpecRich1Dim1 = Column('SpecRich1Dim1', Numeric)
   SpecRich1Dim2 = Column('SpecRich1Dim2', Numeric)
   SpecRich1Area = Column('SpecRich1Area', Numeric)
   Notes = Column('Notes', Text)
   DateLoadedInDb = Column('DateLoadedInDb', Date)
   PrimaryKey = Column('PrimaryKey', Text, ForeignKey('dataHeader.PrimaryKey'))
   DBKey = Column('DBKey', Text)
   Species = Column('Species', Text)
   Source = Column('Source', Text)
   Density = Column('Density', Integer)
   speciesinventory_header = relationship('dataHeader', backref = 'dataSpeciesInventory')

   def __init__(self, LineKey, RecKey, DateModified, FormType, FormDate, Observer, Recorder, DataEntry, DataErrorChecking, SpecRichMethod, SpecRichMeasure, SpecRichNbrSubPlots, SpecRich1Container, SpecRich1Shape, SpecRich1Dim1, SpecRich1Dim2, SpecRich1Area, Notes, DateLoadedInDb, PrimaryKey, DBKey, Source, Density, speciesinventory_header):
       self.LineKey = LineKey
       self.RecKey = RecKey
       self.DateModified = DateModified
       self.FormType = FormType
       self.FormDate = FormDate
       self.Observer = Observer
       self.Recorder = Recorder
       self.DataEntry = DataEntry
       self.DataErrorChecking = DataErrorChecking
       self.SpecRichMethod = SpecRichMethod
       self.SpecRichMeasure = SpecRichMeasure
       self.SpecRichNbrSubPlots = SpecRichNbrSubPlots
       self.SpecRich1Container = SpecRich1Container
       self.SpecRich1Shape = SpecRich1Shape
       self.SpecRich1Dim1 = SpecRich1Dim1
       self.SpecRich1Dim2 = SpecRich1Dim2
       self.SpecRich1Area = SpecRich1Area
       self.Notes = Notes
       self.DateLoadedInDb = DateLoadedInDb
       self.PrimaryKey = PrimaryKey
       self.DBKey = DBKey
       self.Species = Species
       self.Source = Source
       self.Density = Density
       self.speciesinventory_header = speciesinventory_header
