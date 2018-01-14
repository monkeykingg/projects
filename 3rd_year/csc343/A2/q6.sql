-- Sequencabinet_ends

SET SEARCH_PATH TO parlgov;
drop table if exists q6 cascade;

-- You must not change this table definition.

CREATE TABLE q6(
        countryName VARCHAR(50),
        cabinetId INT,
        startDate DATE,
        endDate DATE,
        pmParty VARCHAR(100)
);

-- You may find it convenient to do this for each of the views
-- that define your intermediate steps.  (But give them better names!)
DROP VIEW IF EXISTS cabinet_start CASCADE;
DROP VIEW IF EXISTS cabinet_end CASCADE;
DROP VIEW IF EXISTS current CASCADE;
DROP VIEW IF EXISTS current_cabinet CASCADE;
DROP VIEW IF EXISTS position_prime_minister CASCADE;
DROP VIEW IF EXISTS no_position_prime_minister CASCADE;
DROP VIEW IF EXISTS fit_position_prime_minister CASCADE;
DROP VIEW IF EXISTS fit_no_position_prime_minister CASCADE;
DROP VIEW IF EXISTS cabinet_start_end CASCADE;
DROP VIEW IF EXISTS final CASCADE;

-- Define views for your intermediate steps here.

-- cabinet start date
create view cabinet_start as
select id as cabid,
       country_id as cid,
       start_date as sd,
       name,
       previous_cabinet_id as pcid,
       election_id as eid
from cabinet
order by country_id,
         start_date;

-- cabinet end date, end date is equel to next cabinet start date, use self join to get right end date
create view cabinet_end as
select T1.cabid,
       T1.cid,
       T2.sd as ed,
       T1.name,
       T1.pcid,
       T1.eid
from cabinet_start T1,
     cabinet_start T2
where T2.pcid = T1.cabid
order by cid,
         ed;

-- cabinets do not have end date, which means they are the current cabinet at that country
create view current as
(select cabinet_start.cabid
from cabinet_start)
except
(select cabinet_end.cabid
from cabinet_end);

-- cabinets are the current cabinet at that country
create view current_cabinet as
select current.cabid,
       cid,
       sd,
       name,
       pcid,
       eid
from cabinet_start,
     current
where current.cabid = cabinet_start.cabid
order by cid,
         sd;

-- find the party that fills the position of prime minister
create view position_prime_minister as
select cabinet_id as cabid,
       party.name as pmParty
from cabinet_party,
     party
where cabinet_party.pm = 't' and
      cabinet_party.party_id = party.id;

-- find the party that not fill the position of prime minister, in order to handle null cases
create view no_position_prime_minister as
select cabinet_id as cabid,
       null as pmParty
from cabinet_party
where cabinet_party.pm = 'f';

-- create a suitable view of position_prime_minister with enough columns and info for final union
create view fit_position_prime_minister as
select country.name as countryName,
       current_cabinet.cabid as cabinetId,
       current_cabinet.sd as startDate,
       null as endDate,
       pmParty
from current_cabinet,
     position_prime_minister,
     country
where current_cabinet.cabid = position_prime_minister.cabid and
      current_cabinet.cid = country.id;

-- create a suitable view of no_position_prime_minister with enough columns and info for final union
create view fit_no_position_prime_minister as
select country.name as countryName,
       current_cabinet.cabid as cabinetId,
       current_cabinet.sd as startDate,
       null as endDate,
       pmParty
from current_cabinet,
     no_position_prime_minister,
     country
where current_cabinet.cabid = no_position_prime_minister.cabid and
      current_cabinet.cid = country.id;

-- join start time and end time information, keep those cabinets have no end date as null end date
create view cabinet_start_end as
select country.name as countryName,
       cabinet_start.cabid as cabinetId,
       cabinet_start.sd as startDate,
       ed as endDate,
       pmParty
from cabinet_start,
     cabinet_end,
     position_prime_minister,
     country
where cabinet_start.cabid = cabinet_end.cabid and
      cabinet_start.cabid = position_prime_minister.cabid and
      cabinet_start.cid = country.id;

-- union all views
create view final as
(select * from fit_position_prime_minister)
union
(select * from cabinet_start_end)
union
(select * from fit_no_position_prime_minister);

-- the answer to the query
insert into q6 (countryName,
                cabinetId,
                startDate,
                endDate,
                pmParty)
(select countryName,
        cabinetId,
        startDate,
        endDate,
        pmParty
from final);
