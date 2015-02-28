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
  PRIMARY KEY(id)
);

CREATE TABLE friendsWith(
  user_id INT NOT NULL,
  friend_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (friend_id) REFERENCES user(id)
);

CREATE TABLE groups(
  id INT NOT NULL AUTO_INCREMENT,
  group_name VARCHAR(255) NOT NULL UNIQUE,
  group_type INT NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE userInGroup(
  group_id INT,
  user_id INT,
  user_permissions INT,
  FOREIGN KEY (group_id) REFERENCES groups(id),
  FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE programmingLanguage(
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY(id)
);


CREATE TABLE language(
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,
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
  created_on DATE NOT NULL,
  exercise_number INT NOT NULL,
  correct_answer INT NOT NULL,
  exerciseList_id INT NOT NULL,
  FOREIGN KEY(exerciseList_id) REFERENCES exerciseList(id),
  PRIMARY KEY(id)
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
  id INT NOT NULL AUTO_INCREMENT,
  code_text BLOB NOT NULL,
  exercise_id INT,
  FOREIGN KEY (exercise_id) REFERENCES exercise(id),
  PRIMARY KEY(id)
);

CREATE TABLE madeEx(
  user_id INT,
  exercise_id INT,
  solved BOOLEAN NOT NULL,
  exercise_score INT NOT NULL,
  rating INT,
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (exercise_id) REFERENCES exercise(id)
);

CREATE TABLE question(
  id INT NOT NULL AUTO_INCREMENT,
  question_text BLOB NOT NULL,
  language_id INT,
  correct_answer INT,
  exercise_id INT,
  FOREIGN KEY (exercise_id) REFERENCES exercise(id),
  FOREIGN KEY (language_id) REFERENCES language(id),
  PRIMARY KEY(id)
);


CREATE TABLE hint(
  hint_text varchar(255),
  hint_number INT,
  exercise_id INT,
  FOREIGN KEY (exercise_id) REFERENCES exercise(id)
);


CREATE TABLE subject(
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE hasSubject(
  exerciseList_id INT,
  subject_id INT,
  FOREIGN KEY (exerciseList_id) REFERENCES exerciseList(id),
  FOREIGN KEY (subject_id) REFERENCES subject(id)
);

CREATE TABLE isPartOf(
  exerciseList_id INT,
  exercise_id INT,
  FOREIGN KEY (exerciseList_id) REFERENCES exerciseList(id),
  FOREIGN KEY (exercise_id) REFERENCES exercise(id)
);

CREATE TABLE madeList(
  exerciseList_id INT,
  user_id INT,
  rating INT NOT NULL,
  score INT NOT NULL,
  FOREIGN KEY (exerciseList_id) REFERENCES exerciseList(id),
  FOREIGN KEY (user_id) REFERENCES user(id)
);

# User data
INSERT INTO user(is_active, first_name, last_name, password, email) VALUES (1,'root', 'admin', 'e48e13207341b6bffb7fb1622282247b', 'root_admin_1337@hotmail.com');
INSERT INTO user(is_active, first_name, last_name, password, email) VALUES (1,'Thierry', 'Deruyttere', '098f6bcd4621d373cade4e832627b4f6', 'thierryderuyttere@hotmail.com');
INSERT INTO user(is_active, first_name, last_name, password, email) VALUES (1,'Sten', 'Verbois', '21232f297a57a5a743894a0e4a801fc3', 'stenverbois@gmail.com');
INSERT INTO user(is_active, first_name, last_name, password, email) VALUES (1,'Tristan', 'Vandeputte', '21232f297a57a5a743894a0e4a801fc3', 'tristanvandeputte@hotmail.com');
INSERT INTO user(is_active, first_name, last_name, password, email) VALUES (1,'Marie', 'Kegeleers', '21232f297a57a5a743894a0e4a801fc3', 'marie@.');
INSERT INTO user(is_active, first_name, last_name, password, email) VALUES (1,'Maarten', 'Jorens', '21232f297a57a5a743894a0e4a801fc3', 'maarten@.');

# Friend data
INSERT INTO friendsWith(user_id, friend_id) VALUES (1,2);
INSERT INTO friendsWith(user_id, friend_id) VALUES (3,2);
INSERT INTO friendsWith(user_id, friend_id) VALUES (3,4);
INSERT INTO friendsWith(user_id, friend_id) VALUES (3,5);
INSERT INTO friendsWith(user_id, friend_id) VALUES (3,6);

# Group data
INSERT INTO groups(group_name, group_type) VALUES ('Admins', 0);

# UserInGroup data
# Group creator is 0
INSERT INTO userInGroup(group_id, user_id, user_permissions) VALUES (1,1,0);
INSERT INTO userInGroup(group_id, user_id, user_permissions) VALUES (1,2,1);
INSERT INTO userInGroup(group_id, user_id, user_permissions) VALUES (1,3,1);
INSERT INTO userInGroup(group_id, user_id, user_permissions) VALUES (1,4,1);
INSERT INTO userInGroup(group_id, user_id, user_permissions) VALUES (1,5,1);
INSERT INTO userInGroup(group_id, user_id, user_permissions) VALUES (1,6,1);

# ProgrammingLanguage data
INSERT INTO programmingLanguage(name) VALUES ('Python');
INSERT INTO programmingLanguage(name) VALUES ('C++');
INSERT INTO programmingLanguage(name) VALUES ('SQL');

# ExerciseList data
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Beginning of a journey...', 'Python 101', 1, 1, "2014-2-5", 1);


# Exercise data
# Difficulty range 1-5?
INSERT INTO exercise(difficulty, max_score, penalty, exercise_type, created_by, created_on, exercise_number, correct_answer, exerciseList_id) VALUES (1,5,1,'code',1, '2015-02-1', 1,1,1);

# Code data
INSERT INTO code(code_text, exercise_id) VALUES ('print("")', 1);

# Language data
INSERT INTO language(name) VALUES ('English');
INSERT INTO language(name) VALUES ('Nederlands');

# Question data
INSERT INTO question(question_text, language_id, exercise_id)
    VALUES ('Print your name', 1,1);

# Anwer data
INSERT INTO answer(answer_number, answer_text, language_id, is_answer_for)
    VALUES (1,'Print your name', 1,1);

# Hint data
INSERT INTO hint(hint_text, hint_number, exercise_id)
    VALUES ('write print("your name here")', 1, 1);

# Subject data
INSERT INTO subject(name) VALUES ('Printing');

# HasSubject data
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (1,1);

#insert into madeList
INSERT INTO madeList(exerciseList_id, user_id, rating, score) VALUES (1,1,5,5);
INSERT INTO madeList(exerciseList_id, user_id, rating, score) VALUES (1,3,5,5);

#insert into madeEx
INSERT INTO madeEx(user_id, exercise_id, solved, exercise_score, rating) VALUES(1,1,1,5,5);
