-- Alliances

SET SEARCH_PATH TO parlgov;
drop table if exists q7 cascade;

-- You must not change this table definition.

DROP TABLE IF EXISTS q7 CASCADE;
CREATE TABLE q7(
        countryId INT,
        alliedPartyId1 INT,
        alliedPartyId2 INT
);

-- You may find it convenient to do this for each of the views
-- that define your intermediate steps.  (But give them better names!)
DROP VIEW IF EXISTS electionCounts CASCADE;
DROP VIEW IF EXISTS allAlliances CASCADE;
DROP VIEW IF EXISTS allPairs CASCADE;
DROP VIEW IF EXISTS allUniquePairs CASCADE;
DROP VIEW IF EXISTS pairsAndAppearance CASCADE;
DROP VIEW IF EXISTS pairsAndCountries CASCADE;
DROP VIEW IF EXISTS final CASCADE;



-- Define views for your intermediate steps here.


-- election id, country id of all elections, order by country names
create view electionCounts as
select   country_id as cid,
         count(id) as ecount
from     election
group by country_id;

-- all existing alliances
create view allAlliances as
  select distinct alliance_id
  from election_result;


-- all pairs of parties that have been allied together (repeated pairs included)
create view allPairs as
  (select e1.id as id,
          e1.party_id as pid
  from    election_result e1,
          allAlliances
  where   allAlliances.alliance_id = e1.id)

  union

  (select e2.alliance_id as id,
          e2.party_id as pid
  from    election_result e2,
          allAlliances
  where   allAlliances.alliance_id = e2.alliance_id);

-- all pairs parties that have been allied together (not repeated)
create view allUniquePairs as
  select a1.id,
         a1.pid as pid1,
         a2.pid as pid2
  from   allPairs a1,
         allPairs a2
  where  a1.id = a2.id and
         a1.pid < a2.pid;

-- all pairs and their number of times of being allied together

create view pairsAndAppearance as
  select   count(id) as count,
           pid1 ,
           pid2
  from     allUniquePairs
  group by pid1,
           pid2;

-- all pairs and the country id of the countries they are in
create view pairsAndCountries as
  select pid1,
         pid2, count,
         party.country_id as cid
  from   pairsAndAppearance,  party
  where  pid1 = party.id;


-- all pairs who have been allied together in more than 30% of the elections
-- in their countries

create view final as
  select pairsAndCountries.pid1,
         pairsAndCountries.pid2,
         pairsAndCountries.cid
  from   pairsAndCountries,
         electionCounts
  where  pairsAndCountries.cid = electionCounts.cid and
         (pairsAndCountries.count::float)/(electionCounts.ecount::float) > 0.3;

-- the answer to the query
insert into q7 (countryId, alliedPartyId1, alliedPartyId2)
  (select cid,
          pid1,
          pid2
   from   final);
