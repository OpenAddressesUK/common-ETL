-- phpMyAdmin SQL Dump
-- version 4.0.9deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 21, 2014 at 04:53 PM
-- Server version: 5.5.39-MariaDB-1~wheezy
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
-- Table structure for table `ONSPD_Changes`
--

CREATE TABLE IF NOT EXISTS `ONSPD_Changes` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `CurrPCS` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `TermPCS` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `TermPCS` (`TermPCS`),
  KEY `CurrPCS` (`CurrPCS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ONSPD_Curr`
--

CREATE TABLE IF NOT EXISTS `ONSPD_Curr` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `pcds` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `usertype` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `EA` int(11) DEFAULT NULL,
  `NO` int(11) DEFAULT NULL,
  `osgrdind` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ctry` char(1) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `pcds` (`pcds`),
  KEY `NO` (`NO`),
  KEY `EA` (`EA`),
  KEY `ctry` (`ctry`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ONSPD_Term`
--

CREATE TABLE IF NOT EXISTS `ONSPD_Term` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `pcds` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `usertype` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `EA` int(11) DEFAULT NULL,
  `NO` int(11) DEFAULT NULL,
  `osgrdind` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ctry` char(1) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `pcds` (`pcds`),
  KEY `EA` (`EA`),
  KEY `NO` (`NO`),
  KEY `ctry` (`ctry`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

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
  KEY `Name` (`Name`,`Classification`,`Minx`,`Maxx`,`Miny`,`Maxy`,`Settlement`,`Locality`,`Cou_Unit`,`Local Authority`,`Tile_10k`,`Tile_25k`,`Centx`,`Centy`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
