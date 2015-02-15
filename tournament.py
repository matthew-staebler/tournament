#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    try:
        cursor = connection.cursor()
        cursor.execute("delete from game_result;")
        cursor.execute("delete from game;")
        connection.commit()
    finally:
        connection.close()


def deleteTournaments():
    """Remove all the tournament records from the database."""
    connection = connect()
    try:
        cursor = connection.cursor()
        cursor.execute("delete from tournament;")
        connection.commit()
    finally:
        connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    try:
        cursor = connection.cursor()
        cursor.execute("delete from player;")
        connection.commit()
    finally:
        connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    try:
        cursor = connection.cursor()
        cursor.execute("select count(*) from player;")
        return cursor.fetchone()[0]
    finally:
        connection.close()


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    try:
        cursor = connection.cursor()
        cursor.execute("insert into player (name) values(%s);", (name,))
        connection.commit()
    finally:
        connection.close()
        
        
def createTournament(name):
    """Adds a tournament to the tournament database.
    
    The database assigns a unique serial id number for the tournament.
    
    Args:
      name: the name of the tournament (need not be unique)
      
    Return:
      ID of the created tournament
    """
    connection = connect()
    try:
        cursor = connection.cursor()
        cursor.execute("insert into tournament (name) values(%s) returning id;", (name,))
        tournament_id = cursor.fetchone()[0]
        connection.commit()
        return tournament_id
    finally:
        connection.close()


def playerStandings(tournament):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, ties, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        ties: the number of matches the player has tied
        matches: the number of matches the player has played
    """
    connection = connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            select player_id, player_name, wins, ties, games
            from player_record
			where tournament_id=%s
            """,
            (tournament,))
        return cursor.fetchall();
    finally:
        connection.close()
    


def reportMatch(tournament, player1, player2, winner):
    """Records the outcome of a single match between two players.

    Args:
      tournament: the id of the tournament to which the match belongs
      player1:  the id number of the first player
      player2:  the id number of the second player; or None if this is a bye for the first player
      winner: the id number of the winning player. This must be either (1) player1 or player2,
              in the case of a winner or (2) None in the case of a tie.
    """
    connection = connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            insert into game (tournament_id, player1, player2)
            values(%(tournament)s, %(player1)s, %(player2)s)
            returning id;
            """,
            {'tournament': tournament, 'player1': player1, 'player2': player2})
        game_id = cursor.fetchone()[0]
        if winner:
            cursor.execute(
                """
                insert into game_result (game_id, winner)
                values(%(game_id)s, %(winner)s);
                """,
                {'game_id': game_id, 'winner': winner})
        connection.commit()
    finally:
        connection.close()
 
 
def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    
    Args:
      tournament: the id of the tournament for which to generate pairings
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id; or None if this is a bye for the first player
        name2: the second player's name; or None if this is a bye for the first player
    """
    connection = connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            select p.player_id, p.player_name, p.byes
            from player_record p, opponent_record o
			where p.tournament_id=%s and p.tournament_id=o.tournament_id and p.player_id=o.player_id
            order by p.wins, p.losses desc, o.wins, o.losses desc
            """,
            (tournament,))
        rows = cursor.fetchall();
        matches = [];
        bye_needed = len(rows) % 2 != 0
        match = ()
        for row in rows:
            if bye_needed and row[2]==0:
                matches.append(row[0:2] + (None, None))
                bye_needed = False
            else:
                match += row[0:2]
                if len(match) == 4:
                    matches.append(match)
                    match = ()
        return matches
    finally:
        connection.close()


