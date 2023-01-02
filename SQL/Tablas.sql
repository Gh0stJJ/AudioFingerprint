CREATE DATABASE `fingerprint`;

USE `fingerprint`;

CREATE TABLE songs (
    song_id integer unsigned not null auto_increment, 
    song_name varchar(250) not null,
    interprete varchar(250) not null,
    fingerprinted boolean default 0,
    PRIMARY KEY (song_id)
);

CREATE TABLE fingerprints ( 
    hash varchar(40) not null,
    song_id integer unsigned not null, 
    offset integer unsigned not null,
    INDEX(hash),
    UNIQUE(song_id, hash, offset),
    FOREIGN KEY (song_id) REFERENCES songs(song_id)
);