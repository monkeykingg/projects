SET SEARCH_PATH TO quizschema;
drop table if exists q5 cascade;

CREATE TABLE q5(
        question_id INT,
        num_students_correct INT,
        num_students_wrong INT,
        num_students_no_answer INT
);

DROP VIEW IF EXISTS enrolled_students_with_quiz CASCADE;
DROP VIEW IF EXISTS students_reponses_MC CASCADE;
DROP VIEW IF EXISTS students_reponses_TF CASCADE;
DROP VIEW IF EXISTS students_reponses_NUM CASCADE;
DROP VIEW IF EXISTS correct_students_MC CASCADE;
DROP VIEW IF EXISTS correct_students_TF CASCADE;
DROP VIEW IF EXISTS correct_students_NUM CASCADE;
DROP VIEW IF EXISTS wrong_students_MC CASCADE;
DROP VIEW IF EXISTS wrong_students_TF CASCADE;
DROP VIEW IF EXISTS wrong_students_NUM CASCADE;
DROP VIEW IF EXISTS correct_students CASCADE;
DROP VIEW IF EXISTS wrong_students CASCADE;
DROP VIEW IF EXISTS have_answer_students CASCADE;
DROP VIEW IF EXISTS students_with_quesions_in_quiz CASCADE;
DROP VIEW IF EXISTS no_answer_students CASCADE;
DROP VIEW IF EXISTS correct_counter CASCADE;
DROP VIEW IF EXISTS wrong_counter CASCADE;
DROP VIEW IF EXISTS no_answer_counter CASCADE;
DROP VIEW IF EXISTS final CASCADE;


-- Define views for your intermediate steps here.

-- get all students with the class id they enrolled, the room id of the class, the grade number, the teacher, and the quiz id.
create view enrolled_students_with_quiz as
select enrollments.sid as sid,
       enrollments.cid as cid,
       classes.rid as rid,
       classes.grade as grade,
       rooms.teacher as teacher,
       quizzes.quiz_id as quiz_id
from enrollments,
     classes,
     rooms,
     quizzes
where enrollments.cid = classes.cid and
      classes.rid = rooms.rid and
      quizzes.cid = enrollments.cid;

-- get all students who have MC responses
create view students_reponses_MC as
select enrolled_students_with_quiz.sid as sid,
       enrolled_students_with_quiz.cid as cid,
       enrolled_students_with_quiz.rid as rid,
       enrolled_students_with_quiz.grade as grade,
       enrolled_students_with_quiz.teacher as teacher,
       enrolled_students_with_quiz.quiz_id as quiz_id,

       student_responses_MC.question_id as question_id,
       student_responses_MC.response as response
from enrolled_students_with_quiz,
     student_responses_MC
where enrolled_students_with_quiz.sid = student_responses_MC.sid and
      enrolled_students_with_quiz.cid = student_responses_MC.cid and
      enrolled_students_with_quiz.quiz_id = student_responses_MC.quiz_id;

-- get all students who have TF responses
create view students_reponses_TF as
select enrolled_students_with_quiz.sid as sid,
       enrolled_students_with_quiz.cid as cid,
       enrolled_students_with_quiz.rid as rid,
       enrolled_students_with_quiz.grade as grade,
       enrolled_students_with_quiz.teacher as teacher,
       enrolled_students_with_quiz.quiz_id as quiz_id,

       student_responses_TF.question_id as question_id,
       student_responses_TF.response as response
from enrolled_students_with_quiz,
     student_responses_TF
where enrolled_students_with_quiz.sid = student_responses_TF.sid and
      enrolled_students_with_quiz.cid = student_responses_TF.cid and
      enrolled_students_with_quiz.quiz_id = student_responses_TF.quiz_id;

-- get all students who have NUM responses
create view students_reponses_NUM as
select enrolled_students_with_quiz.sid as sid,
       enrolled_students_with_quiz.cid as cid,
       enrolled_students_with_quiz.rid as rid,
       enrolled_students_with_quiz.grade as grade,
       enrolled_students_with_quiz.teacher as teacher,
       enrolled_students_with_quiz.quiz_id as quiz_id,

       student_responses_NUM.question_id as question_id,
       student_responses_NUM.response as response
from enrolled_students_with_quiz,
     student_responses_NUM
