/*
SQLyog Ultimate v11.24 (32 bit)
MySQL - 5.6.15 
*********************************************************************
*/
/*!40101 SET NAMES utf8 */;

create table `user` (
	`user_id` varchar (16) not null ,
	`user_name` varchar (16) not null ,
	`user_email` varchar (64) not null ,
	`user_password` varchar (32) not null ,
	`user_create_time` datetime not null ,
	`user_update_time` datetime not null ,
	`user_type` varchar (8) not null ,
	primary key (user_id)
); 
insert into `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_create_time`, `user_update_time`, `user_type`) values('161630201','崔云峰','cui@yahoo.com','161630201','2019-11-30 21:14:27','2019-11-30 21:14:33','STUDENT');
insert into `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_create_time`, `user_update_time`, `user_type`) values('161630202','孙笑川','sun@dog.com','161630202','2019-11-30 21:16:34','2019-11-29 21:16:37','STUDENT');
insert into `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_create_time`, `user_update_time`, `user_type`) values('161630203','蒲银','py@sjtu.com','161630203','2019-11-28 21:15:34','2019-11-29 21:15:37','STUDENT');
insert into `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_create_time`, `user_update_time`, `user_type`) values('161630204','李赣','li@dog.com','161630204','2019-11-23 21:19:30','2019-11-29 21:19:33','STUDENT');
insert into `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_create_time`, `user_update_time`, `user_type`) values('161630205','泰隆','loong@qq.com','161630205','2019-11-04 21:20:18','2019-11-28 21:20:21','STUDENT');
insert into `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_create_time`, `user_update_time`, `user_type`) values('161630206','小呆呆','evil@man.com','161630206','2019-09-18 21:21:33','2019-11-28 21:21:36','STUDENT');
insert into `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_create_time`, `user_update_time`, `user_type`) values('161630229','王珊月','wang@qq.com','161630229','2019-11-09 19:36:16','2019-11-09 19:36:16','STUDENT');
insert into `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_create_time`, `user_update_time`, `user_type`) values('161630230','冼健邦','sin@qq.com','161630230','2019-11-09 19:24:00','2019-11-09 19:24:00','STUDENT');
insert into `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_create_time`, `user_update_time`, `user_type`) values('161630231','梁家娟','ljj@nuaa.com','161630231','2019-11-10 20:02:32','2019-11-10 20:02:32','STUDENT');
insert into `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_create_time`, `user_update_time`, `user_type`) values('161640404','高笑','gao@qq.com','161640404','2019-12-06 22:41:19','2019-12-06 22:41:19','STUDENT');
insert into `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_create_time`, `user_update_time`, `user_type`) values('Admin','管理员','admin@qq.com','Admin','2019-11-16 21:31:50','2019-11-16 21:31:50','ADMIN');
insert into `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_create_time`, `user_update_time`, `user_type`) values('T1616001','王力','jh@nuaa.com','T1616001','2019-11-10 20:41:51','2019-11-10 20:41:51','TEACHER');
insert into `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_create_time`, `user_update_time`, `user_type`) values('T1616002','张学友','zhang@qq.com','T1616002','2019-12-04 20:11:17','2019-12-04 20:11:17','TEACHER');
insert into `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_create_time`, `user_update_time`, `user_type`) values('T1616003','葛优','ge@qq.com','T1616003','2019-12-06 22:37:09','2019-12-06 22:37:09','TEACHER');
