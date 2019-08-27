SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET default_tablespace = '';
SET default_with_oids = false;

---
--- drop tables
---

DROP TABLE IF EXISTS "dataHeader";
DROP TABLE IF EXISTS "dataGap";
DROP TABLE IF EXISTS "dataHeight";
DROP TABLE IF EXISTS "dataSpeciesInventory";
DROP TABLE IF EXISTS "dataSoilStability";


--
-- Name: dataHeader; Type: TABLE; Schema: public; Owner: -; Tablespace:
--


CREATE TABLE gisdb.public."dataHeader"(
  "PrimaryKey" VARCHAR(40) PRIMARY KEY,
  "SpeciesState" VARCHAR(2),
  "PlotID" TEXT,
  "PlotKey" VARCHAR(20),
  "DBKey" TEXT,
  "EcologicalSiteId" VARCHAR(50),
  "Latitude_NAD83" NUMERIC,
  "Longitude_NAD83" NUMERIC,
  "State" VARCHAR(2),
  "County" VARCHAR(50),
  "DateEstablished" DATE,
  "DateLoadedInDb" DATE,
  "ProjectName" TEXT,
  "Source" TEXT,
  "LocationType" VARCHAR(20),
  "DateVisited" DATE,
  "Elevation" INT,
  "PercentCoveredByEcoSite" NUMERIC);

  --
  -- Name: dataGap; Type: TABLE; Schema: public; Owner: -; Tablespace:
  --

CREATE TABLE gisdb.public."dataGap"(
  "LineKey" VARCHAR(100),
  "RecKey" VARCHAR(100),
  "DateModified" DATE,
  "FormType" TEXT,
  "FormDate" DATE,
  "Observer" TEXT,
  "Recorder" TEXT,
  "DataEntry" TEXT,
  "DataErrorChecking" TEXT,
  "Direction "NUMERIC,
  "Measure" INT,
  "LineLengthAmount" NUMERIC,
  "GapMin" NUMERIC,
  "GapData" INT,
  "PerennialsCanopy" INT,
  "AnnualGrassesCanopy" INT,
  "AnnualForbsCanopy" INT,
  "OtherCanopy" INT,
  "Notes" TEXT,
  "NoCanopyGaps" INT,
  "NoBasalGaps" INT,
  "DateLoadedInDb" DATE,
  "PerennialsBasal" INT,
  "AnnualGrassesBasal" INT,
  "AnnualForbsBasal" INT,
  "OtherBasal" INT,
  "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
  "DBKey" TEXT,
  "SeqNo" TEXT,
  "RecType" TEXT,
  "GapStart" NUMERIC,
  "GapEnd" NUMERIC,
  "Gap" NUMERIC,
  "source" TEXT);

--
-- Name: dataLPI; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE gisdb.public."dataLPI"(
  "LineKey" VARCHAR(100),
  "RecKey" VARCHAR(100),
  "DateModified" DATE,
  "FormType" TEXT,
  "FormDate" DATE,
  "Observer" TEXT,
  "Recorder" TEXT,
  "DataEntry" TEXT,
  "DataErrorChecking" TEXT,
  "Direction" VARCHAR(50),
  "Measure" INT,
  "LineLengthAmount" NUMERIC,
  "SpacingIntervalAmount" NUMERIC,
  "SpacingType" TEXT,
  --"HeightOption" TEXT, --dropped
  --"HeightUOM" TEXT,  -- dropped
  --"ShowCheckbox" INT, -- dropped
  "CheckboxLabel" TEXT,
  "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
  "DBKey" TEXT,
  "PointLoc" NUMERIC,
  "PointNbr" INT,
  "ShrubShape" TEXT,
  "layer" TEXT,
  "code" TEXT,
  "chckbox" INT,
  "source" TEXT);

  --
-- Name: dataSoilStability; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE gisdb.public."dataSoilStability"(
  "PlotKey" VARCHAR(100),
  "RecKey" VARCHAR(100),
  "DateModified" DATE,
  --"FormType" TEXT, -- dropped
  "FormDate" DATE,
  "LineKey" VARCHAR(100),
  "Observer" TEXT,
  "Recorder" TEXT,
  "DataEntry" TEXT,
  "DataErrorChecking" TEXT,
  "SoilStabSubSurface" INT,
  "Notes" TEXT,
  "DateLoadedInDb" DATE,
  "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
  "DBKey" TEXT,
  "Position" INT,
  "Line" VARCHAR(50),
  "Pos" VARCHAR(50),
  "Veg" TEXT,
  "Rating" INT,
  "Hydro" INT,
  "source" TEXT);

--
-- Name: dataSpeciesInventory; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE gisdb.public."dataSpeciesInventory"(
  "LineKey" VARCHAR(100),
  "RecKey" VARCHAR(100),
  "DateModified" DATE,
  --"FormType" TEXT, --dropped
  "FormDate" DATE,
  "Observer" TEXT,
  "Recorder" TEXT,
  "DataEntry" TEXT,
  "DataErrorChecking" TEXT,
  "SpecRichMethod" INT,
  "SpecRichMeasure" INT,
  "SpecRichNbrSubPlots" INT,
  "SpecRich1Container" INT,
  "SpecRich1Shape" INT,
  "SpecRich1Dim1" NUMERIC,
  "SpecRich1Dim2" NUMERIC,
  "SpecRich1Area" NUMERIC,
  "Notes" TEXT,
  "DateLoadedInDb" DATE,
  "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
  "DBKey" TEXT,
  "Species" TEXT,
  "source" TEXT,
  "Density" INT);

--
-- Name: dataHeight; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE gisdb.public."dataHeight"(
  "PrimaryKey" TEXT REFERENCES gisdb.public."dataHeader"("PrimaryKey"),
  "DBKey" TEXT,
  "PointLoc" NUMERIC,
  "PointNbr" INT,
  "RecKey" VARCHAR(100),
  "Height" NUMERIC,
  "Species" TEXT,
  "Chkbox" INT,
  "type" TEXT,
  "GrowthHabit_measured" TEXT,
  "LineKey" VARCHAR(100),
  "DateModified" DATE,
  "FormType" TEXT,
  "FormDate" DATE,
  "Observer" TEXT,
  "Recorder" TEXT,
  "DataEntry" TEXT,
  "DataErrorChecking" TEXT,
  "Direction" VARCHAR(100),
  "Measure" INT,
  "LineLengthAmount" NUMERIC,
  --"SpacingIntervalAmount" NUMERIC, --dropped
  --"SpacingType" TEXT,  -- dropped
  "HeightOption" TEXT,
  "HeightUOM" TEXT,
  --"ShowCheckbox" INT,  --dropped
  "CheckboxLabel" TEXT,
  "source" TEXT);
  --"UOM" TEXT); --dropped

--
-- Name: userInfo; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE gisdb.public."userInfo"(
  "First" VARCHAR(50),
  "Last" VARCHAR(50),
  "Organization" TEXT,
  "UserID" INT, -- potential PK
  "RoleName" VARCHAR(10), -- potential FK to role table
  "Token" VARCHAR(50));
