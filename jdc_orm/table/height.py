# coding=utf-8

from sqlalchemy import Column, Text, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

from common.base import Base

class dataHeight(Base):
    __tablename__='dataHeight'

   PrimaryKey = Column(Text, ForeignKey("dataHeader.PrimaryKey"))
   DBKey = Column(Text)
   PoIntegerLoc = Column(Numeric)
   PoIntegerNbr = Column(Integer)
   RecKey = Column(String)
   Height = Column(Numeric)
   Species = Column(Text)
   Chkbox = Column(Integer)
   type = Column(Text)
   GrowthHabit_measured = Column(Text)
   LineKey = Column(String)
   DateModified = Column(DATE)
   FormType = Column(Text)
   FormDate = Column(DATE)
   Observer = Column(Text)
   Recorder = Column(Text)
   DataEntry = Column(Text)
   DataErrorChecking = Column(Text)
   Direction = Column(String)
   Measure = Column(Integer)
   LineLengthAmount = Column(Numeric)
   SpacingIntegerervalAmount = Column(Numeric)
   SpacingType = Column(Text)
   HeightOption = Column(Text)
   HeightUOM = Column(Text)
   ShowCheckbox = Column(Integer)
   CheckboxLabel = Column(Text)
   Source = Column(Text)
   UOM = Column(Text)
   height_header = relationship("dataHeader", backref="dataHeight")

# add the relationship as an argument and also as a statement in the body
    def __init__(self, DBKey, PoIntegerLoc, PoIntegerNbr, RecKey, Height, Species,
    Chkbox, type, GrowthHabit_measured, LineKey, DateModified, FormType, FormDate,
    Observer, Recorder, DataEntry, DataErrorChecking, Direction, Measure,
    LineLengthAmount, SpacingIntegerervalAmount, SpacingType, HeightOption,
    HeightUOM, ShowCheckbox, CheckboxLabel, Source, UOM, height_header):

       self.PrimaryKey = PrimaryKey
       self.DBKey = DBKey
       self.PoIntegerLoc = PoIntegerLoc
       self.PoIntegerNbr = PoIntegerNbr
       self.RecKey = RecKey
       self.Height = Height
       self.Species = Species
       self.Chkbox = Chkbox
       self.type = type
       self.GrowthHabit_measured = GrowthHabit_measured
       self.LineKey = LineKey
       self.DateModified = DateModified
       self.FormType = FormType
       self.FormDate = FormDate
       self.Observer = Observer
       self.Recorder = Recorder
       self.DataEntry = DataEntry
       self.DataErrorChecking = DataErrorChecking
       self.Direction = Direction
       self.Measure = Measure
       self.LineLengthAmount = LineLengthAmount
       self.SpacingIntegerervalAmount = SpacingIntegerervalAmount
       self.SpacingType = SpacingType
       self.HeightOption = HeightOption
       self.HeightUOM = HeightUOM
       self.ShowCheckbox = ShowCheckbox
       self.CheckboxLabel = CheckboxLabel
       self.Source = Source
       self.UOM = UOM
       self.height_header = height_header
