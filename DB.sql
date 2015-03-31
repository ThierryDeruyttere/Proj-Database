DROP DATABASE IF EXISTS codegalaxy;
CREATE DATABASE codegalaxy;
\r codegalaxy

CREATE TABLE user(
  id INT NOT NULL AUTO_INCREMENT,
  is_active BOOLEAN NOT NULL,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  permission INT DEFAULT 0,
  joined_on DATE NOT NULL,
  last_login DATE NOT NULL,
  gender VARCHAR(1) NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE friendsWith(
  user_id INT NOT NULL,
  friend_id INT NOT NULL,
  befriended_on DATE NOT NULL,
  status ENUM('Pending', 'Blocked', 'Friends') NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (friend_id) REFERENCES user(id),
  PRIMARY KEY (user_id, friend_id)
);

CREATE TABLE groups(
  id INT NOT NULL AUTO_INCREMENT,
  group_name VARCHAR(255) NOT NULL UNIQUE,
  group_type INT NOT NULL,
  created_on DATE NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE userInGroup(
  group_id INT,
  user_id INT,
  user_permissions INT,
  joined_on DATE,
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
  created_on DATE NOT NULL,
  prog_lang_id INT NOT NULL,
  default_language_code VARCHAR(255) NOT NULL,
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
  created_on DATE NOT NULL,
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
  code_text BLOB NOT NULL,
  exercise_id INT,
  FOREIGN KEY (exercise_id) REFERENCES exercise(id),
  PRIMARY KEY(exercise_id)
);

CREATE TABLE madeEx(
  user_id INT,
  exercise_id INT,
  solved BOOLEAN NOT NULL,
  exercise_score INT NOT NULL,
  rating INT,
  completed_on DATE,
  list_id INT,
  exercise_number INT,
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
  made_on DATE NOT NULL,
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
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'User1', 'A', '21232f297a57a5a743894a0e4a801fc3', 'u1@hotmail.com',"2015-03-06","2015-03-06","F");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'User2', 'B', '21232f297a57a5a743894a0e4a801fc3', 'u2@hotmail.com',"2015-03-06","2015-03-06","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'User3', 'C', '21232f297a57a5a743894a0e4a801fc3', 'u3@hotmail.com',"2015-03-06","2015-03-06","F");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'User4', 'D', '21232f297a57a5a743894a0e4a801fc3', 'u4@hotmail.com',"2015-03-06","2015-03-06","U");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'User5', 'E', '21232f297a57a5a743894a0e4a801fc3', 'u5@hotmail.com',"2015-03-06","2015-03-06","U");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'User6', 'F', '21232f297a57a5a743894a0e4a801fc3', 'u6@hotmail.com',"2015-03-06","2015-03-06","M");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'User7', 'M', '21232f297a57a5a743894a0e4a801fc3', 'u7@hotmail.com',"2015-03-06","2015-03-06","M");

# Friend data

# Group data
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Admins', 0,"2015-03-06");

# UserInGroup data
# Group creator is 0
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on) VALUES (1,1,0,"2015-03-06");

# ProgrammingLanguage data
INSERT INTO programmingLanguage(name) VALUES ('Python');
INSERT INTO programmingLanguage(name) VALUES ('C++');
INSERT INTO programmingLanguage(name) VALUES ('SQL');

# ExerciseList data
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python1', '...', 1, 1, "2015-03-28", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python2', '...', 1, 1, "2015-03-28", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python3', '...', 2, 1, "2014-02-05", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python4', '...', 2, 1, "2014-02-05", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python5', '...', 3, 1, "2014-02-05", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python6', '...', 3, 1, "2014-02-05", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python7', '...', 4, 1, "2014-02-05", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python8', '...', 5, 1, "2014-02-05", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('C++1', '...', 1, 1, "2014-02-05", 2);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('C++2', '...', 1, 1, "2014-02-05", 2);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('C++3', '...', 2, 1, "2014-02-05", 2);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('C++4', '...', 3, 1, "2014-02-05", 2);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('C++5', '...', 4, 1, "2014-02-05", 2);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('C++6', '...', 5, 1, "2014-02-05", 2);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('SQL1', '...', 1, 1, "2014-02-05", 3);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('SQL2', '...', 2, 1, "2014-02-05", 3);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('SQL3', '...', 3, 1, "2014-02-05", 3);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('SQL4', '...', 4, 1, "2014-02-05", 3);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('SQL5', '...', 5, 1, "2014-02-05", 3);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('SQL6', '...', 5, 1, "2014-02-05", 3);

# Subject data
INSERT INTO subject(name) VALUES ('Subject1');
INSERT INTO subject(name) VALUES ('Subject2');
INSERT INTO subject(name) VALUES ('Subject3');
INSERT INTO subject(name) VALUES ('Subject4');
INSERT INTO subject(name) VALUES ('Subject5');
INSERT INTO subject(name) VALUES ('Subject6');
INSERT INTO subject(name) VALUES ('Subject7');

# HasSubject data
# List 1 (1,2)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (1,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (1,2);
# List 2 (1,3)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (2,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (2,3);
# List 3 (2,4,5,6)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (3,2);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (3,4);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (3,5);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (3,6);
# List 4 (1,2,6)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (4,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (4,2);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (4,6);
# List 5 (2)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (5,2);
# List 6 (1,2,3,4,5,6)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (6,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (6,2);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (6,3);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (6,4);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (6,5);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (6,6);
# List 7 (1,3,5,7)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (7,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (7,3);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (7,5);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (7,7);
# List 8 (1,7)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (8,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (8,7);
# List 9 (1,7)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (9,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (9,7);
# List 10 (2,4,6)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (10,2);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (10,4);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (10,6);
# List 11 (3)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (11,3);
# List 12 (7)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (12,7);
# List 13 (2,3,7)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (13,2);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (13,3);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (13,7);
# List 14 (2,3,7)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (14,2);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (14,3);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (14,7);
# List 15 (2,3,7,5)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (15,2);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (15,3);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (15,5);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (15,7);
# List 16 (2,4,5,6)
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (16,2);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (16,4);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (16,5);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (16,6);
# List 17
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (17,5);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (17,6);
# List 18
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (18,1);
# List 19
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (19,2);
# List 20
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (20,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (20,2);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (20,3);

#insert into madeList
# user 1 (Python1-5,C1-3 | same ratings)
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,1,5,100, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,1,5,75, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (3,1,5,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (4,1,5,30, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (5,1,5,0, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (9,1,5,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (10,1,5,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (11,1,5,50, "2015-03-28");
# user 2 (Python1-2, C5, SQL1-5 | SQL low rating, C5 high, Py med)
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,2,4,10, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,2,4,15, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (13,2,5,20, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (15,2,1,35, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (16,2,2,49, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (17,2,3,60, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (14,2,2,80, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (18,2,1,100, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (19,2,2,50, "2015-03-28");
# user 3 (alles)

# user 4 (niks)

# user 5 (Python1-6 C2, Python low rating, C1-2 high mr lang geleden)
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,5,2,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,5,1,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (3,5,2,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (4,5,1,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (5,5,5,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (6,5,5,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (9,5,5,50, "2014-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (10,5,5,50, "2014-03-28");
# user 6 (Python1-2 week geleden, C1-3 maand geleden,SQL1 recent | same ratings)
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,6,5,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,6,5,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (9,6,5,50, "2015-01-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (10,6,5,50, "2015-01-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (11,6,5,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (15,6,5,50, "2015-03-28");
# user 7 (Python1-7 week geleden low rating | SQL1 recent high)
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,7,1,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,7,1,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (3,7,1,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (4,7,1,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (5,7,1,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (6,7,1,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (7,7,1,50, "2014-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (15,7,5,50, "2014-03-28");
