/*
SQLyog Ultimate v11.24 (32 bit)
MySQL - 5.6.15 
*********************************************************************
*/
/*!40101 SET NAMES utf8 */;

create table `teacher_student` (
	`teacher_id` varchar (16) not null ,
	`student_id` varchar (16) not null ,
	foreign key(teacher_id) references `user`(user_id),
	foreign key(student_id) references `user`(user_id)
); 
insert into `teacher_student` (`teacher_id`, `student_id`) values('T1616001','161630230');
insert into `teacher_student` (`teacher_id`, `student_id`) values('T1616002','161630230');
insert into `teacher_student` (`teacher_id`, `student_id`) values('T1616003','161630230');
