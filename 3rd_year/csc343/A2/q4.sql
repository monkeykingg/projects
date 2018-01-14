-- Left-right

SET SEARCH_PATH TO parlgov;
drop table if exists q4 cascade;

-- You must not change this table definition.


CREATE TABLE q4(
        countryName VARCHAR(50),
        r0_2 INT,
        r2_4 INT,
        r4_6 INT,
        r6_8 INT,
        r8_10 INT
);

-- You may find it convenient to do this for each of the views
-- that define your intermediate steps.  (But give them better names!)
DROP VIEW IF EXISTS party_position_country CASCADE;
DROP VIEW IF EXISTS count0to2 CASCADE;
DROP VIEW IF EXISTS count2to4 CASCADE;
DROP VIEW IF EXISTS count4to6 CASCADE;
DROP VIEW IF EXISTS count6to8 CASCADE;
DROP VIEW IF EXISTS count8to10 CASCADE;

-- Define views for your intermediate steps here.

-- party positions with country name
create view party_position_country as
select party_id as pid,
       country.name as countryName,
       left_right
from party_position,
     party,
     country
where party.id = party_id and
      country.id = country_id;

-- count number of parties that have position in the given range
create view count0to2 as
select count(pid) as r0_2,
       countryName
from party_position_country
where left_right >= 0 and
      left_right < 2
group by countryName;

create view count2to4 as
select count(pid) as r2_4,
       countryName
from party_position_country
where left_right >= 2 and
      left_right < 4
group by countryName;

create view count4to6 as
select count(pid) as r4_6,
       countryName
from party_position_country
where left_right >= 4 and
      left_right < 6
group by countryName;

create view count6to8 as
select count(pid) as r6_8,
       countryName
from party_position_country
where left_right >= 6 and
      left_right < 8
group by countryName;

create view count8to10 as
select count(pid) as r8_10,
       countryName
from party_position_country
where left_right >= 8 and
      left_right < 10
group by countryName;


-- the answer to the query
INSERT INTO q4 (countryName,
                r0_2,
                r2_4,
                r4_6,
                r6_8,
                r8_10)
(select countryName,
        r0_2,
        r2_4,
        r4_6,
        r6_8,
        r8_10
from count0to2 natural join
     count2to4 natural join
     count4to6 natural join
     count6to8 natural join
     count8to10);