where enrolled_students_with_quiz.sid = student_responses_NUM.sid and
      enrolled_students_with_quiz.cid = student_responses_NUM.cid and
      enrolled_students_with_quiz.quiz_id = student_responses_NUM.quiz_id;

-- get all students who answered MC correctly
create view correct_students_MC as
select students_reponses_MC.question_id as question_id,
       students_reponses_MC.sid as sid
from MC_question_correct_answers,
     students_reponses_MC
where students_reponses_MC.question_id = MC_question_correct_answers.question_id and
      students_reponses_MC.response = MC_question_correct_answers.correct_answer;

-- get all students who answered TF correctly
create view correct_students_TF as
select students_reponses_TF.question_id as question_id,
       students_reponses_TF.sid as sid
from TF_question_correct_answers,
     students_reponses_TF
where students_reponses_TF.question_id = TF_question_correct_answers.question_id and
      students_reponses_TF.response = TF_question_correct_answers.correct_answer;

-- get all students who answered NUM correctly
create view correct_students_NUM as
select students_reponses_NUM.question_id as question_id,
       students_reponses_NUM.sid as sid
from NUM_question_correct_answers,
     students_reponses_NUM
where students_reponses_NUM.question_id = NUM_question_correct_answers.question_id and
      students_reponses_NUM.response = NUM_question_correct_answers.correct_answer;

-- get all students who answered MC incorrectly
create view wrong_students_MC as
select students_reponses_MC.question_id as question_id,
       students_reponses_MC.sid as sid
from MC_question_correct_answers,
     students_reponses_MC
where students_reponses_MC.question_id = MC_question_correct_answers.question_id and
      students_reponses_MC.response != MC_question_correct_answers.correct_answer;

-- get all students who answered TF incorrectly
create view wrong_students_TF as
select students_reponses_TF.question_id as question_id,
       students_reponses_TF.sid as sid
from TF_question_correct_answers,
     students_reponses_TF
where students_reponses_TF.question_id = TF_question_correct_answers.question_id and
      students_reponses_TF.response != TF_question_correct_answers.correct_answer;

-- get all students who answered NUM incorrectly
create view wrong_students_NUM as
select students_reponses_NUM.question_id as question_id,
       students_reponses_NUM.sid as sid
from NUM_question_correct_answers,
     students_reponses_NUM
where students_reponses_NUM.question_id = NUM_question_correct_answers.question_id and
      students_reponses_NUM.response != NUM_question_correct_answers.correct_answer;

-- get all students who answered correctly
create view correct_students as
(select *
from correct_students_MC)
union
(select *
from correct_students_TF)
union
(select *
from correct_students_NUM);

-- get all students who answered incorrectly
create view wrong_students as
(select *
from wrong_students_MC)
union
(select *
from wrong_students_TF)
union
(select *
from wrong_students_NUM);

-- get all students who answered
create view have_answer_students as
(select *
from correct_students)
union
(select *
from wrong_students);

-- create a table with all students with their questions of corresponding quiz
create view students_with_quesions_in_quiz as
select questions_on_quiz.question_id as question_id,
       enrolled_students_with_quiz.sid as sid
from enrolled_students_with_quiz,
     questions_on_quiz
where questions_on_quiz.quiz_id = enrolled_students_with_quiz.quiz_id;

-- get all students who did not answer
create view no_answer_students as
(select *
from students_with_quesions_in_quiz)
except
(select *
from have_answer_students);

-- count the number of correct students for each question
create view correct_counter as
select question_id,
       count(sid) as num_students_correct
from correct_students
group by question_id;

-- count the number of wrong students for each question
create view wrong_counter as
select question_id,
       count(sid) as num_students_wrong
from wrong_students
group by question_id;

-- count the number of no answer students for each question
create view no_answer_counter as
select question_id,
       count(sid) as num_students_no_answer
from no_answer_students
group by question_id;

-- create final table to gather all counted results
create view final as
select *
from correct_counter natural join wrong_counter natural join no_answer_counter;

-- the answer to the query
insert into q5(question_id,
               num_students_correct,
               num_students_wrong,
               num_students_no_answer)
(select question_id,
        num_students_correct,
        num_students_wrong,
        num_students_no_answer
from final);
