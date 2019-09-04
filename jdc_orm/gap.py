# coding=utf-8

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base


class dataGap(Base):
    __tablename__='dataGap'

    LineKey = Column(VARCHAR(100))
    RecKey = Column(VARCHAR(100))
    DateModified = Column(Date)
    FormType = Column(TEXT)
    FormDate = Column(Date)
    Observer = Column(TEXT)
    Recorder = Column(TEXT)
    DataEntry = Column(TEXT)
    DataErrorChecking = Column(TEXT)
    Direction = Column(NUMERIC)
    Measure = Column(INT)
    LineLengthAmount = Column(NUMERIC)
    GapMin = Column(NUMERIC)
    GapData = Column(INT)
    PerennialsCanopy = Column(INT)
    AnnualGrassesCanopy = Column(INT)
    AnnualForbsCanopy = Column(INT)
    OtherCanopy = Column(INT)
    Notes = Column(TEXT)
    NoCanopyGaps = Column(INT)
    NoBasalGaps = Column(INT)
    DateLoadedInDb = Column(Date)
    PerennialsBasal = Column(INT)
    AnnualGrassesBasal = Column(INT)
    AnnualForbsBasal = Column(INT)
    OtherBasal = Column(INT)
    PrimaryKey = Column(TEXT,ForeignKey('header.PrimaryKey'))
    DBKey = Column(TEXT)
    SeqNo = Column(TEXT)
    RecType = Column(TEXT)
    GapStart = Column(NUMERIC)
    GapEnd = Column(NUMERIC)
    Gap = Column(NUMERIC)
    Source = Column(TEXT)
    gap_header = relationship("dataHeader", backref = backref("dataGap", uselist=False))

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
