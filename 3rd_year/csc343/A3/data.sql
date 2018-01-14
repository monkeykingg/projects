INSERT INTO students VALUES
('0998801234', 'Lena', 'Headey'),
('0010784522', 'Peter', 'Dinklage'),
('0997733991', 'Emilia', 'Clarke'),
('5555555555', 'Kit', 'Harrington'),
('1111111111', 'Sophie', 'Turner'),
('2222222222', 'Maisie', 'Williams');

INSERT INTO rooms VALUES
(120, 'Mr Higgins'),
(366, 'Miss Nyers');

INSERT INTO classes VALUES
(001, 8, 120),
(002, 5, 366);

INSERT INTO enrollments VALUES
('0998801234', 001),
('0010784522', 001),
('0997733991', 001),
('5555555555', 001),
('1111111111', 001),
('2222222222', 002);

INSERT INTO question_bank VALUES
(782, 'What do you promise when you take the oath of citizenship?'),
(566, 'The Prime Minister, Justin Trudeau, is Canada''s Head of State.'),
(601, 'During the "Quiet Revolution," Quebec experienced rapid change. In what decade did this occur? (Enter the year that began the decade, e.g., 1840.)'),
(625, 'What is the Underground Railroad?'),
(790, 'During the War of 1812 the Americans burned down the Parliament Buildings in York (now Toronto). What did the British and Canadians do in return?');

INSERT INTO TF_question_correct_answers VALUES
(566, 'False');

INSERT INTO MC_question_correct_answers VALUES
(782, 'To pledge your loyalty to the Sovereign, Queen Elizabeth II'),
(625, 'A network used by slaves who escaped the United States into Canada'),
(790, 'They burned down the White House in Washington D.C.');

INSERT INTO NUM_question_correct_answers VALUES
(601, 1960);

INSERT INTO MC_question_hints VALUES
(782, 'To pledge your allegiance to the flag and fulfill the duties of a Canadian', 'Think regally.'),
(782, 'To pledge your loyalty to Canada from sea to sea', NULL),
(625, 'The first railway to cross Canada', 'The Underground Railroad was generally south to north, not east-west.'),
(625, 'The CPR''s secret railway line', 'The Underground Railroad was secret, but it had nothing to do with trains.'),
(625, 'The TTC subway system', 'The TTC is relatively recent; the Underground Railroad was in operation over 100 years ago.'),
(790, 'They attacked American merchant ships', NULL),
(790, 'They expanded their defence system, including Fort York', NULL),
(790, 'They captured Niagara Falls', NULL);

INSERT INTO NUM_question_hints VALUES
(601, 1900, 1800, 'The Quiet Revolution happened during the 20th Century.'),
(601, 2010, 2000, 'The Quiet Revolution happened some time ago.'),
(601, 3000, 2020, 'The Quiet Revolution has already happened!');

INSERT INTO quizzes VALUES
('Pr1-220310', 'Citizenship Test Practise Questions', '2017-10-01', '01:30 PM', 'True', 001);

INSERT INTO questions_on_quiz VALUES
('Pr1-220310', 601, 2),
('Pr1-220310', 566, 1),
('Pr1-220310', 790, 3),
('Pr1-220310', 625, 2);

INSERT INTO student_responses_MC VALUES
('0998801234', 001, 'Pr1-220310', 790, 'They expanded their defence system, including Fort York'),
('0998801234', 001, 'Pr1-220310', 625, 'A network used by slaves who escaped the United States into Canada'),

('0010784522', 001, 'Pr1-220310', 790, 'They burned down the White House in Washington D.C.'),
('0010784522', 001, 'Pr1-220310', 625, 'A network used by slaves who escaped the United States into Canada'),

('0997733991', 001, 'Pr1-220310', 790, 'They burned down the White House in Washington D.C.'),
('0997733991', 001, 'Pr1-220310', 625, 'The CPR''s secret railway line'),

('5555555555', 001, 'Pr1-220310', 790, 'They captured Niagara Falls');


INSERT INTO student_responses_TF VALUES
('0998801234', 001, 'Pr1-220310', 566, 'False'),

('0010784522', 001, 'Pr1-220310', 566, 'False'),

('0997733991', 001, 'Pr1-220310', 566, 'True'),

('5555555555', 001, 'Pr1-220310', 566, 'False');


INSERT INTO student_responses_NUM VALUES
('0998801234', 001, 'Pr1-220310', 601, 1950),

('0010784522', 001, 'Pr1-220310', 601, 1960),

('0997733991', 001, 'Pr1-220310', 601, 1960);
