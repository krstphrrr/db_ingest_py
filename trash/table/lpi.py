# coding=utf-8

from sqlalchemy import Column, Text, Date, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

from base import Base

class dataLPI(Base):
    __tablename__='dataLPI'

    LineKey = Column('LineKey', String)
    RecKey = Column('RecKey', String)
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
    PrimaryKey = Column('PrimaryKey', Text, ForeignKey('dataHeader.PrimaryKey'))
    DBKey = Column('DBKey', Text)
    PoIntegerLoc = Column('PoIntegerLoc', Numeric)
    PoIntegerNbr = Column('PoIntegerNbr', Integer)
    ShrubShape = Column('ShrubShape', Text)
    layer = Column('layer', Text)
    code = Column('code', Text)
    chckbox = Column('chckbox', Integer)
    Source = Column('Source', Text)
    lpi_header = relationship("dataHeader", backref="dataLPI")

# add the relationship as an argument and also as a statement in the body
    def __init__(self, LineKey, RecKey, DateModified, FormType, FormDate, Observer,
    Recorder, DataEntry, DataErrorChecking, Direction, Measure, LineLengthAmount,
    SpacingIntegerervalAmount, SpacingType, HeightOption, HeightUOM, ShowCheckbox,
    CheckboxLabel, PrimaryKey, DBKey, PoIntegerLoc, PoIntegerNbr, ShrubShape, layer,
    code, chckbox, Source, lpi_header):
        self.LineKey = LineKey
        self.RecKey = RecKey
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
        self.PrimaryKey = PrimaryKey
        self.DBKey = DBKey
        self.PoIntegerLoc = PoIntegerLoc
        self.PoIntegerNbr = PoIntegerNbr
        self.ShrubShape = ShrubShape
        self.layer = layer
        self.code = code
        self.chckbox = chckbox
        self.Source = Source
        self.lpi_header = lpi_header
