-- VoteRange

SET SEARCH_PATH TO parlgov;
drop table if exists q1 cascade;

-- You must not change this table definition.

create table q1(
year INT,
countryName VARCHAR(50),
voteRange VARCHAR(20),
partyName VARCHAR(100)
);


-- You may find it convenient to do this for each of the views
-- that define your intermediate steps.  (But give them better names!)
DROP VIEW IF EXISTS elections_20years CASCADE;
DROP VIEW IF EXISTS elections_20years_partyInfo CASCADE;
DROP VIEW IF EXISTS elections_20years_partyInfo_countryInfo CASCADE;
DROP VIEW IF EXISTS valid_votes CASCADE;
DROP VIEW IF EXISTS numelection CASCADE;
DROP VIEW IF EXISTS single_election CASCADE;
DROP VIEW IF EXISTS multi_election CASCADE;
DROP VIEW IF EXISTS single_election_precentage_20years_partyInfo_countryInfo CASCADE;
DROP VIEW IF EXISTS multi_election_precentage_20years_partyInfo_countryInfo CASCADE;
DROP VIEW IF EXISTS election_precentage_20years_partyInfo_countryInfo CASCADE;
DROP VIEW IF EXISTS range0to5 CASCADE;
DROP VIEW IF EXISTS range5to10 CASCADE;
DROP VIEW IF EXISTS range10to20 CASCADE;
DROP VIEW IF EXISTS range20to30 CASCADE;
DROP VIEW IF EXISTS range30to40 CASCADE;
DROP VIEW IF EXISTS range40to100 CASCADE;
DROP VIEW IF EXISTS final CASCADE;

-- Define views for your intermediate steps here.



-- First, prepare enough information to get to final result

-- elections for 20 years
create view elections_20years as
select id as eid,
       country_id as cid,
       extract(year from e_date) as year
from election
where extract(year from e_date) >= 1996 and
      extract(year from e_date) <= 2016
order by country_id,
         year;

-- elections for 20 years with parties info, ignore no-voting elections
create view elections_20years_partyInfo as
select election_id as eid,
       party_id as pid,
       cid,
       year,
       votes
from elections_20years,
     election_result
where election_id = eid and
      votes > 0;

-- elections for 20 years with parties and countries info
create view elections_20years_partyInfo_countryInfo as
select eid,
       pid,
       cid,
       year,
       votes,
       country.name as countryName,
       party.name_short as partyName
from party,
     country,
     elections_20years_partyInfo
where pid = party.id and
      cid = country_id and
      cid = country.id;



-- Second, solve problem in different parts and merge subresults

-- get valid votes of each election, ignore no vaild vote election
create view valid_votes as
select id as eid,
       country_id as cid,
       votes_valid,
       extract(year from e_date) as year
from election
where extract(year from e_date) >= 1996 and
      extract(year from e_date) <= 2016 and
      votes_valid > 0;

-- count num of election for single/multiple checking
create view numelection as
select count(eid) as num,
       year,
       cid
from elections_20years
group by year,
         cid;

-- if a single election in same year, same country
create view single_election as
select eid,
       pid,
       elections_20years_partyInfo_countryInfo.cid,
       elections_20years_partyInfo_countryInfo.year,
       votes,
       countryName,
       partyName
from numelection,
     elections_20years_partyInfo_countryInfo
where num = 1 and
      numelection.year = elections_20years_partyInfo_countryInfo.year and
      numelection.cid = elections_20years_partyInfo_countryInfo.cid and
      votes > 0;

-- if multiple elections in same year, same country
create view multi_election as
select eid,
       pid,
       elections_20years_partyInfo_countryInfo.cid,
       elections_20years_partyInfo_countryInfo.year,
       votes,
       countryName,
       partyName
from numelection,
     elections_20years_partyInfo_countryInfo
where num > 1 and
      numelection.year = elections_20years_partyInfo_countryInfo.year and
      numelection.cid = elections_20years_partyInfo_countryInfo.cid and
      votes > 0;

-- single election precentage for 20 years with parties and countries info
create view single_election_precentage_20years_partyInfo_countryInfo as
select single_election.year,
       (votes::decimal/votes_valid::decimal) as precentage,
       countryName,
       partyName
from single_election,
     valid_votes
where single_election.eid = valid_votes.eid and
      single_election.cid = valid_votes.cid and
      single_election.year = valid_votes.year;

-- multiple election precentage for 20 years with parties and countries info
create view multi_election_precentage_20years_partyInfo_countryInfo as
select multi_election.year,
       avg(votes::decimal/votes_valid::decimal) as precentage,
       countryName,
       partyName
from multi_election,
     valid_votes
where multi_election.cid = valid_votes.cid and
      multi_election.year = valid_votes.year
group by pid,
         multi_election.year,
         countryName,
         partyName
order by year;


-- union precentages
create view election_precentage_20years_partyInfo_countryInfo as
(select * from single_election_precentage_20years_partyInfo_countryInfo)
union
(select * from multi_election_precentage_20years_partyInfo_countryInfo);



-- try to meet requirements in final solution

-- set different range as requirements
create view range0to5 as
select year,
       precentage,
       countryName,
       partyName,
       '(0-5]'::text as range
from election_precentage_20years_partyInfo_countryInfo
where 0 < precentage and
      precentage <= 0.05;

create view range5to10 as
select year,
       precentage,
       countryName,
       partyName,
       '(5-10]'::text as range
from election_precentage_20years_partyInfo_countryInfo
where 0.05 < precentage and
      precentage <= 0.1;

create view range10to20 as
select year,
       precentage,
       countryName,
       partyName,
       '(10-20]'::text as range
from election_precentage_20years_partyInfo_countryInfo
where 0.1 < precentage and
      precentage <= 0.2;

create view range20to30 as
select year,
       precentage,
       countryName,
       partyName,
       '(20-30]'::text as range
from election_precentage_20years_partyInfo_countryInfo
where 0.2 < precentage and
      precentage <= 0.3;

create view range30to40 as
select year,
       precentage,
       countryName,
       partyName,
       '(30-40]'::text as range
from election_precentage_20years_partyInfo_countryInfo
where 0.3 < precentage and
      precentage <= 0.4;

create view range40to100 as
select year,
       precentage,
       countryName,
       partyName,
       '(40-100]'::text as range
from election_precentage_20years_partyInfo_countryInfo
where 0.4 < precentage and
      precentage <= 1;

-- union ranges for final insertion
create view final as
(select * from range0to5)
union
(select * from range5to10)
union
(select * from range10to20)
union
(select * from range20to30)
union
(select * from range30to40)
union
(select * from range40to100)
order by precentage;



-- the answer to the query
insert into q1 (year,
                countryName,
                voteRange,
                partyName)
(select year,
        countryName,
        range as voteRange,
        partyName
 from final);
 
