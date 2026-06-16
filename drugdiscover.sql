/*
SQLyog Community v13.3.0 (64 bit)
MySQL - 10.4.32-MariaDB : Database - drugdiscover
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`drugdiscover` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `drugdiscover`;

/*Table structure for table `account` */

DROP TABLE IF EXISTS `account`;

CREATE TABLE `account` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `username` varchar(500) DEFAULT NULL,
  `mno` varchar(500) DEFAULT NULL,
  `email` varchar(500) DEFAULT NULL,
  `password` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `account` */

insert  into `account`(`id`,`username`,`mno`,`email`,`password`) values 
(4,'RAJESWARI SAMUTHIRAKANI','08667622696','reginapeterlio@gmail.com','reginapeterlio@gmail.com'),
(5,'Test1','08667622696','Test1@gmail.com','Test1@gmail.com'),
(6,'Test2','08667622696','Test2@gmail.com','Test2@gmail.com'),
(7,'Test3','08667622696','Test3@gmail.com','Test3@gmail.com'),
(8,'Peter','08667622696','Test4@gmail.com','Test4@gmail.com'),
(9,'Raji','08667622696','reginapeterliorrr@gmail.conm','reginapeterliorrr@gmail.conm'),
(10,'swetha','9087654321','swetha@gmail.com','swetha@gmail.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
