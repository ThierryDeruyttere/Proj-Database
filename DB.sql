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
  PRIMARY KEY(id)
);

CREATE TABLE friendsWith(
  first_id INT NOT NULL,
  second_id INT NOT NULL
);

CREATE TABLE groups(
  id INT NOT NULL AUTO_INCREMENT,
  group_name VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY(id)
);

CREATE TABLE userInGroup(
  group_id INT,
  user_id INT,
  FOREIGN KEY (group_id) REFERENCES groups(id),
  FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE programmingLanguage(
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY(id)
);

CREATE TABLE exercise(
  id INT NOT NULL AUTO_INCREMENT,
  difficulty INT NOT NULL,
  max_score INT NOT NULL,
  penalty INT NOT NULL,
  exercise_type VARCHAR(255) NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE code(
  id INT NOT NULL AUTO_INCREMENT,
  code_text BLOB NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE associatedWith(
  progLang_ID INT,
  exerc_ID INT,
  FOREIGN KEY (progLang_ID) REFERENCES programmingLanguage(id),
  FOREIGN KEY (exerc_ID) REFERENCES exercise(id)
);

CREATE TABLE isCodeFor(
  code_ID INT,
  exerc_ID INT,
  FOREIGN KEY (code_ID) REFERENCES code(id),
  FOREIGN KEY (exerc_ID) REFERENCES exercise(id)
);

CREATE TABLE madeEx(
  user_ID INT,
  exerc_ID INT,
  solved BOOLEAN NOT NULL,
  exercise_score INT NOT NULL,
  rating INT,
  FOREIGN KEY (user_ID) REFERENCES user(id),
  FOREIGN KEY (exerc_ID) REFERENCES exercise(id)
);


CREATE TABLE language(
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY(id)
);

CREATE TABLE question(
  id INT NOT NULL AUTO_INCREMENT,
  question_text BLOB NOT NULL,
  language_id INT,
  FOREIGN KEY (language_id) REFERENCES language(id),
  PRIMARY KEY(id)
);


CREATE TABLE isQuestionFor(
  question_id INT,
  exercise_id INT,
  FOREIGN KEY (question_id) REFERENCES question(id),
  FOREIGN KEY (exercise_id) REFERENCES exercise(id)
);

CREATE TABLE answer(
  id INT NOT NULL AUTO_INCREMENT,
  answer_text BLOB NOT NULL,
  language_id INT,
  is_answer_for INT,
  FOREIGN KEY (language_id) REFERENCES language(id),
  FOREIGN KEY (is_answer_for) REFERENCES exercise(id),
  PRIMARY KEY(id)
);

CREATE TABLE hint(
  hint_text varchar(255),
  hint_number INT,
  exercise_id INT,
  FOREIGN KEY (exercise_id) REFERENCES exercise(id)
);

CREATE TABLE exerciseList(
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description VARCHAR(255) NOT NULL,
  difficulty INT NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE hasSubject(
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

CREATE TABLE hasSubject(
  exerciseList_id INT,
  exercice_id INT,
  FOREIGN KEY (exerciseList_id) REFERENCES exerciseList(id),
  FOREIGN KEY (exercice_id) REFERENCES exercise(id)
);

CREATE TABLE madeList(
  exerciseList_id INT,
  user_id INT,
  rating INT NOT NULL,
  score INT NOT NULL,
  FOREIGN KEY (exerciseList_id) REFERENCES exerciseList(id),
  FOREIGN KEY (user_id) REFERENCES user(id)
);

INSERT INTO user(is_active, first_name, last_name, password,email) VALUES (1,'Thierry', 'Deruyttere', 'test', 'thierryderuyttere@hotmail.com');
