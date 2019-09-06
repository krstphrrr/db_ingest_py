# coding=utf-8

from sqlalchemy import Column, String, Date, Text, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from common.base import Base


class dataGap(Base):
    __tablename__='dataGap'

    LineKey = Column(String)
    RecKey = Column(String)
    DateModified = Column(Date)
    FormType = Column(Text)
    FormDate = Column(Date)
    Observer = Column(Text)
    Recorder = Column(Text)
    DataEntry = Column(Text)
    DataErrorChecking = Column(Text)
    Direction = Column(Numeric)
    Measure = Column(Integer)
    LineLengthAmount = Column(Numeric)
    GapMin = Column(Numeric)
    GapData = Column(Integer)
    PerennialsCanopy = Column(Integer)
    AnnualGrassesCanopy = Column(Integer)
    AnnualForbsCanopy = Column(Integer)
    OtherCanopy = Column(Integer)
    Notes = Column(Text)
    NoCanopyGaps = Column(Integer)
    NoBasalGaps = Column(Integer)
    DateLoadedInDb = Column(Date)
    PerennialsBasal = Column(Integer)
    AnnualGrassesBasal = Column(Integer)
    AnnualForbsBasal = Column(Integer)
    OtherBasal = Column(Integer)
    PrimaryKey = Column(Text,ForeignKey('header.PrimaryKey'))
    DBKey = Column(Text)
    SeqNo = Column(Text)
    RecType = Column(Text)
    GapStart = Column(Numeric)
    GapEnd = Column(Numeric)
    Gap = Column(Numeric)
    Source = Column(Text)
    gap_header = relationship("dataHeader", backref = backref("dataGap"))

# add the relationship as an argument and also as a statement in the body
    def __init__(self, LineKey, RecKey, DateModified, FormType, FormDate, Observer,
    Recorder, DataEntry, DataErrorChecking, Direction, Measure, LineLengthAmount,
    GapMin, GapData, PerennialsCanopy, AnnualGrassesCanopy, AnnualForbsCanopy,
    OtherCanopy, Notes, NoCanopyGaps, NoBasalGaps, DateLoadedInDb, PerennialsBasal,
    AnnualGrassesBasal, AnnualForbsBasal, OtherBasal, PrimaryKey, DBKey, SeqNo,
    RecType, GapStart, GapEnd, Gap, Source, gap_header):
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
        self.GapMin = GapMin
        self.GapData = GapData
        self.PerennialsCanopy = PerennialsCanopy
        self.AnnualGrassesCanopy = AnnualGrassesCanopy
        self.AnnualForbsCanopy = AnnualForbsCanopy
        self.OtherCanopy = OtherCanopy
        self.Notes = Notes
        self.NoCanopyGaps = NoCanopyGaps
        self.NoBasalGaps = NoBasalGaps
        self.DateLoadedInDb = DateLoadedInDb
        self.PerennialsBasal = PerennialsBasal
        self.AnnualGrassesBasal = AnnualGrassesBasal
        self.AnnualForbsBasal = AnnualForbsBasal
        self.OtherBasal = OtherBasal
        self.PrimaryKey = PrimaryKey
        self.DBKey = DBKey
        self.SeqNo = SeqNo
        self.RecType = RecType
        self.GapStart = GapStart
        self.GapEnd = GapEnd
        self.Gap = Gap
        self.Source = Source
        self.gap_header = gap_header
