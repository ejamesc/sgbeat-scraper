DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id int(8) primary key auto_increment,
	username varchar(128) unique not null
);

DROP TABLE IF EXISTS tweets;
CREATE TABLE tweets (
	id int(8) primary key auto_increment,
	user int(8) REFERENCES users(id),
	tweet varchar(256)
);