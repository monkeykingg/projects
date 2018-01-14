-- Q1. What constraints from the domian could not be enforced?
-- Answer: Some constraints that relate to "at least". In A3 Part1, the constraint of "a class has one or more students",
-- the constraint of "a multiple choice question has at least two answer options", and the constraint of "a quiz has one or more questions",
-- cannot be enforced. Because that is possible to have a new class with zero students, a new question with no answer added yet, or a new
-- quiz has no question added yet in real life. Also, the constraint of "10-digit number" of students ID is hard to enforce at database.
-- Actually, these constraints can be handled much easier at front-end.
-- And if we try to avoid these at back-end database, what we design (like allow null values) will cause more redundancy.
-- So we made a trade off here.

-- Q2. What constraints that could have been enforced were not enforced? Why not?
-- Answer: For example, we can add "Students can only in six classes at most" and "A room can only contains 200
-- students" constraints. We do not include these constraints because they are not very related to quizschema.

DROP SCHEMA IF EXISTS quizschema CASCADE;
CREATE SCHEMA quizschema;

SET SEARCH_PATH to quizschema;



-- A table of students. Each student has a unique student ID, a first name, and a last name.
CREATE TABLE students(
    -- The student ID (10-digit number) of each student is unique.
    sid VARCHAR(10) PRIMARY KEY,
    -- First and Last name of a student. We think size 60 is large enough to handle special names.
    -- Name should not be null.
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL
);

-- A extra table to show a room can never have more than one teacher.
CREATE TABLE rooms(
    -- The room ID of each room is unique.
    rid INT PRIMARY KEY,
    -- By given examples, we assume the value of attibute "teacher" is char type.
    -- We do not know the max length of input char, so we simply set the limitation to 90.
    teacher VARCHAR(90) NOT NULL
);

-- A table of classes. A class has a room, grade, and a teacher.
CREATE TABLE classes(
    -- The class ID of each class is unique.
    cid INT PRIMARY KEY,
    -- There can be multiple classes for the same grade.
    grade INT NOT NULL,
    -- Here is the important part!
    -- We have a constraint said "a room can have more than one classed in it, but never more than one teacher".
    -- Which give us the clue that we should set a new table to show the relation between room and teacher,
    -- without affecting "a class has a room and a teacher" constraint.
    -- And of cause, rid must form the table "rooms"
    rid INT NOT NULL REFERENCES rooms(rid)
);

-- A table to show a student is in a class.
CREATE TABLE enrollments(
    -- Since not all students are enrolled in a class. Not all classes have enrolled student too.
    -- So, we only record those students who enrolled in a class/classes and those classes have student(s).
    -- Students must from the table "students" and classes must from the table "classes".
    -- To handle "students can enroll in mutiple classes" and "classes can have multiple students" cases,
    -- we create key tuples.
    sid VARCHAR(10) NOT NULL REFERENCES students(sid),
    cid INT NOT NULL REFERENCES classes(cid),
    PRIMARY KEY(sid, cid)
);



-- A table to store all questions and the question texts (i.e. question contents).
CREATE TABLE question_bank(
    -- The question ID of each question is unique.
    question_id INT PRIMARY KEY,
    -- The question text of each question.
    -- We do not know the max length of input char, so we simply set the limitation to 500.
    question_text VARCHAR(500) NOT NULL
);

-- A table to store all correct answers for true-false questions. The correct answers are "true" or "flase".
CREATE TABLE TF_question_correct_answers(
    -- Questions must from the table "question_bank".
    question_id INT PRIMARY KEY REFERENCES question_bank(question_id),
    -- The correct answer of corresponding question.
    -- We do not know the max length of input char ("T" or "true" or "F" or "flase"), so we simply set the limitation to 10.
    correct_answer VARCHAR(10) NOT NULL
);

-- A table to store all correct answers for multiple choice questions. The correct answers are strings.
CREATE TABLE MC_question_correct_answers(
    -- Questions must from the table "question_bank".
    question_id INT PRIMARY KEY REFERENCES question_bank(question_id),
    -- The correct answer of corresponding question.
    -- We do not know the max length of input char, so we simply set the limitation to 500.
    correct_answer VARCHAR(500) NOT NULL
);

-- A table to store all correct answers for numeric questions. The correct answers are integers.
CREATE TABLE NUM_question_correct_answers(
    -- Questions must from the table "question_bank".
    question_id INT PRIMARY KEY REFERENCES question_bank(question_id),
    -- The correct answer of corresponding question.
    correct_answer INT NOT NULL
);


-- A table to store all hints for multiple choice questions.
CREATE TABLE MC_question_hints(
    -- Questions must from the table "question_bank".
    question_id INT NOT NULL REFERENCES question_bank(question_id),
    -- The wrong answer (i.e. wrong choice) of corresponding question.
    -- We do not know the max length of input char, so we simply set the limitation to 500.
    wrong_choice VARCHAR(500) NOT NULL,
    -- The hint of this question.
    hint VARCHAR(500),
    -- To handle "a question can have multiple wrong answers" case, we create key tuples.
    PRIMARY KEY(question_id, wrong_choice)
);

-- A table to store all hints for numeric questions.
CREATE TABLE NUM_question_hints(
    -- Questions must from the table "question_bank".
    question_id INT NOT NULL REFERENCES question_bank(question_id),
    -- The incorrect answer range upper bound.
    upper_bound INT NOT NULL,
    -- The incorrect answer range lower bound.
    lower_bound INT NOT NULL,
    -- The hint of this question.
    hint VARCHAR(500),
    -- To handle "a question can have multiple wrong answers" case, we create key tuples.
    PRIMARY KEY(question_id, upper_bound, lower_bound)
);



