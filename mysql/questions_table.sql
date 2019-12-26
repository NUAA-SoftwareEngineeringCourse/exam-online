-- 单选和多选都是这个表
create table choice_question(
q_id int not null auto_increment,
q_description varchar(512) not null ,
q_value int(3) not null,
q_answer varchar(4) not null ,
q_A varchar(255) not null ,
q_B varchar(255) not null ,
q_C varchar(255) not null ,
q_D varchar(255) not null ,
q_paperid int not null ,
primary key (q_id),
foreign key (q_paperid) references exam_paper(paper_id)
);

create table judge_question(
q_id int not null auto_increment,
q_description varchar(512) not null ,
q_value int(3) not null ,
q_answer int(1) not null ,
q_paperid int not null ,
primary key(q_id),
foreign key(q_paperid) references exam_paper(paper_id)
);

create table subjective_question(
q_id int not null auto_increment,
q_description varchar(512) not null ,
q_answer varchar(512) not null ,
q_value int(3) not null ,
q_paperid int not null ,
primary key (q_id),
foreign key (q_paperid) references exam_paper(paper_id)
);