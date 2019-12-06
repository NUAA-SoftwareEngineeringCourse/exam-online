create table exam_paper(
paper_id int(5) not null auto_increment,
paper_title varchar(32) not null ,
paper_desc varchar(1024) not null , -- paper desc is limited in 512 Chinese character
paper_time int(3) not null ,
paper_date datetime not null ,
paper_open int(1) not null ,
paper_path varchar(256) not null ,
paper_userid varchar(16) not null ,
primary key (paper_id)
);