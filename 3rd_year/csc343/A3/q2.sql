
--

SET SEARCH_PATH TO quizschema;
drop table if exists q2 cascade;

-- You must not change this table definition.

create table q2(
qid INT,
text VARCHAR(500),
hintNumber INT
);


-- You may find it convenient to do this for each of the views
-- that define your intermediate steps.  (But give them better names!)
DROP VIEW IF EXISTS trueFalseInfo CASCADE;
DROP VIEW IF EXISTS multipleChoiceInfo CASCADE;
DROP VIEW IF EXISTS numericInfo CASCADE;
DROP VIEW IF EXISTS final CASCADE;


-- Define views for your intermediate steps here.

-- information for true-false questions
CREATE VIEW trueFalseInfo as
  SELECT question_bank.question_id as qid,
         question_text as text,
         NULL as count
  FROM question_bank,
       tf_question_correct_answers
  WHERE question_bank.question_id = tf_question_correct_answers.question_id;

-- information for multiple-choice questions
CREATE VIEW multipleChoiceInfo as
  SELECT question_bank.question_id as qid,
         question_text as text,
         count(hint)
  FROM question_bank,
       mc_question_hints
  WHERE question_bank.question_id = mc_question_hints.question_id
  GROUP BY question_bank.question_id,
           question_bank.question_text;


-- information for numeric questions
CREATE VIEW numericInfo as
  SELECT num_question_hints.question_id as qid,
        question_bank.question_text as text,
        count(hint)
  FROM num_question_hints,
       question_bank
  WHERE num_question_hints.question_id = question_bank.question_id
  GROUP BY num_question_hints.question_id,
           question_bank.question_text;

-- information of all questions

CREATE VIEW final as
  (SELECT *
  FROM trueFalseInfo)
  UNION
  (SELECT *
  FROM multipleChoiceInfo)
  UNION
  (SELECT *
  FROM numericInfo);




-- the answer to the query
insert into q2 (qid,
                text,
                hintNumber)
(select qid,
        text,
        count
 from final);
