-- MySQL dump 10.13  Distrib 5.5.41, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: codegalaxy
-- ------------------------------------------------------
-- Server version	5.5.41-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `answer`
--

USE codegalaxy

DROP TABLE IF EXISTS `answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `answer` (
  `answer_number` int(11) NOT NULL,
  `answer_text` blob NOT NULL,
  `language_id` int(11) NOT NULL DEFAULT '0',
  `is_answer_for` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`is_answer_for`,`answer_number`,`language_id`),
  KEY `language_id` (`language_id`),
  CONSTRAINT `answer_ibfk_1` FOREIGN KEY (`language_id`) REFERENCES `language` (`id`),
  CONSTRAINT `answer_ibfk_2` FOREIGN KEY (`is_answer_for`) REFERENCES `exercise` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answer`
--

LOCK TABLES `answer` WRITE;
/*!40000 ALTER TABLE `answer` DISABLE KEYS */;
INSERT INTO `answer` VALUES (1,'Hello Galaxy!',1,1),(1,'4',1,2),(1,'build\r\nbuild\r\nbuild\r\nbuild\r\nbuild\r\nbuild\r\nbuild\r\nbuild\r\nbuild\r\nbuild',1,3),(1,'10\r\n9\r\n8\r\n7\r\n6\r\n5\r\n4\r\n3\r\n2\r\n1\r\n0\r\n',1,4),(1,'Loop',1,5),(1,'',2,5),(2,'Variable',1,5),(2,'',2,5),(3,'Classes',1,5),(3,'',2,5),(4,'',2,5);
/*!40000 ALTER TABLE `answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_0e939a4f` (`group_id`),
  KEY `auth_group_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_group_permissions_group_id_4b2a2571371856a_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group__permission_id_72323e39aa3cfe35_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_417f1b1c` (`content_type_id`),
  CONSTRAINT `auth__content_type_id_7e4fe414a08e38b4_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_e8701ad4` (`user_id`),
  KEY `auth_user_groups_0e939a4f` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_7770b64db6ca18c5_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_3b0bb466d6afbc07_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_e8701ad4` (`user_id`),
  KEY `auth_user_user_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_user_user_permissi_user_id_4a8007655ec4ec73_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_u_permission_id_21bd890699b6d60a_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `code`
--

DROP TABLE IF EXISTS `code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `code` (
  `code_text` blob,
  `exercise_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`exercise_id`),
  CONSTRAINT `code_ibfk_1` FOREIGN KEY (`exercise_id`) REFERENCES `exercise` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `code`
--

LOCK TABLES `code` WRITE;
/*!40000 ALTER TABLE `code` DISABLE KEYS */;
INSERT INTO `code` VALUES ('print(\"\")',1),('distance_1 = 1\r\ndistance_2 = 3',2),('for every_time in range(10):\r\n  print(\"\")',3),('num_list = [10,9,8,7,6,5,4,3,2,1,0]',4);
/*!40000 ALTER TABLE `code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_417f1b1c` (`content_type_id`),
  KEY `django_admin_log_e8701ad4` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_233a481da04ec558_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django__content_type_id_235e46beb836cf_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_6ba5864255c5100a_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2015-04-19 15:48:52'),(2,'auth','0001_initial','2015-04-19 15:48:56'),(3,'admin','0001_initial','2015-04-19 15:48:58'),(4,'sessions','0001_initial','2015-04-19 15:48:58');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('66s6tf8x17okhyrrzz5uti6o9xlow5m7','NDBhM2U2NTNmMDQ0NDY5ZTg2ODg0NTgxMjUxNTc0ZmFhMjUyZDdlNDp7ImN1cnJlbnRfdXNlciI6NH0=','2015-05-08 20:06:02'),('7c01vgq3qlm5arz8cwk6shd3a388wllt','NzJkNjVlNzAwYzI3Y2VkOGM4MWZmNjdjYjU2MDE1OWMzZTQwMWQ4Mzp7ImN1cnJlbnRfdXNlciI6Mn0=','2015-05-09 12:54:34');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exercise`
--

DROP TABLE IF EXISTS `exercise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exercise` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `max_score` int(11) NOT NULL,
  `penalty` int(11) NOT NULL,
  `exercise_type` varchar(255) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_on` datetime NOT NULL,
  `exercise_number` int(11) NOT NULL,
  `correct_answer` int(11) NOT NULL,
  `exerciseList_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exerciseList_id` (`exerciseList_id`),
  CONSTRAINT `exercise_ibfk_1` FOREIGN KEY (`exerciseList_id`) REFERENCES `exerciseList` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exercise`
--

LOCK TABLES `exercise` WRITE;
/*!40000 ALTER TABLE `exercise` DISABLE KEYS */;
INSERT INTO `exercise` VALUES (1,4,1,'Code',4,'2015-04-19 16:44:15',1,1,1),(2,7,1,'Code',4,'2015-04-19 17:08:47',2,1,1),(3,5,1,'Code',4,'2015-04-19 17:20:12',3,1,1),(4,5,1,'Code',4,'2015-04-21 15:11:06',1,1,2),(5,2,3,'Open Question',3,'2015-04-25 11:46:17',1,1,6);
/*!40000 ALTER TABLE `exercise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exerciseList`
--

DROP TABLE IF EXISTS `exerciseList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exerciseList` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `difficulty` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_on` datetime NOT NULL,
  `prog_lang_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `prog_lang_id` (`prog_lang_id`),
  CONSTRAINT `exerciseList_ibfk_1` FOREIGN KEY (`prog_lang_id`) REFERENCES `programmingLanguage` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exerciseList`
--

LOCK TABLES `exerciseList` WRITE;
/*!40000 ALTER TABLE `exerciseList` DISABLE KEYS */;
INSERT INTO `exerciseList` VALUES (1,1,4,'2015-04-19 15:50:35',1),(2,2,4,'2015-04-21 14:53:41',1),(3,1,4,'2015-04-21 16:14:44',2),(4,3,4,'2015-04-21 16:18:33',2),(5,2,2,'2015-04-25 11:34:23',1),(6,1,3,'2015-04-25 11:40:54',1);
/*!40000 ALTER TABLE `exerciseList` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exerciseTitle`
--

DROP TABLE IF EXISTS `exerciseTitle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exerciseTitle` (
  `title` varchar(255) NOT NULL,
  `language_id` int(11) NOT NULL,
  `exercise_id` int(11) NOT NULL,
  PRIMARY KEY (`language_id`,`exercise_id`),
  KEY `exercise_id` (`exercise_id`),
  CONSTRAINT `exerciseTitle_ibfk_1` FOREIGN KEY (`exercise_id`) REFERENCES `exercise` (`id`),
  CONSTRAINT `exerciseTitle_ibfk_2` FOREIGN KEY (`language_id`) REFERENCES `language` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exerciseTitle`
--

LOCK TABLES `exerciseTitle` WRITE;
/*!40000 ALTER TABLE `exerciseTitle` DISABLE KEYS */;
INSERT INTO `exerciseTitle` VALUES ('Hello Galaxy!',1,1),('Number crunching',1,2),('So much work to do...',1,3),('Countdown!',1,4),('Back to building...',1,5),('Getallen verwerken',2,2),('Zo veel werk te doen...',2,3),('',2,5);
/*!40000 ALTER TABLE `exerciseTitle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exercise_references`
--

DROP TABLE IF EXISTS `exercise_references`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exercise_references` (
  `original_id` int(11) NOT NULL,
  `new_list_id` int(11) NOT NULL,
  `new_list_exercise_number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exercise_references`
--

LOCK TABLES `exercise_references` WRITE;
/*!40000 ALTER TABLE `exercise_references` DISABLE KEYS */;
/*!40000 ALTER TABLE `exercise_references` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `friendsWith`
--

DROP TABLE IF EXISTS `friendsWith`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `friendsWith` (
  `user_id` int(11) NOT NULL,
  `friend_id` int(11) NOT NULL,
  `befriended_on` datetime NOT NULL,
  `status` enum('Pending','Blocked','Friends') NOT NULL,
  PRIMARY KEY (`user_id`,`friend_id`),
  KEY `friend_id` (`friend_id`),
  CONSTRAINT `friendsWith_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `friendsWith_ibfk_2` FOREIGN KEY (`friend_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `friendsWith`
--

LOCK TABLES `friendsWith` WRITE;
/*!40000 ALTER TABLE `friendsWith` DISABLE KEYS */;
INSERT INTO `friendsWith` VALUES (1,2,'2015-03-06 05:12:12','Friends'),(1,3,'2015-04-01 12:12:14','Friends'),(1,4,'2015-03-12 12:12:14','Friends'),(1,6,'2015-03-16 12:12:15','Friends'),(1,8,'2015-04-03 12:12:15','Friends'),(1,13,'2015-02-08 03:12:16','Friends'),(1,16,'2015-03-06 12:12:17','Friends'),(1,20,'2015-03-11 08:12:18','Friends'),(2,6,'2015-03-15 05:12:12','Friends'),(2,7,'2015-03-01 12:12:14','Friends'),(2,11,'2015-04-06 05:12:12','Friends'),(2,13,'2015-03-11 12:12:14','Friends'),(2,15,'2015-04-03 12:12:15','Friends'),(2,16,'2015-02-06 03:12:16','Friends'),(2,18,'2015-03-18 12:12:17','Friends'),(2,19,'2015-03-06 08:12:18','Friends'),(3,4,'2015-03-01 12:12:14','Friends'),(3,5,'2015-03-03 12:12:15','Friends'),(3,6,'2015-02-01 03:12:16','Friends'),(3,7,'2015-04-06 12:12:17','Friends'),(3,8,'2015-03-04 08:12:18','Friends'),(3,9,'2015-04-06 12:12:19','Friends'),(3,10,'2015-03-06 12:22:12','Friends'),(3,11,'2015-03-23 10:32:12','Friends'),(3,12,'2015-03-07 12:42:12','Friends'),(3,13,'2015-04-05 11:52:12','Friends'),(3,14,'2015-03-06 13:12:12','Friends'),(3,15,'2015-04-09 14:12:12','Friends'),(3,16,'2015-03-06 15:12:12','Friends'),(3,17,'2015-03-06 01:12:12','Friends'),(3,18,'2015-04-05 17:12:12','Friends'),(3,19,'2015-01-10 18:12:12','Friends'),(3,20,'2015-03-06 19:12:12','Friends'),(4,5,'2015-03-28 12:12:19','Friends'),(4,7,'2015-04-06 12:22:12','Friends'),(4,14,'2015-03-07 10:32:12','Friends'),(5,9,'2015-03-07 12:42:12','Friends'),(5,10,'2015-03-21 11:52:12','Friends'),(5,14,'2015-04-06 13:12:12','Friends'),(5,15,'2015-03-16 14:12:12','Friends'),(5,16,'2015-03-04 15:12:12','Friends'),(5,20,'2015-04-06 01:12:12','Friends'),(6,7,'2015-03-05 17:12:12','Friends'),(6,8,'2015-01-06 18:12:12','Friends'),(6,9,'2015-03-23 19:12:12','Friends'),(7,11,'2015-04-06 18:12:12','Friends'),(7,13,'2015-04-06 19:12:12','Friends'),(7,14,'2015-03-05 17:12:12','Friends'),(7,16,'2015-01-06 18:12:12','Friends'),(7,19,'2015-03-06 19:12:12','Friends'),(8,10,'2015-04-06 19:12:12','Friends'),(8,11,'2015-03-05 17:12:12','Friends'),(8,18,'2015-04-06 18:12:12','Friends'),(8,20,'2015-03-06 19:12:12','Friends'),(9,13,'2015-03-05 17:12:12','Friends'),(9,14,'2015-01-06 18:12:12','Friends'),(9,15,'2015-04-06 19:12:12','Friends'),(10,12,'2015-03-06 19:12:12','Friends'),(11,10,'2015-03-06 19:12:12','Friends'),(11,13,'2015-03-05 17:12:12','Friends'),(11,14,'2015-01-22 18:12:12','Friends'),(11,15,'2015-04-21 19:12:12','Friends'),(11,17,'2015-03-05 17:12:12','Friends'),(11,19,'2015-04-19 18:12:12','Friends'),(12,18,'2015-03-05 17:12:12','Friends'),(12,19,'2015-04-21 18:12:12','Friends'),(12,20,'2015-03-06 19:12:12','Friends'),(13,14,'2015-03-05 17:12:12','Friends'),(13,15,'2015-01-06 18:12:12','Friends'),(13,17,'2015-04-02 19:12:12','Friends'),(13,18,'2015-03-05 17:12:12','Friends'),(14,16,'2015-03-05 17:12:12','Friends'),(15,16,'2015-04-09 17:12:12','Friends'),(17,19,'2015-03-05 17:12:12','Friends');
/*!40000 ALTER TABLE `friendsWith` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(255) NOT NULL,
  `group_type` int(11) NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_name` (`group_name`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groups`
--

LOCK TABLES `groups` WRITE;
/*!40000 ALTER TABLE `groups` DISABLE KEYS */;
INSERT INTO `groups` VALUES (1,'Admins',0,'2015-03-06 19:12:12'),(2,'OLVE',1,'2015-03-06 19:12:12'),(3,'OLVC',1,'2015-03-06 19:12:12'),(4,'Sint-Michielscollege',1,'2015-03-06 19:12:12'),(5,'Universiteit Antwerpen',1,'2015-03-06 19:12:12'),(6,'Universiteit Gent',1,'2015-03-06 19:12:12'),(7,'KDG',1,'2015-03-06 19:12:12'),(8,'VUB',1,'2015-03-06 19:12:12'),(9,'De bende van de bosklapper',1,'2015-03-06 19:12:12'),(10,'NVA sympathisanten',1,'2015-03-06 19:12:12'),(11,'Groen! sympathisanten',1,'2015-03-06 19:12:12'),(12,'PVDA sympathisanten',1,'2015-03-06 19:12:12'),(13,'Open-VLD sympathisanten',1,'2015-03-06 19:12:12'),(14,'sp.a sympathisanten',1,'2015-03-06 19:12:12'),(15,'Vlaanderen',0,'2015-03-06 19:12:12'),(16,'Wallonie',0,'2015-03-06 19:12:12'),(17,'Brussel',0,'2015-03-06 19:12:12'),(18,'Antwerpen',0,'2015-03-06 19:12:12'),(19,'Russia',0,'2015-03-06 19:12:12'),(20,'Nederland',0,'2015-03-06 19:12:12'),(21,'Great-Britain',0,'2015-03-06 19:12:12'),(22,'USA',0,'2015-03-06 19:12:12'),(23,'Wilrijk',0,'2015-03-06 19:12:12'),(24,'Edegem',0,'2015-03-06 19:12:12'),(25,'Mechelen',0,'2015-03-06 19:12:12'),(26,'Brasschaat',0,'2015-03-06 19:12:12'),(27,'Merksem',0,'2015-03-06 19:12:12'),(28,'Schoten',0,'2015-03-06 19:12:12'),(29,'Knokke',0,'2015-03-06 19:12:12'),(30,'Aartselaar',0,'2015-03-06 19:12:12');
/*!40000 ALTER TABLE `groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hasSubject`
--

DROP TABLE IF EXISTS `hasSubject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hasSubject` (
  `exerciseList_id` int(11) NOT NULL DEFAULT '0',
  `subject_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`exerciseList_id`,`subject_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `hasSubject_ibfk_1` FOREIGN KEY (`exerciseList_id`) REFERENCES `exerciseList` (`id`),
  CONSTRAINT `hasSubject_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hasSubject`
--

LOCK TABLES `hasSubject` WRITE;
/*!40000 ALTER TABLE `hasSubject` DISABLE KEYS */;
INSERT INTO `hasSubject` VALUES (1,1),(3,1),(6,1),(1,2),(2,2),(5,2),(6,2),(1,3),(6,3),(1,4),(2,4),(6,4),(3,5),(4,6),(4,7),(5,8),(5,9);
/*!40000 ALTER TABLE `hasSubject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hint`
--

DROP TABLE IF EXISTS `hint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hint` (
  `hint_text` varchar(255) DEFAULT NULL,
  `hint_number` int(11) NOT NULL DEFAULT '0',
  `exercise_id` int(11) NOT NULL DEFAULT '0',
  `language_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`hint_number`,`exercise_id`,`language_id`),
  KEY `language_id` (`language_id`),
  KEY `exercise_id` (`exercise_id`),
  CONSTRAINT `hint_ibfk_1` FOREIGN KEY (`language_id`) REFERENCES `language` (`id`),
  CONSTRAINT `hint_ibfk_2` FOREIGN KEY (`exercise_id`) REFERENCES `exercise` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hint`
--

LOCK TABLES `hint` WRITE;
/*!40000 ALTER TABLE `hint` DISABLE KEYS */;
INSERT INTO `hint` VALUES ('print(\"Hello\") will display \"Hello\".',1,1,1),('\'distance_3 = ...\' will create a new variable called \'distance_3\'',1,2,1),('\'distance_3 = ...\' zal een nieuwe variabele genaamd distance_3 creëren',1,2,2),('This exercise is almost the same as the first exercise! Look at that one if you are stuck!',1,3,1),('Deze vraag is bijna dezelfde als de eerste! Kijk daar terug naar indien je vastzit!',1,3,2),('The for loop could look like this: \"for something in something else:\" and then you put another command below that',1,4,1),('Dont forget upper case letters and the exclamation mark!',2,1,1),('c = a + b will add two variables, called a and b, together and put the end result into the variable c',2,2,1),('\'c = a + b\' zal twee variabelen genaamd a en b optellen en zal het eindresultaat in de variabele c steken',2,2,2),('Don\'t forget the indentation!',2,4,1);
/*!40000 ALTER TABLE `hint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `language`
--

DROP TABLE IF EXISTS `language`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `language` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `language_code` varchar(225) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `language`
--

LOCK TABLES `language` WRITE;
/*!40000 ALTER TABLE `language` DISABLE KEYS */;
INSERT INTO `language` VALUES (1,'English','en'),(2,'Nederlands','nl');
/*!40000 ALTER TABLE `language` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `listTranslation`
--

DROP TABLE IF EXISTS `listTranslation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `listTranslation` (
  `name` varchar(255) NOT NULL,
  `language_id` int(11) NOT NULL,
  `description` blob NOT NULL,
  `list_id` int(11) NOT NULL,
  PRIMARY KEY (`list_id`,`language_id`),
  KEY `language_id` (`language_id`),
  CONSTRAINT `listTranslation_ibfk_1` FOREIGN KEY (`list_id`) REFERENCES `exerciseList` (`id`),
  CONSTRAINT `listTranslation_ibfk_2` FOREIGN KEY (`language_id`) REFERENCES `language` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listTranslation`
--

LOCK TABLES `listTranslation` WRITE;
/*!40000 ALTER TABLE `listTranslation` DISABLE KEYS */;
INSERT INTO `listTranslation` VALUES ('Beginning of a journey',1,'Hello, my name is Kernel, and my friend Grub and I seem to be stranded on this strange planet called Earth. We\'re going to try to signal our spaceship with the Universal language Python, could you lend us a hand please? I promise it won\'t be too difficult',1),('Begin van een avontuur',2,'Hallo, ik ben Kernel, en mijn vriend Grub en ik zijn gestrand op deze vreemde planeet genaamd Aarde! We gaan proberen ons ruimteschip een signaal te sturen met de Universele taal Python. Zou je ons mischien even een handje willen lenen? Ik beloof je dat het niet te moeilijk wordt!',1),('Continuation of that journey...',1,'We\'re in outer space! join me and my friend Grub on our trip through the galaxy!',2),('Het avontuur gaat door...',2,'We zijn in de ruimte! Vergezel Grub en ik in onze tocht door het sterrenstelsel!',2),('C++ for Dummies',1,'Hello there, i\'m Tristan and i made this list to explain/teach you some basic C++ syntax. This list will get you experimenting in no time! Be sure to visit the sandboxmode to test out the things you learned!',3),('C++ voor Dummies',2,'Hallo, ik ben Tristan en ik heb deze lijst gemaakt om je basis C++ syntax uit te leggen/leren. Met deze lijst kan je zo beginnen experimenteren! Bezoek zeker ook de sandbox om de dingen die je hebt geleerd uit te testen!',3),('C++: Basic math functions',1,'This list will teach you to write some basic math functions, these can typically already be found in the standard/math library, but i wish to adress them anyway. I hope these put your mind to thinking, Happy Coding!',4),('C++: Basis wiskundige functies',2,'Deze lijst zal je leren wat basis-wiskundige functies te schrijven, deze vind je meestal wel in de standaard/math library, maar ik wil ze toch even aanhalen. Ik hoop dat deze je toch tot denken doen aanzetten. Veel plezier met het Coden!',4),('Thierry\'s coding Extravaganza',1,'Howdy! This kool list will go over the basic principles of coding like a BOSS. Hope ya enjoy it fellas!!!1!',5),('Thierry\'s Coding Extravaganza',2,'Goedendag beste heren, ik wens u iets bij te brengen ivm een begrip genaamd coderen, ik hoop dat dit een behulpzame oefeningenlijst is.',5),('Seems we crashed...again',1,'Grub lost control of the ship! We\'ve landed on the moon, guess we\'ll need to build a new spaceship...',6),('We zijn opnieuw gecrasht!',2,'Grub verloor controle over het schip! We zijn op de maan geland, dus we bouwen best een nieuw ruimteschip...',6);
/*!40000 ALTER TABLE `listTranslation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `madeEx`
--

DROP TABLE IF EXISTS `madeEx`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `madeEx` (
  `user_id` int(11) NOT NULL DEFAULT '0',
  `solved` tinyint(1) NOT NULL,
  `exercise_score` int(11) NOT NULL,
  `completed_on` datetime DEFAULT NULL,
  `list_id` int(11) NOT NULL DEFAULT '0',
  `exercise_number` int(11) NOT NULL DEFAULT '0',
  `last_answer` blob,
  `hints_used` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`,`exercise_number`,`list_id`),
  CONSTRAINT `madeEx_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `madeEx`
--

LOCK TABLES `madeEx` WRITE;
/*!40000 ALTER TABLE `madeEx` DISABLE KEYS */;
INSERT INTO `madeEx` VALUES (2,1,0,'2015-04-25 12:55:19',1,1,'print(\"Hello Galaxy!\")',2),(2,1,3,'2015-04-25 13:05:15',2,1,'num_list = [10,9,8,7,6,5,4,3,2,1,0]\r\nfor i in num_list:\r\n  print(i)',0),(2,1,7,'2015-04-25 12:55:36',1,2,'distance_1 = 1\r\ndistance_2 = 3\r\nprint(4) # cheating ftw',0),(2,1,2,'2015-04-25 13:02:46',1,3,'for every_time in range(10):\r\n  print(\"build\")',0),(3,1,2,'2015-04-25 12:39:25',1,1,'print(\"Hello Galaxy!\")',1),(3,1,5,'2015-04-25 12:00:24',2,1,'num_list = [10,9,8,7,6,5,4,3,2,1,0]\r\nfor i in num_list:\r\n  print(i)',0),(3,1,6,'2015-04-25 12:39:53',1,2,'distance_1 = 1\r\ndistance_2 = 3\r\nprint(distance_1 + distance_2)',1),(3,1,4,'2015-04-25 12:40:18',1,3,'for every_time in range(10):\r\n  print(\"build\")',0);
/*!40000 ALTER TABLE `madeEx` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `madeList`
--

DROP TABLE IF EXISTS `madeList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `madeList` (
  `exerciseList_id` int(11) NOT NULL DEFAULT '0',
  `user_id` int(11) NOT NULL DEFAULT '0',
  `rating` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `made_on` datetime NOT NULL,
  `shared` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`exerciseList_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `madeList_ibfk_1` FOREIGN KEY (`exerciseList_id`) REFERENCES `exerciseList` (`id`),
  CONSTRAINT `madeList_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `madeList`
--

LOCK TABLES `madeList` WRITE;
/*!40000 ALTER TABLE `madeList` DISABLE KEYS */;
INSERT INTO `madeList` VALUES (1,2,2,69,'2015-04-25 14:55:42'),(1,3,4,75,'2015-04-25 14:40:12'),(2,2,2,60,'2015-04-25 15:05:15'),(2,3,0,100,'2015-04-25 14:00:24');
/*!40000 ALTER TABLE `madeList` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programmingLanguage`
--

DROP TABLE IF EXISTS `programmingLanguage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `programmingLanguage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programmingLanguage`
--

LOCK TABLES `programmingLanguage` WRITE;
/*!40000 ALTER TABLE `programmingLanguage` DISABLE KEYS */;
INSERT INTO `programmingLanguage` VALUES (2,'C++'),(1,'Python'),(3,'SQL');
/*!40000 ALTER TABLE `programmingLanguage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question` (
  `question_text` blob NOT NULL,
  `language_id` int(11) NOT NULL DEFAULT '0',
  `exercise_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`exercise_id`,`language_id`),
  KEY `language_id` (`language_id`),
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`exercise_id`) REFERENCES `exercise` (`id`),
  CONSTRAINT `question_ibfk_2` FOREIGN KEY (`language_id`) REFERENCES `language` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES ('First things first, we want to let everyone know we landed here. We can try to do so by sending them a visual message. The command \'print(\" \") should send everyone the message between the quotation marks, so try creating a message that will send \"Hello Galaxy!\"',1,1),('Good job sending the message! we\'ve just recieved an answer: they want us to give them the distance from between the Earth and the spaceship.  We already have some of the data stored in \'variables\'. These can be seen below in the form of variable = ... Try making your own variable and give it a value by adding the other veriables together on the right side of the \'=\' ! Then use the \'print\' command we just saw to send our friends above the correct distance!',1,2),('Goed gedaan bij het versturen van het bericht! We hebben net een antwoord ontvangen: ze willen dat we ze de afstand tussen de aarde en het ruimteschip geven. We hebben al een deel van de data opgeslagen in \'variabelen\'. Deze kan je hier beneden zien in de vorm van \'varaibele = waarde van de variabele\'. Probeer je eigen variabele te maken en geef het de waarde van de andere twee opgeteld aan de rechterkant van de \'=\' ! Gebruik dan het \'print\' commando dat we net zagen om onze vrienden hierboven de correcte afstnd te sturen!',2,2),('Allright! our spaceship will be arriving soon! However, they need a landing platform to land on! We shall need to build one by printing out \'build\' ten times. But instead of writing the same command so many times, you can use a \'loop\' which can do the command multiple times, which makes it a lot easier! The code written below will execute the print(\") command ten times, exactly as much as given by the range(10) command! Now let it write build every time!',1,3),('Geweldig! ons ruimteschip zal hier zo aankomen! Het heeft echter wel een platform nodig omop te landen, we zullen er zelf een moeten bouwen door \'build\' tien keer te printen. Maar in plaats van dat tien keer op te chrijven, kunnen we een \'loop\' gebruiken, wat het een pak makkelijker maakt! De code hieronder zal het \'print(\"\") commando tien keer uitvoeren, evenveel als aangegeven door het range(10) commando! Laat het nu telkens \'build\' printen',2,3),('We\'re about to fly away using our warpspeed, but we still need to count down from ten to zero!  Use a \"Loop\" like you\'ve learned, but this time, you can use a variable in the loop! We\'ve prepared a list with the numbers in them, print them using the variable after the \"for\" in the loop! And since you obviously want every number in the list, you put the \"num_list\" after the \"in\" . Good luck!',1,4),('Last time we used a construction to do one thing multiple times so we could build our landing station, what was this called?',1,5),('',2,5);
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
--

DROP TABLE IF EXISTS `subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subject` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` VALUES (9,'$$$'),(1,'Basic'),(4,'Conditionals'),(7,'Functions'),(2,'Loops'),(6,'Math'),(5,'Syntax'),(8,'Thierry'),(3,'Variables');
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `permission` int(11) DEFAULT '0',
  `joined_on` datetime NOT NULL,
  `last_login` datetime NOT NULL,
  `gender` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,1,'Root','Admin','e48e13207341b6bffb7fb1622282247b','root_admin_1337@hotmail.com',0,'1990-01-01 12:12:12','9999-12-31 12:12:12','U'),(2,1,'Thierry','Deruyttere','098f6bcd4621d373cade4e832627b4f6','thierryderuyttere@hotmail.com',0,'2015-03-06 12:12:12','2015-04-25 11:30:26','M'),(3,1,'Sten','Verbois','21232f297a57a5a743894a0e4a801fc3','stenverbois@gmail.com',0,'2015-03-06 12:12:12','2015-04-25 11:35:14','M'),(4,1,'Tristan','Vandeputte','21232f297a57a5a743894a0e4a801fc3','tristanvandeputte@hotmail.com',0,'2015-03-06 12:12:12','2015-04-24 20:06:02','M'),(5,1,'Marie','Kegeleers','21232f297a57a5a743894a0e4a801fc3','marie@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','F'),(6,1,'Maarten','Jorens','21232f297a57a5a743894a0e4a801fc3','maarten@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','F'),(7,1,'Dirk','Jan','21232f297a57a5a743894a0e4a801fc3','dirk@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','M'),(8,1,'Thomas','Vandelanotte','21232f297a57a5a743894a0e4a801fc3','Thomas@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','M'),(9,1,'Pieter','Jan','21232f297a57a5a743894a0e4a801fc3','Pieter@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','M'),(10,1,'Bart','De Wever','21232f297a57a5a743894a0e4a801fc3','Bart@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','M'),(11,1,'Chris','Brys','21232f297a57a5a743894a0e4a801fc3','Chris@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','M'),(12,1,'Jommeke','Hegre','21232f297a57a5a743894a0e4a801fc3','Jommeke@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','M'),(13,1,'Fany','Kiekeboe','21232f297a57a5a743894a0e4a801fc3','Fany@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','F'),(14,1,'Wouter','Vanuitdebroeken','21232f297a57a5a743894a0e4a801fc3','Wouter@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','M'),(15,1,'Kalm','Zalm','21232f297a57a5a743894a0e4a801fc3','Kalm@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','U'),(16,1,'Alaise','Pladijs','21232f297a57a5a743894a0e4a801fc3','Alaise@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','F'),(17,1,'Alain','Drissens','21232f297a57a5a743894a0e4a801fc3','Alain@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','M'),(18,1,'Rudy','Verboven','21232f297a57a5a743894a0e4a801fc3','Rudy@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','M'),(19,1,'Bruno','Tobback','21232f297a57a5a743894a0e4a801fc3','Bruno@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','M'),(20,1,'Janneman','Stanneman','21232f297a57a5a743894a0e4a801fc3','Janneman@hotmail.com',0,'2015-03-06 12:12:12','2015-03-06 12:12:12','M');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userInGroup`
--

DROP TABLE IF EXISTS `userInGroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userInGroup` (
  `group_id` int(11) NOT NULL DEFAULT '0',
  `user_id` int(11) NOT NULL DEFAULT '0',
  `user_permissions` int(11) DEFAULT NULL,
  `joined_on` datetime DEFAULT NULL,
  `status` enum('Pending','Blocked','Member') NOT NULL,
  PRIMARY KEY (`group_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `userInGroup_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`),
  CONSTRAINT `userInGroup_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userInGroup`
--

LOCK TABLES `userInGroup` WRITE;
/*!40000 ALTER TABLE `userInGroup` DISABLE KEYS */;
INSERT INTO `userInGroup` VALUES (1,1,0,'2015-03-06 13:42:33','Member'),(1,2,2,'2015-03-06 15:30:53','Pending'),(1,3,1,'2015-03-06 13:20:45','Member'),(1,4,1,'2015-03-06 13:11:55','Member'),(1,5,2,'2015-03-06 20:12:22','Member'),(1,6,2,'2015-03-06 12:20:20','Member'),(2,4,0,'2015-03-06 13:42:33','Member'),(2,6,2,'2015-03-06 15:30:53','Pending'),(2,7,2,'2015-03-06 13:20:45','Member'),(2,9,2,'2015-03-06 13:11:55','Member'),(2,17,2,'2015-03-06 20:12:22','Pending'),(2,18,2,'2015-03-06 12:20:20','Member'),(3,2,2,'2015-03-06 15:30:53','Member'),(3,3,2,'2015-03-06 13:20:45','Member'),(3,5,1,'2015-03-06 13:11:55','Member'),(3,7,2,'2015-03-06 20:12:22','Member'),(3,8,0,'2015-03-06 13:42:33','Member'),(3,9,1,'2015-03-06 15:30:53','Member'),(3,11,2,'2015-03-06 13:20:45','Member'),(3,13,2,'2015-03-06 13:11:55','Member'),(3,15,2,'2015-03-06 20:12:22','Member'),(3,16,2,'2015-03-06 12:20:20','Member'),(3,20,1,'2015-03-06 12:20:20','Member'),(4,13,0,'2015-03-06 13:42:33','Member'),(4,14,1,'2015-03-06 15:30:53','Member'),(5,7,0,'2015-03-06 20:12:22','Member'),(5,11,2,'2015-03-06 13:20:45','Pending'),(5,12,1,'2015-03-06 13:11:55','Member'),(5,17,2,'2015-03-06 12:20:20','Member'),(6,2,2,'2015-03-06 13:20:45','Member'),(6,4,1,'2015-03-06 13:11:55','Member'),(6,6,0,'2015-03-06 20:12:22','Member'),(6,11,2,'2015-03-06 12:20:20','Member'),(6,13,2,'2015-03-06 20:12:22','Member'),(6,15,2,'2015-03-06 12:20:20','Member'),(16,1,2,'2015-03-06 13:20:45','Member'),(16,2,1,'2015-03-06 13:11:55','Member'),(16,3,0,'2015-03-06 20:12:22','Member'),(16,4,2,'2015-03-06 12:20:20','Member'),(16,5,2,'2015-03-06 20:12:22','Member'),(16,6,2,'2015-03-06 12:20:20','Member'),(16,7,2,'2015-03-06 13:20:45','Member'),(16,8,1,'2015-03-06 13:11:55','Member'),(16,9,2,'2015-03-06 20:12:22','Member'),(16,10,1,'2015-03-06 12:20:20','Member'),(16,11,2,'2015-03-06 20:12:22','Member'),(16,13,2,'2015-03-06 12:20:20','Member'),(16,14,2,'2015-03-06 13:20:45','Pending'),(16,15,1,'2015-03-06 13:11:55','Member'),(16,16,2,'2015-03-06 20:12:22','Pending'),(16,17,2,'2015-03-06 12:20:20','Member'),(16,19,2,'2015-03-06 20:12:22','Member'),(16,20,2,'2015-03-06 12:20:20','Pending'),(17,12,1,'2015-03-06 13:20:45','Member'),(17,18,0,'2015-03-06 13:20:45','Member');
/*!40000 ALTER TABLE `userInGroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `verification`
--

DROP TABLE IF EXISTS `verification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `verification` (
  `email` varchar(255) NOT NULL,
  `hash` varchar(255) NOT NULL,
  PRIMARY KEY (`hash`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `hash` (`hash`),
  CONSTRAINT `verification_ibfk_1` FOREIGN KEY (`email`) REFERENCES `user` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `verification`
--

LOCK TABLES `verification` WRITE;
/*!40000 ALTER TABLE `verification` DISABLE KEYS */;
/*!40000 ALTER TABLE `verification` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-04-25 15:14:30
