# coding=utf-8

from sqlalchemy import Column, String, Date, Text, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from common.base import Base


class dataGap(Base):
    __tablename__='dataGap'

    LineKey = Column('LineKey', String)
    RecKey = Column('RecKey', String)
    DateModified = Column('DateModified', Date)
    FormType = Column('FormType', Text)
    FormDate = Column('FormDate', Date)
    Observer = Column('Observer', Text)
    Recorder = Column('Recorder', Text)
    DataEntry = Column('DataEntry', Text)
    DataErrorChecking = Column('DataErrorChecking', Text)
    Direction = Column('Direction', Numeric)
    Measure = Column('Measure', Integer)
    LineLengthAmount = Column('LineLengthAmount',Numeric)
    GapMin = Column('GapMin', Numeric)
    GapData = Column('GapData', Integer)
    PerennialsCanopy = Column('PerennialsCanopy', Integer)
    AnnualGrassesCanopy = Column('AnnualGrassesCanopy', Integer)
    AnnualForbsCanopy = Column('AnnualForbsCanopy', Integer)
    OtherCanopy = Column('OtherCanopy', Integer)
    Notes = Column('Notes', Text)
    NoCanopyGaps = Column('NoCanopyGaps', Integer)
    NoBasalGaps = Column('NoBasalGaps', Integer)
    DateLoadedInDb = Column('DateLoadedInDb', Date)
    PerennialsBasal = Column('PerennialsBasal', Integer)
    AnnualGrassesBasal = Column('AnnualGrassesBasal', Integer)
    AnnualForbsBasal = Column('AnnualForbsBasal', Integer)
    OtherBasal = Column('OtherBasal', Integer)
    PrimaryKey = Column('PrimaryKey', Text, ForeignKey('dataHeader.PrimaryKey'))
    DBKey = Column('DBKey', Text)
    SeqNo = Column('SeqNo', Text)
    RecType = Column('RecType', Text)
    GapStart = Column('GapStart', Numeric)
    GapEnd = Column('GapEnd', Numeric)
    Gap = Column('Gap', Numeric)
    Source = Column('Source', Text)
    gap_header = relationship("dataHeader", backref = "dataGap")

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
