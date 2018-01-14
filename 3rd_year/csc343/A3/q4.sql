
-- MissingQuestions

SET SEARCH_PATH TO quizschema;
drop table if exists q4 cascade;

-- You must not change this table definition.

create table q4(
sid VARCHAR(100),
question_id INT,
questionText VARCHAR(500)
);


-- You may find it convenient to do this for each of the views
-- that define your intermediate steps.  (But give them better names!)
DROP VIEW IF EXISTS allQuizStudents CASCADE;
DROP VIEW IF EXISTS allQuestions CASCADE;
DROP VIEW IF EXISTS studentsAndQuestions CASCADE;
DROP VIEW IF EXISTS allMcResponses CASCADE;
DROP VIEW IF EXISTS allTfResponses CASCADE;
DROP VIEW IF EXISTS allNumResponses CASCADE;
DROP VIEW IF EXISTS allResponses CASCADE;
DROP VIEW IF EXISTS missingQuestions  CASCADE;
DROP VIEW IF EXISTS final CASCADE;


-- Define views for your intermediate steps here.

-- all students who are in the grade 8 class in room 120 with teacher "Mr Higgins"

CREATE VIEW allQuizStudents as

  SELECT enrollments.sid as sid
  FROM enrollments,
       classes,
       students,
       rooms
  WHERE enrollments.cid = classes.cid and
        classes.rid = rooms.rid and
        classes.grade = 8 and
        rooms.rid = 120 and
        rooms.teacher = 'Mr Higgins' and
        students.sid = enrollments.sid;

-- all questions in the quiz

CREATE VIEW allQuestions as

  SELECT questions_on_quiz.question_id as qid
  FROM questions_on_quiz
  WHERE questions_on_quiz.quiz_id = 'Pr1-220310';

-- a fake table relating every students in class to every one of the quesitons in the quiz

CREATE VIEW studentsAndQuestions as
  SELECT *
  FROM allQuizStudents CROSS JOIN allQuestions;

-- all received responses from students

CREATE VIEW allMcResponses as
  SELECT student_responses_mc.sid,
          student_responses_mc.question_id as qid
   FROM student_responses_mc,classes
   WHERE student_responses_mc.quiz_id = 'Pr1-220310' and
        student_responses_mc.cid = classes.cid and
        classes.grade = 8 and
        classes.rid = 120;


CREATE VIEW allTfResponses as
  SELECT student_responses_tf.sid,
          student_responses_tf.question_id as qid
   FROM student_responses_tf,classes
   WHERE student_responses_tf.quiz_id = 'Pr1-220310' and
        student_responses_tf.cid = classes.cid and
        classes.grade = 8 and
        classes.rid = 120;


CREATE VIEW allNumResponses as
  SELECT student_responses_num.sid,
          student_responses_num.question_id as qid
   FROM student_responses_num,classes
   WHERE student_responses_num.quiz_id = 'Pr1-220310' and
        student_responses_num.cid = classes.cid and
        classes.grade = 8 and
        classes.rid = 120;


CREATE VIEW allResponses as
  (SELECT *
  FROM allMcResponses
  )
  UNION
  (SELECT *
  FROM allTfResponses
  )
  UNION
  (SELECT *
  FROM allNUmResponses
  );




-- all missing questions and the name of students who miss them

CREATE VIEW missingQuestions as

  (SELECT *
  FROM studentsAndQuestions)
  except
  (SELECT *
  FROM allResponses);



-- all missing questions, student names and question texts

  CREATE VIEW final as
  SELECT missingQuestions.sid,
         missingQuestions.qid,
         question_bank.question_text as text
  FROM missingQuestions, question_bank
  WHERE missingQuestions.qid = question_bank.question_id;






-- the answer to the query
insert into q4 (sid ,
                question_id ,
                questionText)
(select sid,
        qid,
        text
 from final);
