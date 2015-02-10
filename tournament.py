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
        cursor.execute("delete from game;")
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


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            select p.id, p.name, count(w.*), count(m.*)
            from player p
                left join game w on w.winner = p.id
                left join game m on (m.winner = p.id or m.loser = p.id)
            group by p.id
            """)
        return cursor.fetchall();
    finally:
        connection.close()
    


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    try:
        cursor = connection.cursor()
        cursor.execute("insert into game (winner, loser) values(%(winner)s, %(loser)s);",
            {'winner': winner, 'loser': loser});
        connection.commit()
    finally:
        connection.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    connection = connect()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            select p.id, p.name
            from player p
                left join game w on w.winner = p.id
            group by p.id
            order by count(w.*) desc
            """)
        rows = cursor.fetchall();
        return [rows[i] + rows[i+1] for i in range(len(rows)) if i%2==0]
    finally:
        connection.close()


