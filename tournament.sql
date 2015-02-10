-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table player (
	id	serial,
	name text not null,
	primary key (id)
);

create table game (
	id serial,
	winner integer references player(id) not null,
	loser integer references player(id),
	primary key (id),
	constraint different_players check (winner != loser)
);