create table user(
user_id varchar(16) not null,
user_name varchar(16) not null,
user_email varchar(64) not null,
user_password varchar(32) not null,
user_create_time DATETIME not null,
user_update_time DATETIME not null,
user_type varchar(8) not null,
primary key(user_id)
);