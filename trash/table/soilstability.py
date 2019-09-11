from sqlalchemy import Column, Text, Date, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

from base import Base

class dataSoilStability(Base):
    __tablename__='dataSoilStability'
    PlotKey = Column('PlotKey', String)
    RecKey = Column('RecKey', String)
    DateModified = Column('DateModified', Date)
    FormType = Column('FormType', Text)
    FormDate = Column('FormDate', Date)
    LineKey = Column('LineKey', String)
    Observer = Column('Observer', Text)
    Recorder = Column('Recorder', Text)
    DataEntry = Column('DataEntry', Text)
    DataErrorChecking = Column('DataErrorChecking', Text)
    SoilStabSubSurface = Column('SoilStabSubSurface', Integer)
    Notes = Column('Notes', Text)
    DateLoadedInDb = Column('DateLoadedInDb', Date)
    PrimaryKey = Column('PrimaryKey', ForeignKey('dataHeader.PrimaryKey'))
    DBKey = Column('DBKey', Text)
    Position = Column('Position', Integer)
    Line = Column('Line', String)
    Pos = Column('Pos', String)
    Veg = Column('Veg', Text)
    Rating = Column('Rating', Integer)
    Hydro = Column('Hydro', Integer)
    Source = Column('Source', Text)
    soilstability_header = relationship('dataHeader', backref='dataSoilStability')

    def __init__(self, PlotKey, RecKey, DateModified, FormType, FormDate, LineKey, Observer, Recorder, DataEntry, DataErrorChecking, SoilStabSubSurface, Notes, DateLoadedInDb, PrimaryKey, DBKey, Position, Line, Pos, Veg, Rating, Hydro, Source, soilstability_header):
        self.PlotKey = PlotKey
        self.RecKey = RecKey
        self.DateModified = DateModified
        self.FormType = FormType
        self.FormDate = FormDate
        self.LineKey = LineKey
        self.Observer = Observer
        self.Recorder = Recorder
        self.DataEntry = DataEntry
        self.DataErrorChecking = DataErrorChecking
        self.SoilStabSubSurface = SoilStabSubSurface
        self.Notes = Notes
        self.DateLoadedInDb = DateLoadedInDb
        self.PrimaryKey = PrimaryKey
        self.DBKey = DBKey
        self.Position = Position
        self.Line = Line
        self.Pos = Pos
        self.Veg = Veg
        self.Rating = Rating
        self.Hydro = Hydro
        self.Source = Source
        self.soilstability_header = soilstability_header
