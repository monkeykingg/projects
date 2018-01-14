
-- QuizGrades

SET SEARCH_PATH TO quizschema;
drop table if exists q3 cascade;

-- You must not change this table definition.

create table q3(
sid VARCHAR(100),
lastName VARCHAR(50),
grade INT
);


-- You may find it convenient to do this for each of the views
-- that define your intermediate steps.  (But give them better names!)
DROP VIEW IF EXISTS allQuizStudents CASCADE;
DROP VIEW IF EXISTS allResponses CASCADE;
DROP VIEW IF EXISTS mcQuestions CASCADE;
DROP VIEW IF EXISTS tfQuestions CASCADE;
DROP VIEW IF EXISTS numQuestions CASCADE;
DROP VIEW IF EXISTS mcStudentsGrade CASCADE;
DROP VIEW IF EXISTS tfStudentsGrade CASCADE;
DROP VIEW IF EXISTS numStudentsGrade CASCADE;
DROP VIEW IF EXISTS zeroStudents CASCADE;
DROP VIEW IF EXISTS notZeroStudents CASCADE;
DROP VIEW IF EXISTS allStudentGrades CASCADE;
DROP VIEW IF EXISTS final CASCADE;


-- Define views for your intermediate steps here.

-- all students who are in the grade 8 class in room 120 with teacher "Mr Higgins"

CREATE VIEW allQuizStudents as

  SELECT enrollments.sid as sid,
         students.last_name as lastName
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

-- all multiple choice questions in the quiz and their weights and correct answers

CREATE VIEW mcQuestions as

  SELECT questions_on_quiz.question_id as qid,
         questions_on_quiz.weight,
         correct_answer as mcAnswer
  FROM questions_on_quiz,
       mc_question_correct_answers
  WHERE questions_on_quiz.question_id = mc_question_correct_answers.question_id and
        questions_on_quiz.quiz_id = 'Pr1-220310';


-- all true-false questions in the quiz and their weights and correct answers

CREATE VIEW tfQuestions as

  SELECT questions_on_quiz.question_id as qid,
         questions_on_quiz.weight,
         correct_answer as tfAnswer
  FROM questions_on_quiz,
       tf_question_correct_answers
  WHERE questions_on_quiz.question_id = tf_question_correct_answers.question_id and
        questions_on_quiz.quiz_id = 'Pr1-220310';



-- all numeric questions in the quiz and their weights and correct answers

CREATE VIEW numQuestions as

  SELECT questions_on_quiz.question_id as qid,
         questions_on_quiz.weight,
         correct_answer as numAnswer
  FROM questions_on_quiz,
       num_question_correct_answers
  WHERE questions_on_quiz.question_id = num_question_correct_answers.question_id and
        questions_on_quiz.quiz_id = 'Pr1-220310';


-- information and total grades of multiple choice questions of students who has at least one correct answer in this part

CREATE VIEW mcStudentsGrade as

  SELECT student_responses_mc.sid,
        sum(weight) as grade
  FROM student_responses_mc,
        mcQuestions,
        classes
  WHERE student_responses_mc.question_id = mcQuestions.qid and
        student_responses_mc.response = mcQuestions.mcAnswer and
        student_responses_mc.quiz_id = 'Pr1-220310' and
        student_responses_mc.cid = classes.cid and
        classes.grade = 8 and
        classes.rid = 120
  GROUP BY student_responses_mc.sid;



-- information and total grades of true-false questions of students who has at least one correct answer in this part

CREATE VIEW tfStudentsGrade as

  SELECT student_responses_tf.sid,
        sum(weight) as grade
  FROM student_responses_tf,
        tfQuestions,
        classes
  WHERE student_responses_tf.question_id = tfQuestions.qid and
        student_responses_tf.response = tfQuestions.tfAnswer and
        student_responses_tf.quiz_id = 'Pr1-220310' and
        student_responses_tf.cid = classes.cid and
        classes.grade = 8 and
        classes.rid = 120
  GROUP BY student_responses_tf.sid;


-- information and total grades of numeric questions of students who has at least one correct answer in this part

CREATE VIEW numStudentsGrade as

  SELECT student_responses_num.sid,
        sum(weight) as grade
  FROM student_responses_num,
        numQuestions,
        classes
  WHERE student_responses_num.question_id = numQuestions.qid and
        student_responses_num.response = numQuestions.numAnswer and
        student_responses_num.quiz_id = 'Pr1-220310' and
        student_responses_num.cid = classes.cid and
        classes.grade = 8 and
        classes.rid = 120
  GROUP BY student_responses_num.sid;


-- students who don't receive zero mark in the quiz and their grades

  CREATE VIEW gradesCombined as
       (SELECT *
       FROM mcStudentsGrade)
         UNION
       (SELECT *
       FROM tfStudentsGrade)
         UNION
       (SELECT *
       FROM numStudentsGrade);

  CREATE VIEW notZeroStudents as
    SELECT sid, sum(grade)
    FROM gradesCombined
    GROUP BY sid;

-- students who receive zero mark

  CREATE VIEW zeroStudents as
  SELECT allQuizStudents.sid, 0 as totalGrade
  FROM allQuizStudents
  WHERE allQuizStudents.sid NOT IN (
    SELECT sid
    FROM notZeroStudents
  );

-- all grades of all students

  CREATE VIEW allStudentGrades as
    (SELECT *
    FROM zeroStudents)
    UNION
    (SELECT *
    FROM notZeroStudents);

-- all grades of students, along with their last names

  CREATE VIEW final as
  SELECT allStudentGrades.sid, allStudentGrades.totalGrade, students.last_name as lastName
  FROM allStudentGrades, students
  WHERE allStudentGrades.sid = students.sid;






-- the answer to the query
insert into q3 (sid ,
                lastName ,
                grade)
(select sid,
        lastName,
        totalGrade
 from final);
