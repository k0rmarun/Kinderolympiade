DROP TABLE IF EXISTS LG_NGD;
DROP TABLE IF EXISTS LG_NGD_Ergebnisse;

CREATE TABLE `LG_NGD` (
  `ID` int(11) NOT NULL,
  `Name` varchar(32) NOT NULL,
  `Vorname` varchar(32) NOT NULL,
  `WieAlt` integer NOT NULL,
  `Geschlecht` boolean NOT NULL,
  PRIMARY KEY (`ID`)
);

CREATE TABLE `LG_NGD_Ergebnisse` (
  `ID` integer NOT NULL,
  `UID` integer NOT NULL,
  `Typ` integer NOT NULL,
  `Wert1` float DEFAULT NULL,
  `Wert2` float DEFAULT NULL,
  `Wert3` float DEFAULT NULL,
  PRIMARY KEY (`ID`)
);