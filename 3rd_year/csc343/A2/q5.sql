-- Committed

SET SEARCH_PATH TO parlgov;
drop table if exists q5 cascade;

-- You must not change this table definition.

CREATE TABLE q5(
        countryName VARCHAR(50),
        partyName VARCHAR(100),
        partyFamily VARCHAR(50),
        stateMarket REAL
);

-- You may find it convenient to do this for each of the views
-- that define your intermediate steps.  (But give them better names!)
DROP VIEW IF EXISTS countriesAndCounts CASCADE;
DROP VIEW IF EXISTS partiesAndCounts CASCADE;
DROP VIEW IF EXISTS committedPartiesId CASCADE;
DROP VIEW IF EXISTS withCountryNames CASCADE;
DROP VIEW IF EXISTS withPartyNames CASCADE;
DROP VIEW IF EXISTS noFamilyParties CASCADE;
DROP VIEW IF EXISTS withPartyFamilies CASCADE;
DROP VIEW IF EXISTS allParties CASCADE;
DROP VIEW IF EXISTS final CASCADE;


-- Define views for your intermediate steps here.

-- all countries and their number of cabinets

create view countriesAndCounts as
select count(id) as count, country_id as cid
from cabinet
group by country_id;

-- all parties, their country ids and the number of their cabinets they've joined
create view partiesAndCounts as
select country_id as cid, party_id as pid, count(cabinet_id) as count
from party, cabinet_party
where party_id = party.id
group by country_id, party_id;

-- the party id of the parties that are in all cabinets
create view committedPartiesId as
select partiesAndCOunts.cid, partiesAndCounts.pid
from partiesAndCounts, countriesAndCounts
where partiesAndCounts.count = countriesAndCounts.count and
countriesAndCounts.cid = partiesAndCOunts.cid;

-- the country name of the countries of the committed parties

create view withCountryNames as
select id as cid, pid, name as countryName
from country, committedPartiesId
where cid = id;

-- the name of the committed parties added

create view withPartyNames as
select withCountryNames.cid, pid, countryName, name as partyName
from party, withCountryNames
where id = pid;

-- the party families of the committed parties

create view noFamilyParties as
select *
from withPartyNames
where pid not in (
select pid
from party_family
);

create view withPartyFamilies as
select withPartyNames.cid, withPartyNames.pid, withPartyNames.countryName, withPartyNames.partyName, party_family.family
from withPartyNames, party_family
where withPartyNames.pid = party_family.party_id;

create view allParties as
(select cid, pid, countryName, partyName, family as partyFamily from withPartyFamilies)
union
(select cid, pid, countryName, partyName, cast(NULL as VARCHAR) as partyFamily from noFamilyParties);

create view final as
select countryName, partyName, partyFamily, state_market as stateMarket
from allParties, party_position
where allParties.pid = party_position.party_id;



-- the answer to the query
insert into q5(countryName, partyName, partyFamily, stateMarket)
(select countryName, partyName, partyFamily, stateMarket from final);
