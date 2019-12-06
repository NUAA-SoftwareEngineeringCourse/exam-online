-- 记录学生是否完成了某份试题，若完成，则记录在表
create table student_exam_log(
paper_id int(5) not null,
student_id varchar(16) not null,
answer_json varchar(255) not null,
grade int(3) not null,
foreign key (paper_id) references `exam_paper`(paper_id),
foreign key (student_id) references `user`(user_id)
);