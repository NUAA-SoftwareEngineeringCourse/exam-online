-- MySQL dump 10.13  Distrib 5.6.15, for Win64 (x86_64)
--
-- Host: localhost    Database: sinweb
-- ------------------------------------------------------
-- Server version	5.6.15

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
-- Table structure for table `exam_paper`
--

DROP TABLE IF EXISTS `exam_paper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exam_paper` (
  `paper_id` int(5) NOT NULL AUTO_INCREMENT,
  `paper_title` varchar(32) NOT NULL,
  `paper_desc` varchar(1024) NOT NULL,
  `paper_time` int(3) NOT NULL,
  `paper_date` datetime NOT NULL,
  `paper_open` tinyint(1) NOT NULL,
  `paper_path` varchar(256) NOT NULL,
  `paper_userid` varchar(16) NOT NULL,
  `paper_class` varchar(64) NOT NULL COMMENT '考试班级',
  PRIMARY KEY (`paper_id`),
  KEY `paper_user_id_constraint` (`paper_userid`),
  CONSTRAINT `paper_user_id_constraint` FOREIGN KEY (`paper_userid`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_paper`
--

LOCK TABLES `exam_paper` WRITE;
/*!40000 ALTER TABLE `exam_paper` DISABLE KEYS */;
INSERT INTO `exam_paper` VALUES (17,'操作系统','考察第一章到第十章，PPT涉及的内容，请同学们做好复习工作。',120,'2020-01-21 10:00:00',0,'E:\\Program Files\\PyCharm\\workspace\\exam-online\\FilesUpload\\ExamPapers\\T1616001-操作系统.xlsx','T1616001','1616302;'),(18,'计算机网络','考察所有讲过的内容，重点章节：第二、五、八章。',100,'2020-01-14 10:00:00',0,'E:\\Program Files\\PyCharm\\workspace\\exam-online\\FilesUpload\\ExamPapers\\T1616001-计算机网络.xlsx','T1616001','1616302;'),(19,'数据结构','考察第一章到第十章，PPT涉及的内容，请同学们做好复习工作。',150,'2020-01-26 19:00:00',0,'E:\\Program Files\\PyCharm\\workspace\\exam-online\\FilesUpload\\ExamPapers\\T1616001-数据结构.xlsx','T1616001','1616302;'),(24,'计算机组成原理','考察第一章到第十章，PPT涉及的内容，请同学们做好复习工作。',120,'2020-01-26 18:00:00',0,'E:\\Program Files\\PyCharm\\workspace\\exam-online\\FilesUpload\\ExamPapers\\T1616001-计算机组成原理.xlsx','T1616001','1616302;1616303;1616404;');
/*!40000 ALTER TABLE `exam_paper` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_exam_log`
--

DROP TABLE IF EXISTS `student_exam_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student_exam_log` (
  `paper_id` int(5) NOT NULL,
  `student_id` varchar(16) NOT NULL,
  `answer_json` varchar(2048) NOT NULL,
  `grade` int(3) NOT NULL COMMENT '单选题、多选题、判断题的总分',
  `full_grade` int(3) NOT NULL COMMENT '试卷满分',
  `subjective_grade` int(3) NOT NULL COMMENT '主观题分数',
  `submit_time` datetime NOT NULL COMMENT '提交时间',
  KEY `paper_id` (`paper_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `student_exam_log_ibfk_1` FOREIGN KEY (`paper_id`) REFERENCES `exam_paper` (`paper_id`),
  CONSTRAINT `student_exam_log_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_exam_log`
--

LOCK TABLES `student_exam_log` WRITE;
/*!40000 ALTER TABLE `student_exam_log` DISABLE KEYS */;
INSERT INTO `student_exam_log` VALUES (17,'161630230','{\"0\":\"A\",\"1\":\"A\",\"2\":\"A\",\"3\":\"A\",\"4\":\"A\",\"5\":\"A\",\"6\":\"A\",\"7\":\"A\",\"8\":\"A\",\"9\":\"A\",\"10\":\"ABC\",\"11\":\"BCD\",\"12\":\"ABC\",\"13\":\"A\",\"14\":\"1\",\"15\":\"0\",\"16\":\"1\",\"17\":\"1\",\"18\":\"1\",\"19\":\"计算机的启动步骤，瞎写的回答。\",\"20\":\"系统调用过程，瞎写的回答。\"}',73,100,15,'2019-12-12 19:02:31'),(18,'161630230','{\"0\":\"A\",\"1\":\"A\",\"2\":\"A\",\"3\":\"A\",\"4\":\"A\",\"5\":\"A\",\"6\":\"A\",\"7\":\"A\",\"8\":\"A\",\"9\":\"A\",\"10\":\"ABC\",\"11\":\"BCD\",\"12\":\"ABC\",\"13\":\"CD\",\"14\":\"1\",\"15\":\"1\",\"16\":\"1\",\"17\":\"1\",\"18\":\"1\",\"19\":\"瞎写拥塞控制算法。\",\"20\":\"瞎写TCO/UDP。\"}',75,100,8,'2019-12-12 19:08:30'),(19,'161630230','{\"0\":\"A\",\"1\":\"A\",\"2\":\"A\",\"3\":\"A\",\"4\":\"A\",\"5\":\"A\",\"6\":\"A\",\"7\":\"A\",\"8\":\"A\",\"9\":\"A\",\"10\":\"ABC\",\"11\":\"BCD\",\"12\":\"ABC\",\"13\":\"BCD\",\"14\":\"1\",\"15\":\"1\",\"16\":\"1\",\"17\":\"1\",\"18\":\"1\",\"19\":\"瞎写最短路径。\",\"20\":\"瞎写堆排序。\"}',80,100,17,'2019-12-12 19:10:00'),(24,'161630203','{\"0\":\"C\",\"1\":\"C\",\"2\":\"C\",\"3\":\"C\",\"4\":\"C\",\"5\":\"C\",\"6\":\"A\",\"7\":\"A\",\"8\":\"A\",\"9\":\"A\",\"10\":\"ABC\",\"11\":\"BCD\",\"12\":\"ABC\",\"13\":\"BCD\",\"14\":\"1\",\"15\":\"1\",\"16\":\"1\",\"17\":\"1\",\"18\":\"1\",\"19\":\"RAM相比ROM，蒲银回答。\",\"20\":\"中断控制方式相比DMA控制方式，蒲银回答。\"}',65,100,15,'2019-12-15 20:12:40');
/*!40000 ALTER TABLE `student_exam_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher_student`
--

DROP TABLE IF EXISTS `teacher_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacher_student` (
  `teacher_id` varchar(16) NOT NULL,
  `student_id` varchar(16) NOT NULL,
  `paper_id` int(5) NOT NULL,
  KEY `teacher_id` (`teacher_id`),
  KEY `student_id` (`student_id`),
  KEY `paper_id` (`paper_id`),
  CONSTRAINT `teacher_student_ibfk_3` FOREIGN KEY (`paper_id`) REFERENCES `exam_paper` (`paper_id`),
  CONSTRAINT `teacher_student_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `teacher_student_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_student`
--

LOCK TABLES `teacher_student` WRITE;
/*!40000 ALTER TABLE `teacher_student` DISABLE KEYS */;
INSERT INTO `teacher_student` VALUES ('T1616001','161630230',17),('T1616001','161630230',18),('T1616001','161630230',19),('T1616001','161630229',17),('T1616001','161630231',17),('T1616001','161630231',18),('T1616001','161630201',24),('T1616001','161630202',24),('T1616001','161630203',24),('T1616001','161630204',24),('T1616001','161630205',24),('T1616001','161630206',24),('T1616001','161630229',24),('T1616001','161630230',24),('T1616001','161630231',24),('T1616001','161630301',24),('T1616001','161640404',24);
/*!40000 ALTER TABLE `teacher_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` varchar(16) NOT NULL,
  `user_name` varchar(16) NOT NULL,
  `user_email` varchar(64) NOT NULL,
  `user_password` varchar(32) NOT NULL,
  `user_create_time` datetime NOT NULL,
  `user_update_time` datetime NOT NULL,
  `user_type` varchar(8) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('161630201','崔云峰','cui@yahoo.com','161630201','2019-11-30 21:14:27','2019-11-30 21:14:33','STUDENT'),('161630202','孙笑川','sun@dog.com','161630202','2019-11-30 21:16:34','2019-11-29 21:16:37','STUDENT'),('161630203','蒲银','py@sjtu.com','161630203','2019-11-28 21:15:34','2019-11-29 21:15:37','STUDENT'),('161630204','李赣','li@dog.com','161630204','2019-11-23 21:19:30','2019-11-29 21:19:33','STUDENT'),('161630205','泰隆','loong@qq.com','161630205','2019-11-04 21:20:18','2019-11-28 21:20:21','STUDENT'),('161630206','小呆呆','evil@man.com','161630206','2019-09-18 21:21:33','2019-11-28 21:21:36','STUDENT'),('161630229','王珊月','wang@qq.com','161630229','2019-11-09 19:36:16','2019-11-09 19:36:16','STUDENT'),('161630230','冼健邦','sin@qq.com','161630230','2019-11-09 19:24:00','2019-11-09 19:24:00','STUDENT'),('161630231','梁家娟','ljj@nuaa.com','161630231','2019-11-10 20:02:32','2019-11-10 20:02:32','STUDENT'),('161630301','大师兄','big@qq.com','161630301','2019-12-04 19:43:14','2019-12-07 19:43:19','STUDENT'),('161640404','高笑','gao@qq.com','161640404','2019-12-06 22:41:19','2019-12-06 22:41:19','STUDENT'),('Admin','管理员','admin@qq.com','Admin','2019-11-16 21:31:50','2019-11-16 21:31:50','ADMIN'),('T1616001','王力','jh@nuaa.com','T1616001','2019-11-10 20:41:51','2019-11-10 20:41:51','TEACHER'),('T1616002','张学友','zhang@qq.com','T1616002','2019-12-04 20:11:17','2019-12-04 20:11:17','TEACHER'),('T1616003','葛优','ge@qq.com','T1616003','2019-12-06 22:37:09','2019-12-06 22:37:09','TEACHER');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-15 20:17:50
