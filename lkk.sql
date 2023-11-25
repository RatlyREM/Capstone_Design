-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: lkk
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `nickname` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `nickname` (`nickname`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (9,'pbkdf2_sha256$320000$1QgvqRDNoAoAfpnt4jPfVx$AfbHXFztGQwUwtdGXVPGgTprweKZt5nW55b3gCe4xdE=',NULL,'1234@naver.com','juho',0,1,1,'2023-11-22 22:10:38.159618','2023-11-22 22:10:38.159618'),(10,'pbkdf2_sha256$320000$HNjVo1JnNfUZ5mQMcTeqwg$+0NSkutR9ZqB0j6EUi8B3G11Pi7fQ8qhrRwtaxQr9/U=',NULL,'5678@naver.com','jong',0,1,1,'2023-11-23 19:26:51.543981','2023-11-23 19:26:51.543981');
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Accounts_user_groups_user_id_group_id_08e48791_uniq` (`user_id`,`group_id`),
  KEY `Accounts_user_groups_group_id_2d45a5ea_fk_auth_group_id` (`group_id`),
  CONSTRAINT `Accounts_user_groups_group_id_2d45a5ea_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `Accounts_user_groups_user_id_22b94888_fk_Accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Accounts_user_user_permi_user_id_permission_id_f5291c93_uniq` (`user_id`,`permission_id`),
  KEY `Accounts_user_user_p_permission_id_47be5b0d_fk_auth_perm` (`permission_id`),
  CONSTRAINT `Accounts_user_user_p_permission_id_47be5b0d_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `Accounts_user_user_p_user_id_a60df5b8_fk_Accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_userinfo`
--

DROP TABLE IF EXISTS `accounts_userinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_userinfo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone_number` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `address` varchar(80) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `userinfo_user_id_70851ceb_fk_Accounts_user_id` (`user_id`),
  CONSTRAINT `userinfo_user_id_70851ceb_fk_Accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_userinfo`
--

LOCK TABLES `accounts_userinfo` WRITE;
/*!40000 ALTER TABLE `accounts_userinfo` DISABLE KEYS */;
INSERT INTO `accounts_userinfo` VALUES (3,'김종학','01028482828','이편한',9);
/*!40000 ALTER TABLE `accounts_userinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Token',7,'add_token'),(26,'Can change Token',7,'change_token'),(27,'Can delete Token',7,'delete_token'),(28,'Can view Token',7,'view_token'),(29,'Can add token',8,'add_tokenproxy'),(30,'Can change token',8,'change_tokenproxy'),(31,'Can delete token',8,'delete_tokenproxy'),(32,'Can view token',8,'view_tokenproxy'),(33,'Can add user',9,'add_user'),(34,'Can change user',9,'change_user'),(35,'Can delete user',9,'delete_user'),(36,'Can view user',9,'view_user'),(37,'Can add user info',10,'add_userinfo'),(38,'Can change user info',10,'change_userinfo'),(39,'Can delete user info',10,'delete_userinfo'),(40,'Can view user info',10,'view_userinfo'),(41,'Can add equipment',11,'add_equipment'),(42,'Can change equipment',11,'change_equipment'),(43,'Can delete equipment',11,'delete_equipment'),(44,'Can view equipment',11,'view_equipment'),(45,'Can add log',12,'add_log'),(46,'Can change log',12,'change_log'),(47,'Can delete log',12,'delete_log'),(48,'Can view log',12,'view_log'),(49,'Can add favorites',13,'add_favorites'),(50,'Can change favorites',13,'change_favorites'),(51,'Can delete favorites',13,'delete_favorites'),(52,'Can view favorites',13,'view_favorites'),(53,'Can add board model',14,'add_boardmodel'),(54,'Can change board model',14,'change_boardmodel'),(55,'Can delete board model',14,'delete_boardmodel'),(56,'Can view board model',14,'view_boardmodel'),(57,'Can add renting',15,'add_renting'),(58,'Can change renting',15,'change_renting'),(59,'Can delete renting',15,'delete_renting'),(60,'Can view renting',15,'view_renting'),(61,'Can add returned',16,'add_returned'),(62,'Can change returned',16,'change_returned'),(63,'Can delete returned',16,'delete_returned'),(64,'Can view returned',16,'view_returned'),(65,'Can add returning',17,'add_returning'),(66,'Can change returning',17,'change_returning'),(67,'Can delete returning',17,'delete_returning'),(68,'Can view returning',17,'view_returning');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `board`
--

DROP TABLE IF EXISTS `board`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `board` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `u_id` bigint NOT NULL,
  `written_date` datetime(6) NOT NULL,
  `title` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `field` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `answer` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `hit_count` int NOT NULL DEFAULT '0',
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `table_b_mo_u_id_8d402dde_fk_Accounts_user_id` (`u_id`),
  CONSTRAINT `table_b_mo_u_id_8d402dde_fk_Accounts_user_id` FOREIGN KEY (`u_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `board`
--

LOCK TABLES `board` WRITE;
/*!40000 ALTER TABLE `board` DISABLE KEYS */;
INSERT INTO `board` VALUES (9,9,'2023-11-23 19:59:38.848490','배고파','밥주세요','확인했습니다',6,'2023-11-23 20:31:44.860689');
/*!40000 ALTER TABLE `board` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (9,'Accounts','user'),(10,'Accounts','userinfo'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(7,'authtoken','token'),(8,'authtoken','tokenproxy'),(14,'Board','boardmodel'),(13,'Bookmark','favorites'),(5,'contenttypes','contenttype'),(11,'Equipments','equipment'),(12,'Equipments','log'),(15,'Equipments','renting'),(16,'Equipments','returned'),(17,'Equipments','returning'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-11-12 07:39:42.781032'),(2,'auth','0001_initial','2023-11-12 07:39:43.132163'),(3,'admin','0001_initial','2023-11-12 07:39:43.236767'),(4,'admin','0002_logentry_remove_auto_add','2023-11-12 07:39:43.247736'),(5,'admin','0003_logentry_add_action_flag_choices','2023-11-12 07:39:43.257709'),(6,'contenttypes','0002_remove_content_type_name','2023-11-12 07:39:43.324056'),(7,'auth','0002_alter_permission_name_max_length','2023-11-12 07:39:43.369933'),(8,'auth','0003_alter_user_email_max_length','2023-11-12 07:39:43.402846'),(9,'auth','0004_alter_user_username_opts','2023-11-12 07:39:43.415543'),(10,'auth','0005_alter_user_last_login_null','2023-11-12 07:39:43.463421'),(11,'auth','0006_require_contenttypes_0002','2023-11-12 07:39:43.468435'),(12,'auth','0007_alter_validators_add_error_messages','2023-11-12 07:39:43.478393'),(13,'auth','0008_alter_user_username_max_length','2023-11-12 07:39:43.525600'),(14,'auth','0009_alter_user_last_name_max_length','2023-11-12 07:39:43.571465'),(15,'auth','0010_alter_group_name_max_length','2023-11-12 07:39:43.598399'),(16,'auth','0011_update_proxy_permissions','2023-11-12 07:39:43.613207'),(17,'auth','0012_alter_user_first_name_max_length','2023-11-12 07:39:43.662660'),(18,'authtoken','0001_initial','2023-11-12 07:39:43.714709'),(19,'authtoken','0002_auto_20160226_1747','2023-11-12 07:39:43.751611'),(20,'authtoken','0003_tokenproxy','2023-11-12 07:39:43.756195'),(21,'sessions','0001_initial','2023-11-12 07:39:43.785415'),(22,'Accounts','0001_initial','2023-11-12 12:16:50.581453'),(23,'Accounts','0002_alter_user_groups_alter_user_user_permissions','2023-11-12 14:57:31.028915'),(24,'Accounts','0003_userinfo','2023-11-12 17:01:06.957056'),(25,'Accounts','0004_alter_userinfo_table','2023-11-12 17:01:06.978255'),(26,'Equipments','0001_initial','2023-11-12 17:37:37.758408'),(27,'Equipments','0002_alter_equipment_options','2023-11-12 17:38:38.630520'),(28,'Equipments','0003_equipment_recommend_user','2023-11-12 17:57:56.178131'),(29,'Equipments','0002_alter_equipment_recommend_user','2023-11-21 17:09:52.207646'),(30,'Equipments','0003_equipment_created_at','2023-11-22 05:20:04.193849'),(31,'Equipments','0004_alter_equipment_created_at','2023-11-22 05:21:23.005914'),(32,'Equipments','0005_equipment_updated_at','2023-11-22 07:00:37.266847'),(33,'Equipments','0006_alter_equipment_updated_at','2023-11-22 08:29:37.304442'),(34,'Equipments','0002_alter_log_u','2023-11-22 13:17:58.367710'),(35,'Equipments','0003_log_updated_at','2023-11-22 14:19:41.104741'),(36,'Equipments','0004_alter_log_table','2023-11-22 14:40:18.255529'),(37,'Equipments','0005_alter_log_table','2023-11-22 14:41:55.066830'),(38,'Equipments','0006_rename_u_log_user_id_alter_log_user_id','2023-11-22 14:44:35.385594'),(39,'Bookmark','0001_initial','2023-11-22 15:38:57.377657'),(40,'Bookmark','0002_alter_favorites_model_name','2023-11-22 20:04:19.652798'),(41,'Board','0001_initial','2023-11-23 14:53:26.375863'),(42,'Board','0002_boardmodel_updated_at','2023-11-23 15:24:01.511204'),(43,'Equipments','0007_alter_equipment_updated_at_alter_log_updated_at','2023-11-23 15:24:54.353180'),(44,'Board','0003_alter_boardmodel_title','2023-11-23 16:43:39.744890'),(45,'Board','0004_alter_boardmodel_title','2023-11-23 16:47:54.575321'),(46,'Board','0005_alter_boardmodel_answer','2023-11-23 17:02:28.076130'),(47,'Equipments','0008_renting','2023-11-23 21:40:11.479083'),(48,'Equipments','0009_renting_log_id','2023-11-23 21:54:03.022079'),(49,'Equipments','0010_alter_log_id','2023-11-23 21:54:03.139219'),(50,'Equipments','0011_alter_renting_log_id','2023-11-23 21:54:27.904556'),(51,'Equipments','0012_renting_rent_accepted_date','2023-11-23 21:55:07.792539'),(52,'Equipments','0002_renting_rent_accepted_date','2023-11-23 22:09:22.178837'),(53,'Equipments','0003_alter_renting_rent_accepted_date','2023-11-23 22:10:03.766457'),(54,'Equipments','0004_alter_log_return_accepted_date_returned','2023-11-23 22:14:18.562922'),(55,'Equipments','0005_alter_returned_table','2023-11-23 22:15:30.000867'),(56,'Equipments','0006_returning','2023-11-23 22:17:59.217483'),(57,'Equipments','0007_alter_returning_table','2023-11-23 22:18:14.947699'),(58,'Equipments','0008_alter_renting_rent_accepted_date','2023-11-24 09:14:52.060082'),(59,'Equipments','0002_returned_user_id','2023-11-24 18:44:30.410808'),(60,'Equipments','0003_alter_returned_user_id','2023-11-24 18:46:33.417269');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment` (
  `model_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `price` int DEFAULT '0',
  `repository` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `total_rent` int DEFAULT '0',
  `total_stock` int DEFAULT '0',
  `current_stock` int DEFAULT '0',
  `manufacturer` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `recommend_count` int NOT NULL DEFAULT '0',
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`model_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment`
--

LOCK TABLES `equipment` WRITE;
/*!40000 ALTER TABLE `equipment` DISABLE KEYS */;
INSERT INTO `equipment` VALUES ('ABCD_1234','에어팟','Earphone',300000,'Inha_univ',7,10,80,'Apple',0,'2023-11-22 13:37:42.800892','2023-11-24 20:15:21.232613'),('ABCD_1234567','에어','Earphone',300000,'Inha_univ',0,10,7,'Apple',0,'2023-11-22 18:44:15.792394','2023-11-22 22:15:34.595427');
/*!40000 ALTER TABLE `equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment_recommend_user`
--

DROP TABLE IF EXISTS `equipment_recommend_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_recommend_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `equipment_id` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `equipment_recommend_user_equipment_id_user_id_ee8f06c0_uniq` (`equipment_id`,`user_id`),
  KEY `equipment_recommend_user_user_id_8e6bc3e1_fk_Accounts_user_id` (`user_id`),
  CONSTRAINT `equipment_recommend__equipment_id_4ca2b714_fk_equipment` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`model_name`),
  CONSTRAINT `equipment_recommend_user_user_id_8e6bc3e1_fk_Accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment_recommend_user`
--

LOCK TABLES `equipment_recommend_user` WRITE;
/*!40000 ALTER TABLE `equipment_recommend_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `equipment_recommend_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorites`
--

DROP TABLE IF EXISTS `favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `model_name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `u_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `favorites_model_name_328de720_fk_equipment_model_name` (`model_name`),
  KEY `favorites_u_id_6a78f8d0_fk_Accounts_user_id` (`u_id`),
  CONSTRAINT `favorites_model_name_328de720_fk_equipment_model_name` FOREIGN KEY (`model_name`) REFERENCES `equipment` (`model_name`),
  CONSTRAINT `favorites_u_id_6a78f8d0_fk_Accounts_user_id` FOREIGN KEY (`u_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorites`
--

LOCK TABLES `favorites` WRITE;
/*!40000 ALTER TABLE `favorites` DISABLE KEYS */;
/*!40000 ALTER TABLE `favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `u_id` bigint NOT NULL,
  `model_name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `rent_count` int NOT NULL DEFAULT '0',
  `return_deadline` datetime DEFAULT NULL,
  `rent_requested_date` datetime DEFAULT NULL,
  `rent_accepted_date` datetime DEFAULT NULL,
  `return_requested_date` datetime DEFAULT NULL,
  `return_accepted_date` datetime DEFAULT NULL,
  `rent_price` int DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `log_rent_accepted_date_8a3cc763_uniq` (`rent_accepted_date`),
  UNIQUE KEY `log_return_accepted_date_8aad1aff_uniq` (`return_accepted_date`),
  KEY `FK_log_equipment` (`model_name`),
  KEY `log_u_id_c380b807_fk_Accounts_user_id` (`u_id`),
  CONSTRAINT `FK_log_equipment` FOREIGN KEY (`model_name`) REFERENCES `equipment` (`model_name`),
  CONSTRAINT `log_u_id_c380b807_fk_Accounts_user_id` FOREIGN KEY (`u_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log`
--

LOCK TABLES `log` WRITE;
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
INSERT INTO `log` VALUES (42,9,'ABCD_1234',2,'2023-12-01 19:41:19','2023-11-24 19:41:19','2023-11-24 20:06:03','2023-11-24 20:06:43','2023-11-24 20:06:53',300000,'2023-11-24 20:06:52.869689'),(45,9,'ABCD_1234',2,'2023-12-01 20:15:18','2023-11-24 20:15:18',NULL,NULL,NULL,300000,'2023-11-24 20:15:18.085765'),(46,9,'ABCD_1234',2,'2023-12-01 20:15:20','2023-11-24 20:15:20',NULL,NULL,NULL,300000,'2023-11-24 20:15:19.743141'),(47,9,'ABCD_1234',2,'2023-12-01 20:15:21','2023-11-24 20:15:21',NULL,NULL,NULL,300000,'2023-11-24 20:15:21.240591');
/*!40000 ALTER TABLE `log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `renting`
--

DROP TABLE IF EXISTS `renting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `renting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `u_id` bigint NOT NULL,
  `log_id` int DEFAULT NULL,
  `rent_accepted_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rent_accepted_date` (`rent_accepted_date`),
  KEY `renting_u_id_be8ca3c3_fk_Accounts_user_id` (`u_id`),
  KEY `renting_log_id_c014f13a_fk_log_id` (`log_id`),
  CONSTRAINT `FK_renting_log` FOREIGN KEY (`rent_accepted_date`) REFERENCES `log` (`rent_accepted_date`),
  CONSTRAINT `renting_log_id_c014f13a_fk_log_id` FOREIGN KEY (`log_id`) REFERENCES `log` (`id`),
  CONSTRAINT `renting_u_id_be8ca3c3_fk_Accounts_user_id` FOREIGN KEY (`u_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `renting`
--

LOCK TABLES `renting` WRITE;
/*!40000 ALTER TABLE `renting` DISABLE KEYS */;
INSERT INTO `renting` VALUES (34,9,45,NULL),(35,9,46,NULL),(36,9,47,NULL);
/*!40000 ALTER TABLE `renting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `returned`
--

DROP TABLE IF EXISTS `returned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `returned` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `log_id` int DEFAULT NULL,
  `return_accepted_date` datetime DEFAULT NULL,
  `u_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Equipments_returned_log_id_87f33eb7_fk_log_id` (`log_id`),
  KEY `FK_returned_log` (`return_accepted_date`),
  KEY `returned_u_id_c13f6e52_fk_Accounts_user_id` (`u_id`),
  CONSTRAINT `Equipments_returned_log_id_87f33eb7_fk_log_id` FOREIGN KEY (`log_id`) REFERENCES `log` (`id`),
  CONSTRAINT `FK_returned_log` FOREIGN KEY (`return_accepted_date`) REFERENCES `log` (`return_accepted_date`),
  CONSTRAINT `returned_u_id_c13f6e52_fk_Accounts_user_id` FOREIGN KEY (`u_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `returned`
--

LOCK TABLES `returned` WRITE;
/*!40000 ALTER TABLE `returned` DISABLE KEYS */;
INSERT INTO `returned` VALUES (3,42,'2023-11-24 20:06:53',9);
/*!40000 ALTER TABLE `returned` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `returning`
--

DROP TABLE IF EXISTS `returning`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `returning` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `log_id` int DEFAULT NULL,
  `u_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Equipments_returning_log_id_8fbebf05_fk_log_id` (`log_id`),
  KEY `Equipments_returning_u_id_6f1db31a_fk_Accounts_user_id` (`u_id`),
  CONSTRAINT `Equipments_returning_log_id_8fbebf05_fk_log_id` FOREIGN KEY (`log_id`) REFERENCES `log` (`id`),
  CONSTRAINT `Equipments_returning_u_id_6f1db31a_fk_Accounts_user_id` FOREIGN KEY (`u_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `returning`
--

LOCK TABLES `returning` WRITE;
/*!40000 ALTER TABLE `returning` DISABLE KEYS */;
/*!40000 ALTER TABLE `returning` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-25 19:14:31
