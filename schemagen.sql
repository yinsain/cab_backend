PRAGMA foreign_keys=OFF;

drop table if exists users_login;
drop table if exists users_meta;
drop table if exists rider;
drop table if exists ride_meta;
drop table if exists traveller;

BEGIN TRANSACTION;

CREATE TABLE users_login(
uid integer not null unique primary key,
name text not null unique,
password text not null
);

CREATE TABLE users_meta(
uid integer not null unique primary key,
email text not null unique,
phone_no text not null unique,
name text not null,
id_proof text not null unique,
subs text not null unique,
folls text not null unique,
blist text not null unique,
rating integer not null
);

CREATE TABLE ride_meta(
  ride_id integer not null unique primary key,
  loc_source text not null,
  loc_dest text not null,
  date_c text not null,
  stops text,
  status integer not null,
  traverllerid text not null
);

CREATE TABLE rider(
  car_model text not null unique,
  no_of_seats integer not null,
  avlbl_seats integer not null,
  rating integer not null,
  rides_given integer not null
);

CREATE TABLE traveller(
  blocking_list text not null,
  rating integer not null,
  rides_taken integer not null,
  pref text not null
);
COMMIT;
