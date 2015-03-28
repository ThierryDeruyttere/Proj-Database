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

# Friend data
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (1,2,"2015-03-06",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (2,3,"2015-03-06",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (2,4,"2015-03-06",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (5,6,"2015-03-06",'Friends');

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

# Subject data
INSERT INTO subject(name) VALUES ('Sub1');
INSERT INTO subject(name) VALUES ('Sub2');
INSERT INTO subject(name) VALUES ('Sub3');
INSERT INTO subject(name) VALUES ('Sub4');
INSERT INTO subject(name) VALUES ('Sub5');

# HasSubject data


#insert into madeList
# user 1 (Python1-5,C1-3 | same ratings)
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,1,5,100, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,1,5,75, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (3,1,5,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (4,1,5,30, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (5,1,5,0, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (9,1,5,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (10,1,5,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (11,1,5,50, "2015-03-28");
# user 2 (Python1-2, C5, SQL1-5 | SQL low rating, C5 high, Py med)
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,2,4,10, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,2,4,15, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (13,2,5,20, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (15,2,1,35, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (16,2,2,49, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (17,2,3,60, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (14,2,2,80, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (18,2,1,100, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (19,2,2,50, "2015-03-28");
# user 3 (niks)

# user 4 (alles)
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,3,4,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,3,4,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (3,3,5,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (4,3,1,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (5,3,2,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (6,3,3,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (7,3,2,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (8,3,1,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (9,3,2,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (10,3,4,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (11,3,4,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (12,3,4,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (13,3,5,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (14,3,1,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (15,3,2,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (16,3,3,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (17,3,2,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (18,3,1,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (19,3,2,50, "2015-03-28");
# user 5 (Python1-2, C5, SQL1-5)
# user 6 (Python1-2, C5, SQL1-5)
# user 7 (Python1-2, C5, SQL1-5)
# user 8 (Python1-2, C5, SQL1-5)
