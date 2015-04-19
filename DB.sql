# Sandbox user privileges
GRANT ALL PRIVILEGES ON sandbox.* TO 'sandbox'@'localhost' IDENTIFIED BY 'sandbox';
CREATE DATABASE IF NOT EXISTS sandbox;

DROP DATABASE IF EXISTS codegalaxy;
CREATE DATABASE codegalaxy;
use codegalaxy

CREATE TABLE user(
  id INT NOT NULL AUTO_INCREMENT,
  is_active BOOLEAN NOT NULL,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  permission INT DEFAULT 0,
  joined_on DATETIME NOT NULL,
  last_login DATETIME NOT NULL,
  gender VARCHAR(1) NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE friendsWith(
  user_id INT NOT NULL,
  friend_id INT NOT NULL,
  befriended_on DATETIME NOT NULL,
  status ENUM('Pending', 'Blocked', 'Friends') NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (friend_id) REFERENCES user(id),
  PRIMARY KEY (user_id, friend_id)
);

CREATE TABLE groups(
  id INT NOT NULL AUTO_INCREMENT,
  group_name VARCHAR(255) NOT NULL UNIQUE,
  group_type INT NOT NULL,
  created_on DATETIME NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE userInGroup(
  group_id INT,
  user_id INT,
  user_permissions INT,
  joined_on DATETIME,
  status ENUM('Pending', 'Blocked', 'Member') NOT NULL,
  FOREIGN KEY (group_id) REFERENCES groups(id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  PRIMARY KEY(group_id, user_id)
);

CREATE TABLE programmingLanguage(
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY(id)
);

CREATE TABLE language(
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,
  language_code VARCHAR(225) NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE exerciseList(
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description VARCHAR(255) NOT NULL,
  difficulty INT NOT NULL,
  created_by INT NOT NULL,
  created_on DATETIME NOT NULL,
  prog_lang_id INT NOT NULL,
  FOREIGN KEY (prog_lang_id) REFERENCES programmingLanguage(id),
  PRIMARY KEY(id)
);

CREATE TABLE exercise(
  id INT NOT NULL AUTO_INCREMENT,
  difficulty INT NOT NULL,
  max_score INT NOT NULL,
  penalty INT NOT NULL,
  exercise_type VARCHAR(255) NOT NULL,
  created_by INT NOT NULL,
  created_on DATETIME NOT NULL,
  exercise_number INT NOT NULL,
  correct_answer INT NOT NULL,
  exerciseList_id INT NOT NULL,
  FOREIGN KEY(exerciseList_id) REFERENCES exerciseList(id),
  PRIMARY KEY(id)
);

CREATE TABLE exercise_references(
  original_id INT NOT NULL,
  new_list_id INT NOT NULL,
  new_list_exercise_number INT NOT NULL
);

CREATE TABLE answer(
  answer_number INT NOT NULL,
  answer_text BLOB NOT NULL,
  language_id INT,
  is_answer_for INT,
  FOREIGN KEY (language_id) REFERENCES language(id),
  FOREIGN KEY (is_answer_for) REFERENCES exercise(id),
  PRIMARY KEY(is_answer_for, answer_number, language_id)
);

CREATE TABLE code(
  code_text BLOB,
  exercise_id INT,
  FOREIGN KEY (exercise_id) REFERENCES exercise(id),
  PRIMARY KEY(exercise_id)
);

CREATE TABLE madeEx(
  user_id INT,
  solved BOOLEAN NOT NULL,
  exercise_score INT NOT NULL,
  completed_on DATETIME,
  list_id INT,
  exercise_number INT,
  last_answer BLOB,
  hints_used INT,
  FOREIGN KEY (user_id) REFERENCES user(id),
  PRIMARY KEY(user_id, exercise_number, list_id)
);

CREATE TABLE question(
  question_text BLOB NOT NULL,
  language_id INT,
  exercise_id INT,
  FOREIGN KEY (exercise_id) REFERENCES exercise(id),
  FOREIGN KEY (language_id) REFERENCES language(id),
  PRIMARY KEY(exercise_id, language_id)
);

CREATE TABLE hint(
  hint_text varchar(255),
  hint_number INT,
  exercise_id INT,
  language_id INT,
  FOREIGN KEY (language_id) REFERENCES language(id),
  FOREIGN KEY (exercise_id) REFERENCES exercise(id),
  PRIMARY KEY (hint_number, exercise_id, language_id)
);


CREATE TABLE subject(
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY(id)
);

CREATE TABLE hasSubject(
  exerciseList_id INT,
  subject_id INT,
  FOREIGN KEY (exerciseList_id) REFERENCES exerciseList(id),
  FOREIGN KEY (subject_id) REFERENCES subject(id),
  PRIMARY KEY (exerciseList_id, subject_id)
);

CREATE TABLE madeList(
  exerciseList_id INT,
  user_id INT,
  rating INT NOT NULL,
  score INT NOT NULL,
  made_on DATETIME NOT NULL,
  FOREIGN KEY (exerciseList_id) REFERENCES exerciseList(id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  PRIMARY KEY (exerciseList_id, user_id)
);

CREATE TABLE verification(
  email VARCHAR(255) NOT NULL UNIQUE,
  hash VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY(hash),
  FOREIGN KEY (email) REFERENCES user(email)
);

CREATE TABLE exerciseTitle(
  title VARCHAR(255) NOT NULL,
  language_id INT NOT NULL,
  exercise_id INT NOT NULL,
  PRIMARY KEY(language_id, exercise_id),
  FOREIGN KEY(exercise_id) REFERENCES exercise(id),
  FOREIGN KEY(language_id) REFERENCES language(id)
);

# User data (20 users)
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Root', 'Admin', 'e48e13207341b6bffb7fb1622282247b', 'root_admin_1337@hotmail.com',"0-01-01 12:12:12","9999-12-31 12:12:12","U");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Thierry', 'Deruyttere', '098f6bcd4621d373cade4e832627b4f6', 'thierryderuyttere@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Sten', 'Verbois', '21232f297a57a5a743894a0e4a801fc3', 'stenverbois@gmail.com',"2015-03-06 12:12:12 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Tristan', 'Vandeputte', '21232f297a57a5a743894a0e4a801fc3', 'tristanvandeputte@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Marie', 'Kegeleers', '21232f297a57a5a743894a0e4a801fc3', 'marie@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","F");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Maarten', 'Jorens', '21232f297a57a5a743894a0e4a801fc3', 'maarten@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","F");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Dirk', 'Jan', '21232f297a57a5a743894a0e4a801fc3', 'dirk@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Thomas', 'Vandelanotte', '21232f297a57a5a743894a0e4a801fc3', 'Thomas@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Pieter', 'Jan', '21232f297a57a5a743894a0e4a801fc3', 'Pieter@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Bart', 'De Wever', '21232f297a57a5a743894a0e4a801fc3', 'Bart@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Chris', 'Brys', '21232f297a57a5a743894a0e4a801fc3', 'Chris@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Jommeke', 'Hegre', '21232f297a57a5a743894a0e4a801fc3', 'Jommeke@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Fany', 'Kiekeboe', '21232f297a57a5a743894a0e4a801fc3', 'Fany@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","F");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Wouter', 'Vanuitdebroeken', '21232f297a57a5a743894a0e4a801fc3', 'Wouter@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Kalm', 'Zalm', '21232f297a57a5a743894a0e4a801fc3', 'Kalm@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","U");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Alaise', 'Pladijs', '21232f297a57a5a743894a0e4a801fc3', 'Alaise@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","F");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Alain', 'Drissens', '21232f297a57a5a743894a0e4a801fc3', 'Alain@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Rudy', 'Verboven', '21232f297a57a5a743894a0e4a801fc3', 'Rudy@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Bruno', 'Tobback', '21232f297a57a5a743894a0e4a801fc3', 'Bruno@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Janneman', 'Stanneman', '21232f297a57a5a743894a0e4a801fc3', 'Janneman@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");

# Friend data (telkens User X, de volgende moeten met deze dan geen rekening meer houden)
# user 1
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (1,2,"2015-03-06 05:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (1,3,"2015-04-01 12:12:14",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (1,4,"2015-03-12 12:12:14",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (1,6,"2015-03-16 12:12:15",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (1,8,"2015-04-03 12:12:15",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (1,13,"2015-02-08 03:12:16",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (1,16,"2015-03-06 12:12:17",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (1,20,"2015-03-11 08:12:18",'Friends');
# user 2
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (2,6,"2015-03-15 05:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (2,7,"2015-03-01 12:12:14",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (2,11,"2015-04-06 05:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (2,13,"2015-03-11 12:12:14",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (2,15,"2015-04-03 12:12:15",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (2,16,"2015-02-06 03:12:16",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (2,18,"2015-03-18 12:12:17",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (2,19,"2015-03-06 08:12:18",'Friends');
# user 3
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,4,"2015-03-01 12:12:14",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,5,"2015-03-03 12:12:15",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,6,"2015-02-01 03:12:16",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,7,"2015-04-06 12:12:17",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,8,"2015-03-04 08:12:18",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,9,"2015-04-06 12:12:19",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,10,"2015-03-06 12:22:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,11,"2015-03-23 10:32:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,12,"2015-03-07 12:42:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,13,"2015-04-05 11:52:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,14,"2015-03-06 13:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,15,"2015-04-09 14:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,16,"2015-03-06 15:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,17,"2015-03-06 01:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,18,"2015-04-05 17:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,19,"2015-01-10 18:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,20,"2015-03-06 19:12:12",'Friends');
# user 4
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (4,5,"2015-03-28 12:12:19",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (4,7,"2015-04-06 12:22:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (4,14,"2015-03-07 10:32:12",'Friends');
# user 5
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (5,9,"2015-03-07 12:42:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (5,10,"2015-03-21 11:52:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (5,14,"2015-04-06 13:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (5,15,"2015-03-16 14:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (5,16,"2015-03-04 15:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (5,20,"2015-04-06 01:12:12",'Friends');
# user 6
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (6,7,"2015-03-05 17:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (6,8,"2015-01-06 18:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (6,9,"2015-03-23 19:12:12",'Friends');
# user 7
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (7,11,"2015-04-06 18:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (7,13,"2015-04-06 19:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (7,14,"2015-03-05 17:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (7,16,"2015-01-06 18:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (7,19,"2015-03-06 19:12:12",'Friends');
# user 8
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (8,10,"2015-04-06 19:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (8,11,"2015-03-05 17:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (8,18,"2015-04-06 18:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (8,20,"2015-03-06 19:12:12",'Friends');
# user 9
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (9,13,"2015-03-05 17:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (9,14,"2015-01-06 18:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (9,15,"2015-04-06 19:12:12",'Friends');
# user 10
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (10,12,"2015-03-06 19:12:12",'Friends');
# user 11
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (11,13,"2015-03-05 17:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (11,14,"2015-01-22 18:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (11,15,"2015-04-21 19:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (11,17,"2015-03-05 17:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (11,19,"2015-04-19 18:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (11,10,"2015-03-06 19:12:12",'Friends');
# user 12
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (12,18,"2015-03-05 17:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (12,19,"2015-04-21 18:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (12,20,"2015-03-06 19:12:12",'Friends');
# user 13
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (13,14,"2015-03-05 17:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (13,15,"2015-01-06 18:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (13,17,"2015-04-02 19:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (13,18,"2015-03-05 17:12:12",'Friends');
# user 14
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (14,16,"2015-03-05 17:12:12",'Friends');
# user 15
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (15,16,"2015-04-09 17:12:12",'Friends');
# user 17
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (17,19,"2015-03-05 17:12:12",'Friends');

# Group data (~ 30 groepen)
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Admins', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('OLVE', 1,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('OLVC', 1,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Sint-Michielscollege', 1,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Universiteit Antwerpen', 1,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Universiteit Gent', 1,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('KDG', 1,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('VUB', 1,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('De bende van de bosklapper', 1,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('NVA sympathisanten', 1,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Groen! sympathisanten', 1,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('PVDA sympathisanten', 1,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Open-VLD sympathisanten', 1,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('sp.a sympathisanten', 1,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Vlaanderen', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Wallonie', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Brussel', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Antwerpen', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Russia', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Nederland', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Great-Britain', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('USA', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Wilrijk', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Edegem', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Mechelen', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Brasschaat', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Merksem', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Schoten', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Knokke', 0,"2015-03-06 19:12:12");
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Aartselaar', 0,"2015-03-06 19:12:12");


# UserInGroup data
# Group creator is 0, admin 1, user 2
# group 1
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (1,1,0,"2015-03-06 13:42:33",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (1,2,2,"2015-03-06 15:30:53",'Pending');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (1,3,1,"2015-03-06 13:20:45",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (1,4,1,"2015-03-06 13:11:55",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (1,5,2,"2015-03-06 20:12:22",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (1,6,2,"2015-03-06 12:20:20",'Member');
# group 2
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (2,4,0,"2015-03-06 13:42:33",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (2,6,2,"2015-03-06 15:30:53",'Pending');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (2,7,2,"2015-03-06 13:20:45",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (2,9,2,"2015-03-06 13:11:55",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (2,17,2,"2015-03-06 20:12:22",'Pending');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (2,18,2,"2015-03-06 12:20:20",'Member');
# group 3
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (3,8,0,"2015-03-06 13:42:33",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (3,9,1,"2015-03-06 15:30:53",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (3,11,2,"2015-03-06 13:20:45",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (3,13,2,"2015-03-06 13:11:55",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (3,15,2,"2015-03-06 20:12:22",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (3,20,1,"2015-03-06 12:20:20",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (3,8,2,"2015-03-06 13:42:33",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (3,9,2,"2015-03-06 15:30:53",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (3,11,2,"2015-03-06 13:20:45",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (3,13,1,"2015-03-06 13:11:55",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (3,15,2,"2015-03-06 20:12:22",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (3,20,2,"2015-03-06 12:20:20",'Member');
# group 4
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (4,13,0,"2015-03-06 13:42:33",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (4,14,1,"2015-03-06 15:30:53",'Member');
# group 5
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (5,11,2,"2015-03-06 13:20:45",'Pending');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (5,12,1,"2015-03-06 13:11:55",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (5,7,0,"2015-03-06 20:12:22",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (5,17,2,"2015-03-06 12:20:20",'Member');
# group 6
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (6,2,2,"2015-03-06 13:20:45",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (6,4,1,"2015-03-06 13:11:55",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (6,6,0,"2015-03-06 20:12:22",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (6,11,2,"2015-03-06 12:20:20",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (6,13,2,"2015-03-06 20:12:22",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (6,15,2,"2015-03-06 12:20:20",'Member');
# group 7
# group 8
# group 9
# group 10
# group 11
# group 12
# group 13
# group 14
# group 15
# group 16
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,1,2,"2015-03-06 13:20:45",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,2,1,"2015-03-06 13:11:55",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,3,0,"2015-03-06 20:12:22",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,4,2,"2015-03-06 12:20:20",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,5,2,"2015-03-06 20:12:22",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,6,2,"2015-03-06 12:20:20",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,7,2,"2015-03-06 13:20:45",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,8,1,"2015-03-06 13:11:55",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,9,2,"2015-03-06 20:12:22",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,10,1,"2015-03-06 12:20:20",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,11,2,"2015-03-06 20:12:22",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,13,2,"2015-03-06 12:20:20",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,14,2,"2015-03-06 13:20:45",'Pending');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,15,1,"2015-03-06 13:11:55",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,16,2,"2015-03-06 20:12:22",'Pending');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,17,2,"2015-03-06 12:20:20",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,19,2,"2015-03-06 20:12:22",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (16,20,2,"2015-03-06 12:20:20",'Pending');
# group 17
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (17,12,1,"2015-03-06 13:20:45",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (17,18,0,"2015-03-06 13:20:45",'Member');
# group 18
# group 19
# group 20
# group 21
# group 22
# group 23
# group 24
# group 25
# group 26
# group 27
# group 28
# group 29

# ProgrammingLanguage data
INSERT INTO programmingLanguage(name) VALUES ('Python');
INSERT INTO programmingLanguage(name) VALUES ('C++');
INSERT INTO programmingLanguage(name) VALUES ('SQL');
