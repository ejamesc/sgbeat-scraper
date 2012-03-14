DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id int(8) primary key auto_increment,
	username varchar(128) unique not null
);

DROP TABLE IF EXISTS tweets;
CREATE TABLE tweets (
	id int(8) primary key auto_increment,
	user int(8) REFERENCES users(id),
	location varchar(128) CHARACTER SET utf8 DEFAULT NULL,
	tweet varchar(256) CHARACTER SET utf8 not null
);