-- A table of quizzes. A quiz has a unique ID, a title, a due date and time, and a class to which it is assigned.
-- The instructor can choose whether or not students should be shown a hint during the whole quiz.
-- We consider "a quiz has one or more questions from question bank" in ohter table.
CREATE TABLE quizzes(
    -- The quiz ID of each quiz is unique.
    -- As given example, the quiz ID is "Pr1-220310", so we simply set the limitation to 20.
    quiz_id VARCHAR(20) NOT NULL PRIMARY KEY,
    -- The title of this quiz.
    -- We do not know the max length of input char, so we simply set the limitation to 500.
    title VARCHAR(500) NOT NULL,
    -- The due date of this quiz.
    due_date DATE NOT NULL,
    -- The due time of this quiz.
    due_time TIME NOT NULL,
    -- Hint flag to decide whether or not to show hint.
    hint_flag VARCHAR(10) NOT NULL,
    -- Classes must from the table "classes".
    cid INT NOT NULL REFERENCES classes(cid)
);

-- A extra table to show "a quiz has one or more questions from question bank" and "each question on a quiz has a weight".
CREATE TABLE questions_on_quiz(
    -- Quizzes muct from the table "quizzes" and questions must from the table "question_bank".
    quiz_id VARCHAR(20) NOT NULL REFERENCES quizzes(quiz_id),
    question_id INT NOT NULL REFERENCES question_bank(question_id),
    -- Each question on a quiz has a weight, which is a integer.
    -- Same question can occur in multiple different quizzes with different weights.
    weight INT NOT NULL,
    -- To handle "a quiz has one or more questions from question bank" case, we create key tuples.
    PRIMARY KEY(quiz_id, question_id)
);

-- A table of student multiple choice responses.
-- A student can enroll in multiple classes, attend multiple quizzes, and answer multiple questions.
-- Also, a student may not have answered all questions, even answered none.
-- Only students in the class that assigned a quiz can answer questions on that quiz.
CREATE TABLE student_responses_MC(
    -- The combinations of students and classes must from the table "enrollment".
    sid VARCHAR(10) NOT NULL,
    cid INT NOT NULL,
    FOREIGN KEY (sid, cid) REFERENCES enrollments(sid, cid),
    -- The combinations of quizzes and questions must from the table "questions_on_quiz".
    quiz_id VARCHAR(20) NOT NULL,
    question_id INT NOT NULL,
    FOREIGN KEY (quiz_id, question_id) REFERENCES questions_on_quiz(quiz_id, question_id),
    -- The response answer (i.e. student answer) for the quiz question by this student.
    -- We do not know the max length of input char, so we simply set the limitation to 500.
    response VARCHAR(500) NOT NULL,
    -- To handle "a student can enroll in multiple classes, attend multiple quizzes, and answer multiple questions.
    -- Also, a student may not have answered all questions, even answered none" case, we create key tuples.
    PRIMARY KEY(sid, cid, quiz_id, question_id)
);

-- A table of student true-false responses.
-- A student can enroll in multiple classes, attend multiple quizzes, and answer multiple questions.
-- Also, a student may not have answered all questions, even answered none.
-- Only students in the class that assigned a quiz can answer questions on that quiz.
CREATE TABLE student_responses_TF(
    -- The combinations of students and classes must from the table "enrollment".
    sid VARCHAR(10) NOT NULL,
    cid INT NOT NULL,
    FOREIGN KEY (sid, cid) REFERENCES enrollments(sid, cid),
    -- The combinations of quizzes and questions must from the table "questions_on_quiz".
    quiz_id VARCHAR(20) NOT NULL,
    question_id INT NOT NULL,
    FOREIGN KEY (quiz_id, question_id) REFERENCES questions_on_quiz(quiz_id, question_id),
    -- The response answer (i.e. student answer) for the quiz question by this student.
    -- We do not know the max length of input char, so we simply set the limitation to 500.
    response VARCHAR(10) NOT NULL,
    -- To handle "a student can enroll in multiple classes, attend multiple quizzes, and answer multiple questions.
    -- Also, a student may not have answered all questions, even answered none" case, we create key tuples.
    PRIMARY KEY(sid, cid, quiz_id, question_id)
);

-- A table of student numeric responses.
-- A student can enroll in multiple classes, attend multiple quizzes, and answer multiple questions.
-- Also, a student may not have answered all questions, even answered none.
-- Only students in the class that assigned a quiz can answer questions on that quiz.
CREATE TABLE student_responses_NUM(
    -- The combinations of students and classes must from the table "enrollment".
    sid VARCHAR(10) NOT NULL,
    cid INT NOT NULL,
    FOREIGN KEY (sid, cid) REFERENCES enrollments(sid, cid),
    -- The combinations of quizzes and questions must from the table "questions_on_quiz".
    quiz_id VARCHAR(20) NOT NULL,
    question_id INT NOT NULL,
    FOREIGN KEY (quiz_id, question_id) REFERENCES questions_on_quiz(quiz_id, question_id),
    -- The response answer (i.e. student answer) for the quiz question by this student.
    -- We do not know the max length of input char, so we simply set the limitation to 500.
    response INT NOT NULL,
    -- To handle "a student can enroll in multiple classes, attend multiple quizzes, and answer multiple questions.
    -- Also, a student may not have answered all questions, even answered none" case, we create key tuples.
    PRIMARY KEY(sid, cid, quiz_id, question_id)
);
