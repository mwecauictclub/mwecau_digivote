/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.2-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: election_sys
-- ------------------------------------------------------
-- Server version	11.8.2-MariaDB-1 from Debian

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add content type',4,'add_contenttype'),
(14,'Can change content type',4,'change_contenttype'),
(15,'Can delete content type',4,'delete_contenttype'),
(16,'Can view content type',4,'view_contenttype'),
(17,'Can add session',5,'add_session'),
(18,'Can change session',5,'change_session'),
(19,'Can delete session',5,'delete_session'),
(20,'Can view session',5,'view_session'),
(21,'Can add course',6,'add_course'),
(22,'Can change course',6,'change_course'),
(23,'Can delete course',6,'delete_course'),
(24,'Can view course',6,'view_course'),
(25,'Can add state',7,'add_state'),
(26,'Can change state',7,'change_state'),
(27,'Can delete state',7,'delete_state'),
(28,'Can view state',7,'view_state'),
(29,'Can add user',8,'add_user'),
(30,'Can change user',8,'change_user'),
(31,'Can delete user',8,'delete_user'),
(32,'Can view user',8,'view_user'),
(33,'Can add College Data',9,'add_collegedata'),
(34,'Can change College Data',9,'change_collegedata'),
(35,'Can delete College Data',9,'delete_collegedata'),
(36,'Can view College Data',9,'view_collegedata'),
(37,'Can add election',10,'add_election'),
(38,'Can change election',10,'change_election'),
(39,'Can delete election',10,'delete_election'),
(40,'Can view election',10,'view_election'),
(41,'Can add election level',11,'add_electionlevel'),
(42,'Can change election level',11,'change_electionlevel'),
(43,'Can delete election level',11,'delete_electionlevel'),
(44,'Can view election level',11,'view_electionlevel'),
(45,'Can add position',12,'add_position'),
(46,'Can change position',12,'change_position'),
(47,'Can delete position',12,'delete_position'),
(48,'Can view position',12,'view_position'),
(49,'Can add candidate',13,'add_candidate'),
(50,'Can change candidate',13,'change_candidate'),
(51,'Can delete candidate',13,'delete_candidate'),
(52,'Can view candidate',13,'view_candidate'),
(53,'Can add voter token',14,'add_votertoken'),
(54,'Can change voter token',14,'change_votertoken'),
(55,'Can delete voter token',14,'delete_votertoken'),
(56,'Can view voter token',14,'view_votertoken'),
(57,'Can add vote',15,'add_vote'),
(58,'Can change vote',15,'change_vote'),
(59,'Can delete vote',15,'delete_vote'),
(60,'Can view vote',15,'view_vote'),
(61,'Can add Blacklisted Token',16,'add_blacklistedtoken'),
(62,'Can change Blacklisted Token',16,'change_blacklistedtoken'),
(63,'Can delete Blacklisted Token',16,'delete_blacklistedtoken'),
(64,'Can view Blacklisted Token',16,'view_blacklistedtoken'),
(65,'Can add Outstanding Token',17,'add_outstandingtoken'),
(66,'Can change Outstanding Token',17,'change_outstandingtoken'),
(67,'Can delete Outstanding Token',17,'delete_outstandingtoken'),
(68,'Can view Outstanding Token',17,'view_outstandingtoken');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `college_data`
--

