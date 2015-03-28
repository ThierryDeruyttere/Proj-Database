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
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'PythonLiker', 'P', '21232f297a57a5a743894a0e4a801fc3', 'p@hotmail.com',"0-01-01","9999-12-31","U");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'PythonLiker2', 'P2', '21232f297a57a5a743894a0e4a801fc3', 'p2@hotmail.com',"0-01-01","9999-12-31","U");
INSERT INTO user(is_active, first_name, last_name, password, email, joined_on, last_login, gender) VALUES (1,'C++Liker', 'C', '21232f297a57a5a743894a0e4a801fc3', 'c@hotmail.com',"2015-03-06","2015-03-06","F");

# Friend data
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (1,2,"2015-03-06",'Friends');

# Group data
INSERT INTO groups(group_name, group_type, created_on) VALUES ('Admins', 0,"2015-03-06");

# UserInGroup data
# Group creator is 0
INSERT INTO userInGroup(group_id, user_id, user_permissions, joined_on) VALUES (1,1,0,"2015-03-06");

# ProgrammingLanguage data
INSERT INTO programmingLanguage(name) VALUES ('Python');
INSERT INTO programmingLanguage(name) VALUES ('C++');

# ExerciseList data
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python1', '...', 1, 1, "2014-02-05", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python2', '...', 1, 1, "2014-02-05", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python3', '...', 1, 1, "2014-02-05", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python4', '...', 1, 1, "2014-02-05", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python5', '...', 1, 1, "2014-02-05", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python6', '...', 1, 1, "2014-02-05", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python7', '...', 1, 1, "2014-02-05", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('Python8', '...', 1, 1, "2014-02-05", 1);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('C++1', '...', 1, 1, "2014-02-05", 2);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('C++2', '...', 1, 1, "2014-02-05", 2);
INSERT INTO exerciseList(name, description ,difficulty, created_by, created_on, prog_lang_id)
VALUES ('C++3', '...', 1, 1, "2014-02-05", 2);

# Subject data
INSERT INTO subject(name) VALUES ('Sub1');
INSERT INTO subject(name) VALUES ('not Sub1');

# HasSubject data
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (1,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (1,2);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (2,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (3,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (5,1);
INSERT INTO hasSubject(exerciseList_id, subject_id) VALUES (6,2);

#insert into madeList
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,1,5,50, "2015-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,1,1,50, "2015-03-05");
