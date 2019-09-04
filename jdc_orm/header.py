
from sqlalchemy import Column, String, Integer, Date
from base import Base

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

    def __init__(self, PrimaryKey,SpeciesState,PlotID,DBKey,EcologicalSiteId,Latitude_NAD83,
    Longitude_NAD83,State,County,DateEstablished,DateLoadedInDb,ProjectName,Source,
    LocationType,DateVisited,Elevation,PercentCoveredByEcoSite):

        self.PrimaryKey = PrimaryKey
        self.SpeciesState = SpeciesState
        self.PlotID = PlotID
        self.PlotKey = PlotKey
        self.DBKey = DBKey
        self.EcologicalSiteId = EcologicalSiteId
        self.Latitude_NAD83 = Latitude_NAD83
        self.Longitude_NAD83 = Longitude_NAD83
        self.State = State
        self.County = County
        self.DateEstablished = DateEstablished
        self.DateLoadedInDb = DateLoadedInDb
        self.ProjectName = ProjectName
        self.Source = Source
        self.LocationType = LocationType
        self.DateVisited = DateVisited
        self.Elevation = Elevation
        self.PercentCoveredByEcoSite = PercentCoveredByEcoSite
