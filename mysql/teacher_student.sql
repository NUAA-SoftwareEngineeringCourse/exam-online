create table teacher_student(
teacher_id varchar(16) not null,
student_id varchar(16) not null,
foreign key (teacher_id) references `user`(user_id),
foreign key (student_id) references `user`(user_id)
);