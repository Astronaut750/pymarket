create table saisonal_M(
stockTicker varchar(50),
year int,
month int,
gain float,
primary key (stockTicker, year, month)
);