DROP TABLE IF EXISTS `college_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `college_data` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `registration_number` varchar(20) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(254) NOT NULL,
  `voter_id` varchar(36) DEFAULT NULL,
  `is_used` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `uploaded_by_id` bigint(20) NOT NULL,
  `course_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `registration_number` (`registration_number`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `voter_id` (`voter_id`),
  KEY `college_data_uploaded_by_id_51056561_fk_users_id` (`uploaded_by_id`),
  KEY `college_dat_registr_86e753_idx` (`registration_number`),
  KEY `college_dat_course__1baf12_idx` (`course_id`,`is_used`),
  KEY `college_dat_status_24a8f1_idx` (`status`),
  KEY `college_dat_voter_i_fbb903_idx` (`voter_id`),
  CONSTRAINT `college_data_course_id_4ebcfa59_fk_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `college_data_uploaded_by_id_51056561_fk_users_id` FOREIGN KEY (`uploaded_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `college_data`
--

LOCK TABLES `college_data` WRITE;
/*!40000 ALTER TABLE `college_data` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `college_data` VALUES
(1,'T/DEG/2000/0001','Cleven','Godson','cleven@mail.com',NULL,0,'2025-08-25 16:03:10.172225','pending',2,1),
(2,'T/DEG/2020/0003','Neema','John','neema@mail.com',NULL,0,'2025-08-25 21:29:37.533163','pending',4,2),
(3,'T/DEG/1/1','Klevin','Omari','kev@me.com',NULL,0,'2025-08-26 09:00:38.497572','pending',4,2);
/*!40000 ALTER TABLE `college_data` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `courses_code_fa42f1_idx` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `courses` VALUES
(1,'Computer Science','CS101','2025-08-25 16:02:37.892219','2025-08-25 20:52:36.234196'),
(2,'Computer Science','CS100','2025-08-25 21:28:15.005369','2025-08-25 21:28:15.005417');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_admin_log` VALUES
(1,'2025-08-26 08:59:49.036848','4','T/ADMIN/2020/0002 (T/ADMIN/2020/0002)',2,'[{\"changed\": {\"fields\": [\"Last login\", \"Gender\", \"State\", \"Course\", \"Role\", \"Is verified\", \"Date verified\"]}}]',8,1),
(2,'2025-08-26 09:00:38.498343','3','Klevin Omari (T/DEG/1/1)',1,'[{\"added\": {}}]',9,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_content_type` VALUES
(1,'admin','logentry'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'contenttypes','contenttype'),
(9,'core','collegedata'),
(6,'core','course'),
(7,'core','state'),
(8,'core','user'),
(13,'election','candidate'),
(10,'election','election'),
(11,'election','electionlevel'),
(12,'election','position'),
(15,'election','vote'),
(14,'election','votertoken'),
(5,'sessions','session'),
(16,'token_blacklist','blacklistedtoken'),
(17,'token_blacklist','outstandingtoken');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2025-08-25 08:54:03.417587'),
(2,'contenttypes','0002_remove_content_type_name','2025-08-25 08:54:04.193071'),
(3,'auth','0001_initial','2025-08-25 08:54:07.571135'),
(4,'auth','0002_alter_permission_name_max_length','2025-08-25 08:54:08.419723'),
(5,'auth','0003_alter_user_email_max_length','2025-08-25 08:54:08.452486'),
(6,'auth','0004_alter_user_username_opts','2025-08-25 08:54:08.471563'),
(7,'auth','0005_alter_user_last_login_null','2025-08-25 08:54:08.484236'),
(8,'auth','0006_require_contenttypes_0002','2025-08-25 08:54:08.487338'),
(9,'auth','0007_alter_validators_add_error_messages','2025-08-25 08:54:08.509256'),
(10,'auth','0008_alter_user_username_max_length','2025-08-25 08:54:08.529203'),
(11,'auth','0009_alter_user_last_name_max_length','2025-08-25 08:54:08.550384'),
(12,'auth','0010_alter_group_name_max_length','2025-08-25 08:54:09.315658'),
(13,'auth','0011_update_proxy_permissions','2025-08-25 08:54:09.340598'),
(14,'auth','0012_alter_user_first_name_max_length','2025-08-25 08:54:09.395240'),
(15,'core','0001_initial','2025-08-25 08:54:24.576606'),
(16,'admin','0001_initial','2025-08-25 08:54:26.061523'),
(17,'admin','0002_logentry_remove_auto_add','2025-08-25 08:54:26.100457'),
(18,'admin','0003_logentry_add_action_flag_choices','2025-08-25 08:54:26.161560'),
(19,'core','0002_alter_user_registration_number','2025-08-25 08:54:26.193350'),
(20,'election','0001_initial','2025-08-25 08:54:40.396435'),
(21,'election','0002_vote_election_vo_token_i_2ae447_idx_and_more','2025-08-25 08:54:41.907865'),
(22,'sessions','0001_initial','2025-08-25 08:54:42.552121'),
(23,'token_blacklist','0001_initial','2025-08-25 08:54:44.407489'),
(24,'token_blacklist','0002_outstandingtoken_jti_hex','2025-08-25 08:54:44.907742'),
(25,'token_blacklist','0003_auto_20171017_2007','2025-08-25 08:54:44.981155'),
(26,'token_blacklist','0004_auto_20171017_2013','2025-08-25 08:54:46.341041'),
(27,'token_blacklist','0005_remove_outstandingtoken_jti','2025-08-25 08:54:46.874138'),
(28,'token_blacklist','0006_auto_20171017_2113','2025-08-25 08:54:47.509692'),
(29,'token_blacklist','0007_auto_20171017_2214','2025-08-25 08:54:50.108366'),
(30,'token_blacklist','0008_migrate_to_bigautofield','2025-08-25 08:54:52.874785'),
(31,'token_blacklist','0010_fix_migrate_to_bigautofield','2025-08-25 08:54:52.931255'),
(32,'token_blacklist','0011_linearizes_history','2025-08-25 08:54:53.068540'),
(33,'token_blacklist','0012_alter_outstandingtoken_user','2025-08-25 08:54:53.101821'),
(34,'token_blacklist','0013_alter_blacklistedtoken_options_and_more','2025-08-25 08:54:53.158405'),
(35,'core','0003_rename_course_code_83d7d9_idx_courses_code_fa42f1_idx_and_more','2025-08-26 12:13:06.801470');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_session` VALUES
('76aiyn8m2r6m3kssvdv68utyni5zdcpa','.eJxVjEEOwiAQRe_C2pCBoYAu3fcMZGBGqZo2Ke3KeHdD0oVu_3vvv1Wifatpb7KmidVFGXX63TKVp8wd8IPm-6LLMm_rlHVX9EGbHheW1_Vw_w4qtdrraDgMEINH49FhyQXQ0yDIbEqIxSGBBCaH1lkbWW4CPho4ZwYgVJ8vyXQ3WA:1uqpUX:lR9Wg7Rm2ixJ5WI9OGge1nEldijLv2aIzt-kiNZ2SkA','2025-09-09 08:57:21.392940');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `election_candidate`
--

DROP TABLE IF EXISTS `election_candidate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `election_candidate` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `bio` longtext NOT NULL,
  `platform` longtext NOT NULL,
  `vote_count` int(10) unsigned NOT NULL CHECK (`vote_count` >= 0),
  `user_id` bigint(20) NOT NULL,
  `election_id` bigint(20) NOT NULL,
  `position_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `election_candidate_user_id_election_id_position_id_c8d4aa35_uniq` (`user_id`,`election_id`,`position_id`),
  KEY `election_ca_electio_1af40c_idx` (`election_id`,`position_id`),
  KEY `election_candidate_position_id_95e70f2a_fk_election_position_id` (`position_id`),
  CONSTRAINT `election_candidate_election_id_37fd6b2d_fk_election_election_id` FOREIGN KEY (`election_id`) REFERENCES `election_election` (`id`),
  CONSTRAINT `election_candidate_position_id_95e70f2a_fk_election_position_id` FOREIGN KEY (`position_id`) REFERENCES `election_position` (`id`),
  CONSTRAINT `election_candidate_user_id_74b82485_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `election_candidate`
--

LOCK TABLES `election_candidate` WRITE;
/*!40000 ALTER TABLE `election_candidate` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `election_candidate` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `election_election`
--

DROP TABLE IF EXISTS `election_election`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `election_election` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `has_ended` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `election_el_is_acti_17f51b_idx` (`is_active`,`start_date`,`end_date`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `election_election`
--

LOCK TABLES `election_election` WRITE;
/*!40000 ALTER TABLE `election_election` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `election_election` VALUES
(1,'Student Election 2025','','2025-07-31 21:00:00.000000','2025-08-29 21:00:00.000000',1,0,'2025-08-25 21:30:55.068966','2025-08-25 21:30:55.069006');
/*!40000 ALTER TABLE `election_election` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `election_electionlevel`
--

DROP TABLE IF EXISTS `election_electionlevel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `election_electionlevel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `code` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `election_el_code_ed5cf2_idx` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `election_electionlevel`
--

LOCK TABLES `election_electionlevel` WRITE;
/*!40000 ALTER TABLE `election_electionlevel` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `election_electionlevel` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `election_position`
--

DROP TABLE IF EXISTS `election_position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `election_position` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `gender_restriction` varchar(10) NOT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `election_level_id` bigint(20) NOT NULL,
  `state_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `election_position_election_level_id_title__9023cd77_uniq` (`election_level_id`,`title`,`gender_restriction`,`state_id`,`course_id`),
  KEY `election_po_electio_4b8711_idx` (`election_level_id`,`state_id`,`course_id`),
  KEY `election_position_course_id_08e04d99_fk_course_id` (`course_id`),
  KEY `election_position_state_id_b32b8dfe_fk_state_majimbo_id` (`state_id`),
  CONSTRAINT `election_position_course_id_08e04d99_fk_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `election_position_election_level_id_2c923c7a_fk_election_` FOREIGN KEY (`election_level_id`) REFERENCES `election_electionlevel` (`id`),
  CONSTRAINT `election_position_state_id_b32b8dfe_fk_state_majimbo_id` FOREIGN KEY (`state_id`) REFERENCES `states` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `election_position`
--

LOCK TABLES `election_position` WRITE;
/*!40000 ALTER TABLE `election_position` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `election_position` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `election_vote`
--

DROP TABLE IF EXISTS `election_vote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `election_vote` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime(6) NOT NULL,
  `candidate_id` bigint(20) NOT NULL,
  `election_id` bigint(20) NOT NULL,
  `token_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `election_vote_token_id_election_id_e51434c7_uniq` (`token_id`,`election_id`),
  KEY `election_vo_token_i_2ae447_idx` (`token_id`,`candidate_id`),
  KEY `election_vo_candida_803f21_idx` (`candidate_id`,`timestamp`),
  KEY `election_vo_electio_f3c178_idx` (`election_id`),
  CONSTRAINT `election_vote_candidate_id_3b8efe02_fk_election_candidate_id` FOREIGN KEY (`candidate_id`) REFERENCES `election_candidate` (`id`),
  CONSTRAINT `election_vote_election_id_d9c733f8_fk_election_election_id` FOREIGN KEY (`election_id`) REFERENCES `election_election` (`id`),
  CONSTRAINT `election_vote_token_id_7a979f4c_fk_election_votertoken_id` FOREIGN KEY (`token_id`) REFERENCES `election_votertoken` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `election_vote`
--

LOCK TABLES `election_vote` WRITE;
/*!40000 ALTER TABLE `election_vote` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `election_vote` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `election_votertoken`
--

DROP TABLE IF EXISTS `election_votertoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `election_votertoken` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `token` uuid NOT NULL,
  `is_used` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `used_at` datetime(6) DEFAULT NULL,
  `election_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  UNIQUE KEY `election_votertoken_user_id_election_id_7ff7158f_uniq` (`user_id`,`election_id`),
  KEY `election_vo_token_7bf182_idx` (`token`),
  KEY `election_vo_electio_7196fb_idx` (`election_id`,`is_used`),
  CONSTRAINT `election_votertoken_election_id_32f1aaa5_fk_election_election_id` FOREIGN KEY (`election_id`) REFERENCES `election_election` (`id`),
  CONSTRAINT `election_votertoken_user_id_8f8e2364_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `election_votertoken`
--

LOCK TABLES `election_votertoken` WRITE;
/*!40000 ALTER TABLE `election_votertoken` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `election_votertoken` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `states`
--

DROP TABLE IF EXISTS `states`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `states` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `states_name_9db832_idx` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `states`
--

LOCK TABLES `states` WRITE;
/*!40000 ALTER TABLE `states` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `states` VALUES
(1,'Change State','2025-08-25 16:02:00.787669','2025-08-25 16:02:00.787715'),
(2,'Kifumbu','2025-08-25 21:28:03.236486','2025-08-25 21:28:03.236533');
/*!40000 ALTER TABLE `states` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

DROP TABLE IF EXISTS `token_blacklist_blacklistedtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_blacklistedtoken`
--

LOCK TABLES `token_blacklist_blacklistedtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

DROP TABLE IF EXISTS `token_blacklist_outstandingtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `jti` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outstandingtoken_user_id_83bc629a_fk_users_id` (`user_id`),
  CONSTRAINT `token_blacklist_outstandingtoken_user_id_83bc629a_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

LOCK TABLES `token_blacklist_outstandingtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `registration_number` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `voter_id` varchar(36) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `date_verified` datetime(6) DEFAULT NULL,
  `last_login_ip` char(39) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `state_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `registration_number` (`registration_number`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `voter_id` (`voter_id`),
  KEY `users_registr_4b432d_idx` (`registration_number`),
  KEY `users_role_a93a92_idx` (`role`,`is_verified`),
  KEY `users_state_i_e49108_idx` (`state_id`,`course_id`),
  KEY `users_email_4b85f2_idx` (`email`),
  KEY `users_gender_c12881_idx` (`gender`),
  KEY `users_voter_i_c1d34a_idx` (`voter_id`),
  KEY `users_course_id_ef7a18fa_fk_course_id` (`course_id`),
  CONSTRAINT `users_course_id_ef7a18fa_fk_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `users_state_id_0521d641_fk_state_majimbo_id` FOREIGN KEY (`state_id`) REFERENCES `states` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `users` VALUES
(1,'pbkdf2_sha256$1000000$DrkdKwkwfPzpZui5QkyCnw$vhgSiwiO3kirocdueIzdzBtv+2T1jPfGcIi0z49X/cc=','2025-08-26 08:57:21.364533',1,'','',1,1,'2025-08-25 13:28:00.198674','T/DEG/100/1','admin@me.com',NULL,NULL,'voter',0,NULL,NULL,NULL,NULL),
(2,'pbkdf2_sha256$1000000$mNOWax0YiB4akeIxWele2H$4MFZMTyuaVLCjGROJePPZqC35T9fT0zhKQH7p5pxVc0=',NULL,1,'','',1,1,'2025-08-25 16:01:59.812138','T/ADMIN/2020/001','admin@example.com',NULL,NULL,'voter',0,NULL,NULL,NULL,NULL),
(4,'pbkdf2_sha256$1000000$DDGIrEPljhjCBpBl6fXkFJ$axOul85CnIcPu/mQ2dE82SUmKGAZyOVvvaF5CIoPsOg=','2025-08-26 08:59:19.000000',1,'','',1,1,'2025-08-25 21:27:48.000000','T/ADMIN/2020/0002','admin@mail.com',NULL,'male','commissioner',1,'2025-08-26 08:59:43.000000',NULL,2,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users_groups`
--

DROP TABLE IF EXISTS `users_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_groups_user_id_group_id_fc7788e8_uniq` (`user_id`,`group_id`),
  KEY `users_groups_group_id_2f3517aa_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_groups_user_id_f500bee5_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_groups`
--

LOCK TABLES `users_groups` WRITE;
/*!40000 ALTER TABLE `users_groups` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `users_groups` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `users_user_permissions`
--

DROP TABLE IF EXISTS `users_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_permissions_user_id_permission_id_3b86cbdf_uniq` (`user_id`,`permission_id`),
  KEY `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_permissions_user_id_92473840_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_permissions`
--

LOCK TABLES `users_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `users_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-08-26  8:13:25
