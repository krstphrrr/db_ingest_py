
from sqlalchemy.engine import url as sa_url

from sqlalchemy import Column, String, Integer, Text, Numeric, Date
from sqlalchemy.orm import relationship
from common.base import Base

class dataHeader(Base):
    __tablename__ = 'dataHeader'

    PrimaryKey = Column('PrimaryKey', Text, primary_key = True)
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

    gap_header = relationship("dataGap")
    height_header = relationship("dataHeight")
    lpi_header = relationship("dataLPI")
    soilstab_header = relationship("dataSoilStability")
    speciesinv_header = relationship("dataSpeciesInventory")
    geoind_header = relationship("geo_ind")
    geospp_header = relationship("geo_spp")


    def __init__(self, PrimaryKey, SpeciesState, PlotID, DBKey, EcologicalSiteId, Latitude_NAD83,
    Longitude_NAD83, State, County, DateEstablished, DateLoadedInDb, ProjectName, Source,
    LocationType, DateVisited, Elevation, PercentCoveredByEcoSite, gap_header, height_header, lpi_header, soilstab_header, speciesinv_header, geoind_header, geospp_header):
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
        self.gap_header = gap_header
        self.height_header = height_header
        self.lpi_header = lpi_header
        self.soilstab_header = soilstab_header
        self.speciesinv_header = speciesinv_header
        self.geoind_header = geoind_header
        self.geospp_header = geoind_header
