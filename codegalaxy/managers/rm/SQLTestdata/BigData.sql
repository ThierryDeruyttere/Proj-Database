# GETEST MET/ZONDER VRIENDEN EN MET/ZONDER SUBJECTS
# default_lists = [1,9,10,15]
# results: order of occurence

# NOTE: testen zonder persoon die alles heeft gemaakt (User3) mss
# deze zorgt er nl voor dat iedereen max overlapscore zit vr enlke lijst
# behalve de laatste SQL lijst

# Geen subjects/vrienden,wel U3:
# User1: Python(rest)->C++(rest)->SQL | OPM: SQL1 staat vanvoor aan de
#SQL omdat deze default is, anders event niet
# User2: Python(rest)->c++(rest)->SQL(laatste) | OPM: main reason dat SQL
#hier niet gepickt werd was niet de lage rating maar het checken van
#overlap met anderen, niemand had de laatste oef gemaakt
# User3: Enkel SQL lijst6 (rest al gemaakt), fav is hier C++ (ratings>aantal in dit geval)
# User4: In volgorde de recommended (default) ex gevolgd door (in volgorde)
# de rest vd lijsten (Python->C++->SQL)
# User5: Python->C++->SQL
# User6: C++->SQL->Python | OPM: dit is wss omdat # oef lineair een deel vd
# score bepaald, terwijl bij date set multipliers zijn
# User7: SQL1-5->Python8->SQL6->C++ | OPM: door de zeer lage ratings word
# SQL voor Python gegeven, SQL mist de overlapscore en komt dus nog wel erna


# MADELISTS
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
# user 3 (alles behalve 1 SQL oef)
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,3,4,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,3,4,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (3,3,5,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (4,3,1,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (5,3,2,50, "2014-03-05");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (6,3,3,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (7,3,2,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (8,3,1,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (9,3,2,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (10,3,4,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (11,3,4,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (12,3,4,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (13,3,5,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (14,3,1,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (15,3,2,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (16,3,3,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (17,3,2,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (18,3,1,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (19,3,2,50, "2015-03-28");
# user 4 (niks)

# user 5 (Python1-6 C1-2, Python low rating, C1-2 high mr lang geleden)
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,3,2,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,3,1,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (3,3,2,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (4,3,1,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (5,3,5,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (6,3,5,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (9,3,5,50, "2014-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (10,3,5,50, "2014-03-28");
# user 6 (Python1-2 week geleden, C1-3 maand geleden,SQL1 recent | same ratings)
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,3,5,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,3,5,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (9,3,5,50, "2015-01-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (10,3,5,50, "2015-01-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (11,3,5,50, "2015-03-28");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (15,3,5,50, "2015-03-28");
# user 7 (Python1-7 week geleden low rating | SQL1 recent high)
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (1,3,1,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (2,3,1,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (3,3,1,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (4,3,1,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (5,3,1,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (6,3,1,50, "2015-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (7,3,1,50, "2014-03-10");
INSERT INTO madeList(exerciseList_id, user_id, rating, score, made_on) VALUES (15,3,5,50, "2014-03-28");

# SUBJECTS
INSERT INTO subject(name) VALUES ('Sub1');
INSERT INTO subject(name) VALUES ('Sub2');
INSERT INTO subject(name) VALUES ('Sub3');
INSERT INTO subject(name) VALUES ('Sub4');
INSERT INTO subject(name) VALUES ('Sub5');
# FRIENDS
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (1,2,"2015-03-06",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (2,3,"2015-03-06",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (2,4,"2015-03-06",'Friends');
INSERT INTO friendsWith(user_id, friend_id, befriended_on,status) VALUES (5,6,"2015-03-06",'Friends');
