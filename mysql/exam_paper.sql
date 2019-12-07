/*
SQLyog Ultimate v11.24 (32 bit)
MySQL - 5.6.15 
*********************************************************************
*/
/*!40101 SET NAMES utf8 */;

create table `exam_paper` (
	`paper_id` int (5) not null auto_increment,
	`paper_title` varchar (32) not null ,
	`paper_desc` varchar (1024) not null ,
	`paper_time` int (3) not null ,
	`paper_date` datetime not null ,
	`paper_open` tinyint (1) not null ,
	`paper_path` varchar (256) not null ,
	`paper_userid` varchar (16) not null ,
	primary key(paper_id)
); 
insert into `exam_paper` (`paper_id`, `paper_title`, `paper_desc`, `paper_time`, `paper_date`, `paper_open`, `paper_path`, `paper_userid`) values('13','计算机网络','考察所有讲过的内容，重点章节：第二、五、八章。','120','2019-12-29 10:00:00','0','E:\\Program Files\\PyCharm\\workspace\\exam-online\\FilesUpload\\ExamPapers\\T1616001-计算机网络.xlsx','T1616001');
insert into `exam_paper` (`paper_id`, `paper_title`, `paper_desc`, `paper_time`, `paper_date`, `paper_open`, `paper_path`, `paper_userid`) values('14','操作系统','考察第一章到第十章，PPT涉及的内容，请同学们做好复习工作。','120','2020-01-15 14:00:00','0','E:\\Program Files\\PyCharm\\workspace\\exam-online\\FilesUpload\\ExamPapers\\T1616002-操作系统.xlsx','T1616002');
insert into `exam_paper` (`paper_id`, `paper_title`, `paper_desc`, `paper_time`, `paper_date`, `paper_open`, `paper_path`, `paper_userid`) values('15','软件测试','考察第一章到第十章，PPT涉及的内容，请同学们做好复习工作。','120','2019-12-31 10:00:00','0','E:\\Program Files\\PyCharm\\workspace\\exam-online\\FilesUpload\\ExamPapers\\T1616003-软件测试.xlsx','T1616003');
