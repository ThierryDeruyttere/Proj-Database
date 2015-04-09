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
  title VARCHAR(255) NOT NULL,
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
  exercise_id INT,
  solved BOOLEAN NOT NULL,
  exercise_score INT NOT NULL,
  completed_on DATETIME,
  list_id INT,
  exercise_number INT,
  last_answer BLOB,
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (exercise_id) REFERENCES exercise(id),
  PRIMARY KEY(user_id, exercise_id)
);

CREATE TABLE question(
  question_text BLOB NOT NULL,
  language_id INT,
  exercise_id INT,
  FOREIGN KEY (exercise_id) REFERENCES exercise(id),
  FOREIGN KEY (language_id) REFERENCES language(id),
  PRIMARY KEY(exercise_id)
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
  last_answer BLOB,
  # can be null
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

# User data
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Root', 'Admin', 'e48e13207341b6bffb7fb1622282247b', 'root_admin_1337@hotmail.com',"0-01-01 12:12:12","9999-12-31 12:12:12","U");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Thierry', 'Deruyttere', '098f6bcd4621d373cade4e832627b4f6', 'thierryderuyttere@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","F");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Sten', 'Verbois', '21232f297a57a5a743894a0e4a801fc3', 'stenverbois@gmail.com',"2015-03-06 12:12:12 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Tristan', 'Vandeputte', '21232f297a57a5a743894a0e4a801fc3', 'tristanvandeputte@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Marie', 'Kegeleers', '21232f297a57a5a743894a0e4a801fc3', 'marie@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","F");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'Maarten', 'Jorens', '21232f297a57a5a743894a0e4a801fc3', 'maarten@hotmail.com',"2015-03-06 12:12:12","2015-03-06 12:12:12","M");
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

# Friend data
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (1,2,"2015-03-06 12:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,2,"2015-03-05 12:12:13",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,4,"2015-03-01 12:12:14",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,5,"2015-03-03 12:12:15",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,6,"2015-02-06 12:12:16",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,7,"2015-03-06 12:12:17",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,8,"2015-03-06 12:12:18",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,9,"2015-03-06 12:12:19",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,10,"2015-03-06 12:22:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,11,"2015-03-06 12:32:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,12,"2015-03-07 12:42:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,13,"2015-03-06 12:52:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,14,"2015-03-06 13:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,15,"2015-03-02 14:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,16,"2015-03-06 15:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,17,"2015-03-06 16:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,18,"2015-03-05 17:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,19,"2015-01-06 18:12:12",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (3,20,"2015-03-06 19:12:12",'Friends');


# Group data
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
# Group creator is 0
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (1,1,1,"2015-03-06 13:42:33",'Pending');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (1,2,1,"2015-03-06 15:30:53",'Pending');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (1,3,1,"2015-03-06 13:20:45",'Pending');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (1,4,1,"2015-03-06 13:11:55",'Pending');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (1,5,1,"2015-03-06 20:12:22",'Member');
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on, status) VALUES (1,6,1,"2015-03-06 12:20:20",'Member');

# ProgrammingLanguage data
INSERT INTO programmingLanguage(name) VALUES ('Python');
INSERT INTO programmingLanguage(name) VALUES ('C++');
INSERT INTO programmingLanguage(name) VALUES ('SQL');

# ExerciseList data
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Beginning of a journey...', 'Python 101', 1, 1, "2014-02-05 10:10:10", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('The continuation of that journey...', '...', 1, 1, "2014-03-05 11:11:11", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Still not there yet...', '.......', 1, 1, "2014-02-06 12:12:12", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python for dummies', 'For those who are new', 2, 1, "2015-02-05 13:14:15", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python for experts', 'Yer a wizard Harry', 1, 1, "2014-03-05 13:15:14", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Advanced Templating Stuff', 'Aw yisss', 1, 1, "2014-02-12 12:11:10", 2);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('C++ for Grandmothers', 'Dont touch the screen gramps', 3, 1, "2014-02-05 10:19:54", 2);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('C++ -> C += 1', 'i C u like puns', 1, 1, "2020-02-05 23:12:36", 2);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('SQL injections: a short guide', 'Learn all about sql injections with this exercise list', 1, 1, "2014-02-05 12:19:19", 3);

# Exercise data
# Difficulty range 1-5?
INSERT INTO exercise(difficulty, max_score, penalty, exercise_type, created_by, created_on, exercise_number, correct_answer, exerciseList_id, title) VALUES (1,5,1,'Code',1, '1981-10-12 13:40:58', 1,1,1, "Question 1");
INSERT INTO exercise(difficulty, max_score, penalty, exercise_type, created_by, created_on, exercise_number, correct_answer, exerciseList_id, title) VALUES (2,5,1,'Code',1, '2001-09-11 12:12:12', 2,1,1, "Question 2");

# Code data
INSERT INTO code(code_text, exercise_id) VALUES ('print("")', 1);
INSERT INTO code(code_text, exercise_id) VALUES ('print("")', 2);

# Language data
INSERT INTO language(name,language_code) VALUES ('English','en');
INSERT INTO language(name,language_code) VALUES ('Nederlands','nl');

# Question data
INSERT INTO question(question_text, language_id, exercise_id)
VALUES ('Print your name.', 1,1);
INSERT INTO question(question_text, language_id, exercise_id)
VALUES ('Print something else.', 1,2);

# Anwer data
INSERT INTO answer(answer_number, answer_text, language_id, is_answer_for)
VALUES (1,'*', 1,1);
INSERT INTO answer(answer_number, answer_text, language_id, is_answer_for)
VALUES (1,'*', 1,2);

# Hint data
INSERT INTO hint(hint_text, hint_number, exercise_id, language_id)
VALUES ('write print("your name here")', 1, 1, 1);

# Subject data
INSERT INTO subject(name) VALUES ('Printing');
INSERT INTO subject(name) VALUES ('Tutorial');
INSERT INTO subject(name) VALUES ('42');
INSERT INTO subject(name) VALUES ('Awesomeness');
INSERT INTO subject(name) VALUES ('Yourneying');

# HasSubject data
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (1,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (1,5);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (2,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (2,5);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (3,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (3,5);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (4,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (4,5);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (4,2);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (5,5);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (5,2);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (7,2);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (6,3);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (8,4);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (9,4);

#insert into madeList
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,1,3,75, "2018-12-05 16:23:05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,3,4,30, "2001-01-06 13:14:48");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,2,5,50, "1985-07-20 23:54:21");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,6,5,30, "1999-08-22 17:17:42");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (3,3,5,30, "2015-03-05 12:12:12");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (3,6,5,30, "1985-07-20 23:54:50");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (4,6,5,30, "2015-03-05 13:13:13");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (8,12,5,30, "2015-03-05 14:14:14");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,12,5,30, "1999-07-13 18:12:05");

#insert into madeEx
INSERT INTO madeEx(user_id, exercise_id, solved, exercise_score, completed_on) VALUES(1,1,1,5,"2015-03-06 10:10:10");
