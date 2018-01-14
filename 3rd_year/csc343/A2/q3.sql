-- Participate

SET SEARCH_PATH TO parlgov;
drop table if exists q3 cascade;

-- You must not change this table definition.

create table q3(
countryName VARCHAR(50),
year int,
participationRatio real
);


-- You may find it convenient to do this for each of the views
-- that define your intermediate steps.  (But give them better names!)
DROP VIEW IF EXISTS e15y CASCADE;
DROP VIEW IF EXISTS notNonDecreasings CASCADE;
DROP VIEW IF EXISTS idAndRatios CASCADE;
DROP VIEW IF EXISTS final CASCADE;

-- Define views for your intermediate steps here.

-- country id, year and  average participation rate for each year for countries
-- that has at least one  election for the past 15 years
create view e15y as
  select    country_id as cid,
            avg(votes_cast::float/electorate::float) as participationRatio,
            extract(year from e_date) as year
  from      election
  where     extract(year from e_date) >= 2001 and
            extract(year from e_date) <= 2016
  group by  country_id,
            year,
            electorate
  order by  country_id,
            year;


-- country id of countries whose average election participation ratios
-- during this period are NOT monotonically non-decreasing
create view notNonDecreasings as
  select distinct e1.cid
  from  e15y e1 ,
        e15y e2
  where e1.cid = e2.cid and
        e1.year < e2.year and
        e2.participationRatio < e1.participationRatio;


-- country id, average election participation ratios per year for the countries
-- that meets the criteria(non-decreasing).
create view idAndRatios as
  select e15y.cid,
         e15y.year as year,
         participationRatio
  from e15y
  where not exists (
    select notNonDecreasings.cid
    from   notNonDecreasings
    where  notNonDecreasings.cid = e15y.cid
  );

--country name. average election participation ratios per year for the countries
-- that meets the criteria.

create view final as
  select country.name as name,
         idAndRatios.participationRatio,
         idAndRatios.year
  from   country,
         idAndRatios
  where  country.id = idAndRatios.cid;



-- the answer to the query
insert into q3 (countryName, year, participationRatio)
  (select name,
          year,
          participationRatio
   from   final);
