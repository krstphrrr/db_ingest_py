# coding=utf-8

from sqlalchemy import Column, Text, Date, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

from common.base import Base

class dataHeight(Base):
    __tablename__='dataHeight'

   PrimaryKey = Column('PrimaryKey', Text, ForeignKey("dataHeader.PrimaryKey"))
   DBKey = Column('DBKey', Text)
   PoIntegerLoc = Column('PoIntegerLoc', Numeric)
   PoIntegerNbr = Column('PoIntegerNbr', Integer)
   RecKey = Column('RecKey', String)
   Height = Column('Height', Numeric)
   Species = Column('Species', Text)
   Chkbox = Column('Chkbox', Integer)
   type = Column('type', Text)
   GrowthHabit_measured = Column('GrowthHabit_measured', Text)
   LineKey = Column('LineKey', String)
   DateModified = Column('DateModified', Date)
   FormType = Column('FormType', Text)
   FormDate = Column('FormDate', Date)
   Observer = Column('Observer', Text)
   Recorder = Column('Recorder', Text)
   DataEntry = Column('DataEntry', Text)
   DataErrorChecking = Column('DataErrorChecking', Text)
   Direction = Column('Direction', String)
   Measure = Column('Measure', Integer)
   LineLengthAmount = Column('LineLengthAmount', Numeric)
   SpacingIntegerervalAmount = Column('SpacingIntegerervalAmount', Numeric)
   SpacingType = Column('SpacingType', Text)
   HeightOption = Column('HeightOption', Text)
   HeightUOM = Column('HeightUOM', Text)
   ShowCheckbox = Column('ShowCheckbox', Integer)
   CheckboxLabel = Column('CheckboxLabel', Text)
   Source = Column('Source', Text)
   UOM = Column('UOM', Text)
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
