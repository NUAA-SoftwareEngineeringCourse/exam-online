/*
SQLyog Ultimate v11.24 (32 bit)
MySQL - 5.6.15 
*********************************************************************
*/
/*!40101 SET NAMES utf8 */;

create table `student_exam_log` (
	`paper_id` int (5) not null ,
	`student_id` varchar (16) not null ,
	`answer_json` varchar (255) not null ,
	`grade` int (3) not null ,
	`full_grade` int (3) not null ,
	`subjective_grade` int(3) not null ,
	foreign key (paper_id) references `exam_paper`(paper_id) ,
	foreign key (student_id) references `user`(user_id)
); 
insert into `student_exam_log` (`paper_id`, `student_id`, `answer_json`, `grade`, `full_grade`) values('15','161630230','{\"0\":\"A\",\"1\":\"A\",\"2\":\"A\",\"3\":\"A\",\"4\":\"A\",\"5\":\"A\",\"6\":\"A\",\"7\":\"A\",\"8\":\"A\",\"9\":\"A\",\"10\":\"ABC\",\"11\":\"ABC\",\"12\":\"ABC\",\"13\":\"1\",\"14\":\"1\",\"15\":\"1\",\"16\":\"1\",\"17\":\"1\"}','90','100');
insert into `student_exam_log` (`paper_id`, `student_id`, `answer_json`, `grade`, `full_grade`) values('13','161630230','{\"0\":\"A\",\"1\":\"A\",\"2\":\"A\",\"3\":\"A\",\"4\":\"A\",\"5\":\"A\",\"6\":\"A\",\"7\":\"A\",\"8\":\"A\",\"9\":\"A\",\"10\":\"ABC\",\"11\":\"BCD\",\"12\":\"ABC\",\"13\":\"1\",\"14\":\"1\",\"15\":\"1\",\"16\":\"1\",\"17\":\"0\"}','98','100');
insert into `student_exam_log` (`paper_id`, `student_id`, `answer_json`, `grade`, `full_grade`) values('14','161630230','{\"0\":\"A\",\"1\":\"B\",\"2\":\"A\",\"3\":\"A\",\"4\":\"A\",\"5\":\"A\",\"6\":\"A\",\"7\":\"A\",\"8\":\"A\",\"9\":\"A\",\"10\":\"ABC\",\"11\":\"BCD\",\"12\":\"ABC\",\"13\":\"1\",\"14\":\"1\",\"15\":\"1\",\"16\":\"1\",\"17\":\"1\"}','94','100');
