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
-- Table structure for table `choice_question`
--

DROP TABLE IF EXISTS `choice_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `choice_question` (
  `q_id` int(11) NOT NULL AUTO_INCREMENT,
  `q_description` varchar(512) NOT NULL,
  `q_value` int(3) NOT NULL,
  `q_answer` varchar(4) NOT NULL,
  `q_A` varchar(255) NOT NULL,
  `q_B` varchar(255) NOT NULL,
  `q_C` varchar(255) NOT NULL,
  `q_D` varchar(255) NOT NULL,
  `q_paperid` int(11) NOT NULL,
  PRIMARY KEY (`q_id`),
  KEY `q_paperid` (`q_paperid`),
  CONSTRAINT `choice_question_ibfk_1` FOREIGN KEY (`q_paperid`) REFERENCES `exam_paper` (`paper_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `choice_question`
--

LOCK TABLES `choice_question` WRITE;
/*!40000 ALTER TABLE `choice_question` DISABLE KEYS */;
INSERT INTO `choice_question` VALUES (1,'关于网桥的描述中，正确的是 （）',5,'A','网桥是在数据链路层实现网络互联的设备','网桥无法实现地址过滤与帧转发功能','网桥互联的网络在网络层都采用不同协议','透明网桥由源结点实现帧的路由选择功能',30),(2,'对于基带 CSMA/CD 而言，为了确保发送站点在传输时能检测到可能存在的冲突，数据帧的传输时延至少要等于信号传播时延的 (   )。',5,'A','2倍','1倍','4倍','2.5倍',30),(3,'What the message in NetworkLayer is called? ( )',5,'A','datagram','algorithms','segment','message',30),(4,'下列关于交换机的叙述中，正确的是 （） 。',5,'A','以太网交换机本质上是一种多端口网桥','通过交换机互连的一组工作站构成一个冲突域','交换机每个端口所连网络构成一个独立的广播域','以太网交换机可实现采用不同网络层协议的网络互联',30),(5,'双绞线传输介质是把两根导线绞在一起，这样可以减少（）。',5,'A','信号之间的相互串扰','外界信号的干扰','信号向外泄露','信号传输时的衰减',30),(6,'一A类网络的子网号subnet-id分别为16个1，那么他的子网掩码是多少？（ ）',5,'A','255.255.255.0','255.255.248.255','255.255.248.0','255.255.255.248',30),(7,'关于因特网中路由器和广域网中结点交换机叙述错误的是（）',5,'A','路由器和结点交换机都使用统一的IP协议。','路由器专门用来转发分组，结点交换机还可以连接上许多主机。','路由器用来互连不同的网络，结点交换机只是在一个特定的网络中工作。','路由器根据目的网络地址找出下一跳（即下一个路由器），而结点交换机则根据目的站所接入的交换机号找出下一跳（即下一个结点交换机）。',30),(8,'发送窗口大小是多少？（ ）',5,'A','不超过2^n-1','不超过2^n','2^n','2^n-1',30),(9,'采用海明码纠正一位差错，若信息位为 4 位，则冗余位至少应为 (   )',5,'A','3位','2位','5位','4位',30),(10,'下列（   ）设备或者软件属于核心系统',5,'A','路由器','Web服务器','联网的智能手机','个人笔记本',30),(11,'我是多项选择题1',5,'ABC','Option-A','Option-B','Option-C','Option-D',30),(12,'我是多项选择题2',5,'BCD','Option-A','Option-B','Option-C','Option-D',30),(13,'我是多项选择题3',5,'ABC','Option-A','Option-B','Option-C','Option-D',30),(14,'我是多项选择题4',5,'BCD','Option-A','Option-B','Option-C','Option-D',30);
/*!40000 ALTER TABLE `choice_question` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_paper`
--

LOCK TABLES `exam_paper` WRITE;
/*!40000 ALTER TABLE `exam_paper` DISABLE KEYS */;
INSERT INTO `exam_paper` VALUES (17,'操作系统','考察第一章到第十章，PPT涉及的内容，请同学们做好复习工作。',120,'2020-01-21 10:00:00',0,'E:\\Program Files\\PyCharm\\workspace\\exam-online\\FilesUpload\\ExamPapers\\T1616001-操作系统.xlsx','T1616001','1616302;'),(18,'计算机网络','考察所有讲过的内容，重点章节：第二、五、八章。',100,'2020-01-14 10:00:00',0,'E:\\Program Files\\PyCharm\\workspace\\exam-online\\FilesUpload\\ExamPapers\\T1616001-计算机网络.xlsx','T1616001','1616302;'),(19,'数据结构','考察第一章到第十章，PPT涉及的内容，请同学们做好复习工作。',150,'2020-01-26 19:00:00',0,'E:\\Program Files\\PyCharm\\workspace\\exam-online\\FilesUpload\\ExamPapers\\T1616001-数据结构.xlsx','T1616001','1616302;'),(24,'计算机组成原理','考察第一章到第十章，PPT涉及的内容，请同学们做好复习工作。',120,'2020-01-26 18:00:00',0,'E:\\Program Files\\PyCharm\\workspace\\exam-online\\FilesUpload\\ExamPapers\\T1616001-计算机组成原理.xlsx','T1616001','1616302;1616303;1616404;'),(25,'计算机组成原理（2）','考察所有讲过的内容，重点章节：第二、五、八章。',120,'2019-12-21 13:25:00',0,'E:\\Program Files\\PyCharm\\workspace\\exam-online\\FilesUpload\\ExamPapers\\T1616001-计算机组成原理（2）.xlsx','T1616001','1616302;1616303;1616404;'),(26,'计算机组成原理(3)','考察第一章到第十章，PPT涉及的内容，请同学们做好复习工作。',120,'2019-12-21 14:10:00',0,'E:\\Program Files\\PyCharm\\workspace\\exam-online\\FilesUpload\\ExamPapers\\T1616001-计算机组成原理(3).xlsx','T1616001','1616302;1616303;1616404;'),(30,'计算机网络(Network)','考察第一章到第十章，PPT涉及的内容，请同学们做好复习工作。',150,'2020-01-30 11:00:00',0,'E:\\Program Files\\PyCharm\\workspace\\exam-online\\FilesUpload\\ExamPapers\\T1616002-计算机网络(Network).xlsx','T1616002','1616302;');
/*!40000 ALTER TABLE `exam_paper` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `judge_question`
--

DROP TABLE IF EXISTS `judge_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `judge_question` (
  `q_id` int(11) NOT NULL AUTO_INCREMENT,
  `q_description` varchar(512) NOT NULL,
  `q_value` int(3) NOT NULL,
  `q_answer` int(1) NOT NULL,
  `q_paperid` int(11) NOT NULL,
  PRIMARY KEY (`q_id`),
  KEY `q_paperid` (`q_paperid`),
  CONSTRAINT `judge_question_ibfk_1` FOREIGN KEY (`q_paperid`) REFERENCES `exam_paper` (`paper_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `judge_question`
--

LOCK TABLES `judge_question` WRITE;
/*!40000 ALTER TABLE `judge_question` DISABLE KEYS */;
INSERT INTO `judge_question` VALUES (11,'判断题1',2,1,30),(12,'判断题2',2,1,30),(13,'判断题3',2,1,30),(14,'判断题4',2,1,30),(15,'判断题5',2,1,30);
/*!40000 ALTER TABLE `judge_question` ENABLE KEYS */;
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
INSERT INTO `student_exam_log` VALUES (17,'161630230','{\"0\":\"A\",\"1\":\"A\",\"2\":\"A\",\"3\":\"A\",\"4\":\"A\",\"5\":\"A\",\"6\":\"A\",\"7\":\"A\",\"8\":\"A\",\"9\":\"A\",\"10\":\"ABC\",\"11\":\"BCD\",\"12\":\"ABC\",\"13\":\"A\",\"14\":\"1\",\"15\":\"0\",\"16\":\"1\",\"17\":\"1\",\"18\":\"1\",\"19\":\"计算机的启动步骤，瞎写的回答。\",\"20\":\"系统调用过程，瞎写的回答。\"}',73,100,15,'2019-12-12 19:02:31'),(18,'161630230','{\"0\":\"A\",\"1\":\"A\",\"2\":\"A\",\"3\":\"A\",\"4\":\"A\",\"5\":\"A\",\"6\":\"A\",\"7\":\"A\",\"8\":\"A\",\"9\":\"A\",\"10\":\"ABC\",\"11\":\"BCD\",\"12\":\"ABC\",\"13\":\"CD\",\"14\":\"1\",\"15\":\"1\",\"16\":\"1\",\"17\":\"1\",\"18\":\"1\",\"19\":\"瞎写拥塞控制算法。\",\"20\":\"瞎写TCO/UDP。\"}',75,100,8,'2019-12-12 19:08:30'),(19,'161630230','{\"0\":\"A\",\"1\":\"A\",\"2\":\"A\",\"3\":\"A\",\"4\":\"A\",\"5\":\"A\",\"6\":\"A\",\"7\":\"A\",\"8\":\"A\",\"9\":\"A\",\"10\":\"ABC\",\"11\":\"BCD\",\"12\":\"ABC\",\"13\":\"BCD\",\"14\":\"1\",\"15\":\"1\",\"16\":\"1\",\"17\":\"1\",\"18\":\"1\",\"19\":\"瞎写最短路径。\",\"20\":\"瞎写堆排序。\"}',80,100,17,'2019-12-12 19:10:00'),(24,'161630203','{\"0\":\"C\",\"1\":\"C\",\"2\":\"C\",\"3\":\"C\",\"4\":\"C\",\"5\":\"C\",\"6\":\"A\",\"7\":\"A\",\"8\":\"A\",\"9\":\"A\",\"10\":\"ABC\",\"11\":\"BCD\",\"12\":\"ABC\",\"13\":\"BCD\",\"14\":\"1\",\"15\":\"1\",\"16\":\"1\",\"17\":\"1\",\"18\":\"1\",\"19\":\"RAM相比ROM，蒲银回答。\",\"20\":\"中断控制方式相比DMA控制方式，蒲银回答。\"}',65,100,15,'2019-12-15 20:12:40'),(25,'161630230','{\"0\":\"A\",\"1\":\"A\",\"2\":\"A\",\"3\":\"A\",\"4\":\"A\",\"5\":\"A\",\"6\":\"A\",\"7\":\"A\",\"8\":\"A\",\"9\":\"A\",\"10\":\"ABC\",\"11\":\"BCD\",\"12\":\"ABC\",\"13\":\"BCD\",\"14\":\"1\",\"15\":\"1\",\"16\":\"1\",\"17\":\"1\",\"18\":\"1\",\"19\":\"冼健邦RAM/ROM。\",\"20\":\"冼健邦DMA。\"}',50,100,16,'2019-12-21 13:28:28'),(25,'161630201','{\"0\":\"A\",\"1\":\"C\",\"2\":\"A\",\"3\":\"C\",\"4\":\"A\",\"5\":\"C\",\"6\":\"D\",\"7\":\"A\",\"8\":\"A\",\"9\":\"A\",\"10\":\"ABC\",\"11\":\"BCD\",\"12\":\"A\",\"13\":\"BCD\",\"14\":\"1\",\"15\":\"1\",\"16\":\"1\",\"17\":\"1\",\"18\":\"1\",\"19\":\"崔云峰RAM/ROM。\",\"20\":\"崔云峰DMA。\"}',50,100,20,'2019-12-21 13:31:05'),(25,'161630202','{\"0\":\"C\",\"1\":\"C\",\"2\":\"C\",\"3\":\"C\",\"4\":\"B\",\"5\":\"A\",\"6\":\"C\",\"7\":\"A\",\"8\":\"A\",\"9\":\"A\",\"10\":\"ABC\",\"11\":\"BCD\",\"12\":\"ABC\",\"13\":\"BCD\",\"14\":\"1\",\"15\":\"1\",\"16\":\"1\",\"17\":\"1\",\"18\":\"1\",\"19\":\"孙笑川RAM/ROM。\",\"20\":\"孙笑川DMA。\"}',80,100,16,'2019-12-21 13:36:22'),(25,'161630203','{\"0\":\"D\",\"1\":\"D\",\"2\":\"D\",\"3\":\"D\",\"4\":\"A\",\"5\":\"A\",\"6\":\"C\",\"7\":\"B\",\"8\":\"A\",\"9\":\"B\",\"10\":\"ABC\",\"11\":\"ABC\",\"12\":\"ABC\",\"13\":\"ABC\",\"14\":\"0\",\"15\":\"1\",\"16\":\"0\",\"17\":\"1\",\"18\":\"1\",\"19\":\"蒲银RAM/ROM.\",\"20\":\"蒲银DMA.\"}',31,100,12,'2019-12-21 13:40:21');
/*!40000 ALTER TABLE `student_exam_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subjective_question`
--

DROP TABLE IF EXISTS `subjective_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subjective_question` (
  `q_id` int(11) NOT NULL AUTO_INCREMENT,
  `q_description` varchar(512) NOT NULL,
  `q_answer` varchar(512) NOT NULL,
  `q_value` int(3) NOT NULL,
  `q_paperid` int(11) NOT NULL,
  PRIMARY KEY (`q_id`),
  KEY `q_paperid` (`q_paperid`),
  CONSTRAINT `subjective_question_ibfk_1` FOREIGN KEY (`q_paperid`) REFERENCES `exam_paper` (`paper_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subjective_question`
--

LOCK TABLES `subjective_question` WRITE;
/*!40000 ALTER TABLE `subjective_question` DISABLE KEYS */;
INSERT INTO `subjective_question` VALUES (6,'请简述拥塞控制算法的主要过程。','我是拥塞算法标准答案。',10,30),(7,'请简述TCP和UDP协议的主要过程。','我是TCP/UDP的标准答案。',10,30);
/*!40000 ALTER TABLE `subjective_question` ENABLE KEYS */;
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
  CONSTRAINT `teacher_student_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `teacher_student_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `teacher_student_ibfk_3` FOREIGN KEY (`paper_id`) REFERENCES `exam_paper` (`paper_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_student`
--

LOCK TABLES `teacher_student` WRITE;
/*!40000 ALTER TABLE `teacher_student` DISABLE KEYS */;
INSERT INTO `teacher_student` VALUES ('T1616001','161630230',17),('T1616001','161630230',18),('T1616001','161630230',19),('T1616001','161630229',17),('T1616001','161630231',17),('T1616001','161630231',18),('T1616001','161630201',24),('T1616001','161630202',24),('T1616001','161630203',24),('T1616001','161630204',24),('T1616001','161630205',24),('T1616001','161630206',24),('T1616001','161630229',24),('T1616001','161630230',24),('T1616001','161630231',24),('T1616001','161630301',24),('T1616001','161640404',24),('T1616001','161630201',25),('T1616001','161630202',25),('T1616001','161630203',25),('T1616001','161630204',25),('T1616001','161630205',25),('T1616001','161630206',25),('T1616001','161630229',25),('T1616001','161630230',25),('T1616001','161630231',25),('T1616001','161630301',25),('T1616001','161640404',25),('T1616001','161630201',26),('T1616001','161630202',26),('T1616001','161630203',26),('T1616001','161630204',26),('T1616001','161630205',26),('T1616001','161630206',26),('T1616001','161630229',26),('T1616001','161630230',26),('T1616001','161630231',26),('T1616001','161630301',26),('T1616001','161640404',26),('T1616002','161630201',30),('T1616002','161630202',30),('T1616002','161630203',30),('T1616002','161630204',30),('T1616002','161630205',30),('T1616002','161630206',30),('T1616002','161630229',30),('T1616002','161630230',30),('T1616002','161630231',30);
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

-- Dump completed on 2019-12-26 17:13:14
