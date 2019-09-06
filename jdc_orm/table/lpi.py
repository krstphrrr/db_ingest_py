# coding=utf-8

from sqlalchemy import Column, Text, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

from base import Base

class dataLPI(Base):
    __tablename__='dataLPI'

    LineKey = Column(String)
    RecKey = Column(String)
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
    PrimaryKey = Column(Text, ForeignKey('dataHeader.PrimaryKey'))
    DBKey = Column(Text)
    PoIntegerLoc = Column(Numeric)
    PoIntegerNbr = Column(Integer)
    ShrubShape = Column(Text)
    layer = Column(Text)
    code = Column(Text)
    chckbox = Column(Integer)
    Source = Column(Text)
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
