-- drop previous tables

drop table client cascade;
drop table product cascade;
drop table artist cascade;
drop table scoreboard cascade;

create table client (
    cid SERIAL,
    name varchar(80) not null unique,
    pass varchar(64) not null,
    constraint pk_user primary key(cid)
);

create table artist (
    aid SERIAL,
    name varchar(80) not null unique,
    constraint pk_artist primary key(aid)
);

create table scoreboard (
    aid integer not null,
    amount money not null,
    cid integer not null,
    constraint pk_scoreboard primary key(aid, cid),
    constraint fk_user foreign key(cid) references client(cid),
    constraint fk_artist foreign key(aid) references artist(aid)
);

create table product (
    pid SERIAL,
    name varchar(80) not null unique,
    type varchar(80) not null,
    aid integer not null,
    price money not null,
    constraint pk_product primary key(pid),
    constraint fk_artist foreign key(aid) references artist(aid)
);
