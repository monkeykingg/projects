
-- StudentInfo

SET SEARCH_PATH TO quizschema;
drop table if exists q1 cascade;

-- You must not change this table definition.

create table q1(
studentNumber VARCHAR(100),
fullName VARCHAR(100)
);


-- You may find it convenient to do this for each of the views
-- that define your intermediate steps.  (But give them better names!)
DROP VIEW IF EXISTS final CASCADE;



-- Define views for your intermediate steps here.

-- full name and student number of students
CREATE VIEW final as
  SELECT sid as studentNumber,
         CONCAT(first_name, ' ', last_name) as fullName
  FROM students;

-- the answer to the query
insert into q1 (studentNumber,
                fullName)
(select studentNumber,
        fullName
 from final);
 
