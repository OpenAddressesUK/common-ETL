-- phpMyAdmin SQL Dump
-- version 4.0.9deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 29, 2014 at 12:47 PM
-- Server version: 5.5.40-MariaDB-1~wheezy
-- PHP Version: 5.4.4-14+deb7u14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `oa_alpha_etl`
--

-- --------------------------------------------------------

--
-- Table structure for table `ONSPD`
--

CREATE TABLE IF NOT EXISTS `ONSPD` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `pcds` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `usertype` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `EA` int(11) DEFAULT NULL,
  `NO` int(11) DEFAULT NULL,
  `osgrdind` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ctry` char(1) COLLATE utf8_unicode_ci NOT NULL,
  `current` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `pcds` (`pcds`),
  KEY `NO` (`NO`),
  KEY `EA` (`EA`),
  KEY `ctry` (`ctry`),
  KEY `Current` (`current`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2561456 ;

-- --------------------------------------------------------

--
-- Table structure for table `ONSPD_Changes`
--

CREATE TABLE IF NOT EXISTS `ONSPD_Changes` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `curr_pcds` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `term_pcds` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `term_pcds` (`term_pcds`),
  KEY `curr_pcds` (`curr_pcds`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=128166 ;

-- --------------------------------------------------------

--
-- Table structure for table `OS_Locator`
--

CREATE TABLE IF NOT EXISTS `OS_Locator` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Classification` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Centx` int(11) NOT NULL,
  `Centy` int(11) NOT NULL,
  `Minx` int(11) NOT NULL,
  `Maxx` int(11) NOT NULL,
  `Miny` int(11) NOT NULL,
  `Maxy` int(11) NOT NULL,
  `Settlement` varchar(120) COLLATE utf8_unicode_ci NOT NULL,
  `Locality` varchar(120) COLLATE utf8_unicode_ci NOT NULL,
  `Cou_Unit` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `Local Authority` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `Tile_10k` varchar(6) COLLATE utf8_unicode_ci NOT NULL,
  `Tile_25k` varchar(4) COLLATE utf8_unicode_ci NOT NULL,
  `Source` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Name` (`Name`),
  KEY `Centx` (`Centx`),
  KEY `Centy` (`Centy`),
  KEY `Minx` (`Minx`),
  KEY `Maxx` (`Maxx`),
  KEY `Miny` (`Miny`),
  KEY `Maxy` (`Maxy`),
  KEY `Locality` (`Locality`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=867836 ;

-- --------------------------------------------------------

--
-- Table structure for table `Settlements`
--

CREATE TABLE IF NOT EXISTS `Settlements` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `OS_Code` int(11) NOT NULL,
  `Type` char(1) COLLATE utf8_unicode_ci NOT NULL,
  `Name` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `Cym_Name` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Admin` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `Cym_Admin` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Easting` int(11) NOT NULL,
  `Northing` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Type` (`Type`),
  KEY `Name` (`Name`),
  KEY `Cym_Name` (`Cym_Name`),
  KEY `Admin` (`Admin`),
  KEY `Cym_Admin` (`Cym_Admin`),
  KEY `Easting` (`Easting`),
  KEY `Northing` (`Northing`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=25430 ;

-- --------------------------------------------------------

--
-- Table structure for table `Street_Types`
--

CREATE TABLE IF NOT EXISTS `Street_Types` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Street` varchar(60) COLLATE utf8_unicode_ci NOT NULL,
  `Count` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Street` (`Street`),
  KEY `Count` (`Count`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=651 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
