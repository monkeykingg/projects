-- Winners

SET SEARCH_PATH TO parlgov;
drop table if exists q2 cascade;

-- You must not change this table definition.

create table q2(
countryName VARCHaR(100),
partyName VARCHaR(100),
partyFamily VARCHaR(100),
wonElections INT,
mostRecentlyWonElectionId INT,
mostRecentlyWonElectionYear INT
);


-- You may find it convenient to do this for each of the views
-- that define your intermediate steps.  (But give them better names!)
DROP VIEW IF EXISTS winnersvotes CASCADE;
DROP VIEW IF EXISTS winner CASCADE;
DROP VIEW IF EXISTS winners_electionInfo_partyInfo_countryInfo_year_votes CASCADE;
DROP VIEW IF EXISTS num_party_country CASCADE;
DROP VIEW IF EXISTS num_winner_party_country CASCADE;
DROP VIEW IF EXISTS average CASCADE;
DROP VIEW IF EXISTS winparty CASCADE;
DROP VIEW IF EXISTS connect CASCADE;
DROP VIEW IF EXISTS morethan3 CASCADE;
DROP VIEW IF EXISTS recent_won_year CASCADE;
DROP VIEW IF EXISTS recent_won_election_year CASCADE;
DROP VIEW IF EXISTS recent_won_election_year_wonElections CASCADE;
DROP VIEW IF EXISTS recent_won_election_year_wonElections_country_family CASCADE;

-- Define views for your intermediate steps here.

-- find those winners'(i.e. the most) votes for each election
create view winnersvotes as
select election_id as eid,
       MAX(votes) as votes
from election_result
group by election_id
order by election_id;

-- connect the winner votes with other winner information
create view winners as
select election_id as eid,
       party_id as pid,
       winnersvotes.votes
from election_result,
     winnersvotes
where election_result.votes = winnersvotes.votes and
      election_result.election_id = winnersvotes.eid
order by election_id;

-- winners with election id, party id, country id, year and votes info
create view winners_electionInfo_partyInfo_countryInfo_year_votes as
select eid,
       pid,
       party.country_id as cid,
       extract(year from e_date) as year,
       votes
from winners,
     party,
     election
where party.id = pid and
      election.id = eid
order by eid;


-- number of party in a counrty in general
create view num_party_country as
select country_id as cid,
       count(id) as party_num
from party
group by country_id;

-- number of winner party in a country
create view num_winner_party_country as
select count(pid) as winner_num,
       cid
from winners_electionInfo_partyInfo_countryInfo_year_votes
group by cid
order by cid;

-- compute average number of elections
create view average as
select num_winner_party_country.cid,
       winner_num::decimal/party_num::decimal as ave
from num_winner_party_country,
     num_party_country
where num_winner_party_country.cid = num_party_country.cid;


-- winner party with counrty info, number of wins
create view winparty as
select cid,
       pid,
       count(eid) as winnum
from winners_electionInfo_partyInfo_countryInfo_year_votes
group by cid,
         pid
order by cid;

-- connect average and winner party for next step
create view connect as
select average.cid,
       pid,
       winnum,
       ave
from average,
     winparty
where average.cid = winparty.cid;

-- compare winner to average and find the number of wins is 3 time average
create view morethan3 as
select cid,
       pid,
       winnum as wonElections
from connect
where winnum > 3 * ave;


-- recent won year
create view recent_won_year as
select winners_electionInfo_partyInfo_countryInfo_year_votes.pid as pid,
       winners_electionInfo_partyInfo_countryInfo_year_votes.cid as cid,
       MAX(year) as year
from winners_electionInfo_partyInfo_countryInfo_year_votes,
     morethan3
where winners_electionInfo_partyInfo_countryInfo_year_votes.pid = morethan3.pid and
      winners_electionInfo_partyInfo_countryInfo_year_votes.cid = morethan3.cid
group by winners_electionInfo_partyInfo_countryInfo_year_votes.pid,
         winners_electionInfo_partyInfo_countryInfo_year_votes.cid
order by cid;

-- recent won year and election
create view recent_won_election_year as
select distinct winners_electionInfo_partyInfo_countryInfo_year_votes.eid as eid,
       recent_won_year.pid as pid,
       recent_won_year.cid as cid,
       recent_won_year.year as year
from winners_electionInfo_partyInfo_countryInfo_year_votes,
     recent_won_year
where winners_electionInfo_partyInfo_countryInfo_year_votes.pid = recent_won_year.pid and
      winners_electionInfo_partyInfo_countryInfo_year_votes.cid = recent_won_year.cid and
      winners_electionInfo_partyInfo_countryInfo_year_votes.year = recent_won_year.year
order by cid;

-- recent won election and year with wonElections
create view recent_won_election_year_wonElections as
select eid,
       recent_won_election_year.pid,
       recent_won_election_year.cid,
       year,
       wonElections
from recent_won_election_year,
     morethan3
where recent_won_election_year.pid = morethan3.pid and
      recent_won_election_year.cid = morethan3.cid;

-- recent won election and year with country name
create view recent_won_election_year_wonElections_country as
select eid,
       pid,
       cid,
       year,
       wonElections,
       country.name as countryName
from recent_won_election_year_wonElections,
     country
where country.id = recent_won_election_year_wonElections.cid;

-- recent won election and year with country and party and family name
create view recent_won_election_year_wonElections_country_family as
select eid,
       pid,
       cid,
       year,
       wonElections,
       countryName,
       party.name as partyName,
       family as partyFamily
from recent_won_election_year_wonElections_country,
     party left join party_family on party.id = party_id
where party.id = recent_won_election_year_wonElections_country.pid
order by pid;

-- the answer to the query
insert into q2 (countryName,
                partyName,
                partyFamily,
                wonElections,
                mostRecentlyWonElectionId,
                mostRecentlyWonElectionYear)
(select countryName,
        partyName,
        partyFamily,
        wonElections,
        eid as mostRecentlyWonElectionId,
        year as mostRecentlyWonElectionYear
from recent_won_election_year_wonElections_country_family);
