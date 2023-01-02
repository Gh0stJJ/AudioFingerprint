-- Active: 1636241981621@@localhost@3306@signala
CREATE TABLE fingerprints ( 
     hash binary(10) not null,
     song_id mediumint unsigned not null, 
     offset int unsigned not null, 
     INDEX(hash),
     UNIQUE(song_id, offset, hash)
);

CREATE TABLE songs (
    song_id mediumint unsigned not null auto_increment, 
    song_name varchar(250) not null,
    fingerprinted tinyint default 0,
    PRIMARY KEY (song_id),
    UNIQUE KEY song_id (song_id)
);


