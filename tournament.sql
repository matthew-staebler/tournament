-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table player (
	id serial,
	name text not null,
	primary key (id)
);

create table tournament (
	id serial,
	name text not null,
	primary key (id)
);

create table game (
	id serial,
	tournament_id integer references tournament(id) not null,
	player1 integer references player(id) not null,
	player2 integer references player(id),
	primary key (id),
	constraint different_players check (player1!=player2)
);

create table game_result (
	game_id integer references game(id) not null,
	winner integer references player(id) not null
);

create view player_record as
	select t.id as tournament_id,
		p.id as player_id,
		p.name as player_name,
		count(g.*) as games,
		count(w.*) as wins,
		count(l.*) as losses,
		count(g.*)-(count(w.*)+count(l.*)) as ties,
		count(b.*) as byes
	from tournament t
		cross join player p
		left join game g on g.tournament_id=t.id and p.id in (g.player1, g.player2)
		left join game_result w on w.game_id=g.id and w.winner=p.id
		left join game_result l on l.game_id=g.id and l.winner!=p.id
		left join game b on b.id=g.id and b.player2 is null
	group by t.id, p.id;

create view opponent_record as
	select t.id as tournament_id,
		p.id as player_id,
		sum(o.wins) as wins,
		sum(o.losses) as losses,
		sum(o.ties) as ties
	from tournament t
		cross join player p
		left join game g on g.tournament_id=t.id and p.id in (g.player1, g.player2)
		left join player_record o on o.tournament_id=t.id and o.player_id=case when p.id=g.player1 then g.player2 else g.player1 end
	group by t.id, p.id;