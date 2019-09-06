
from sqlalchemy.engine import url as sa_url
from sqlalchemy import Column, String, Integer, Text, Numeric, Date
from common.base import Base
from common.base
# connection credentials
db_connect_url = sa_url.URL(
    drivername="postgresql",
    username =db_user,
    password=db_password,
    host=db_host,
    port=5432,
    database="gisdb")

# sqlalchemy engine
engine = create_engine(db_connect_url)

class dataHeader(Base):
    __tablename__ = 'dataHeader'

    PrimaryKey = Column(String, primary_key = True)
    SpeciesState = Column('SpeciesState',String)
    PlotID = Column('PlotID',Text)
    PlotKey = Column('PlotKey',String)
    DBKey = Column('DBKey',Text)
    EcologicalSiteId = Column('EcologicalSiteId', String)
    Latitude_NAD83 = Column('Latitude_NAD83', Numeric)
    Longitude_NAD83 = Column('Longitude_NAD83',Numeric)
    State = Column('State', String)
    County = Column('County', String)
    DateEstablished = Column('DateEstablished', Date)
    DateLoadedInDb = Column('DateLoadedInDb',Date)
    ProjectName = Column('ProjectName',Text)
    Source = Column('Source',Text)
    LocationType = Column('LocationType', String)
    DateVisited = Column('DateVisited',Date)
    Elevation = Column('Elevation',Numeric)
    PercentCoveredByEcoSite = Column('PercentCoveredByEcoSite', Numeric)

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
