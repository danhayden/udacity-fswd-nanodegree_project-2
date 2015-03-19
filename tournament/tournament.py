#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import bleach
import psycopg2


def connect():
    ''' Connect to the PostgreSQL database.  Returns a database connection. '''
    return psycopg2.connect("dbname=tournament")


def db_query(query, params=False):
    '''
    Helper function for queries that do not need to return anything

    Args:
      query: the sql statement to be excuted
      params: the parameters of the query
    '''
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()


def db_select_one(query, params=False):
    '''
    Helper function for queries that return one result

    Args:
      query: the sql statement to be excuted
      params: the parameters of the query

    Returns:
      The first value of the first row returned from the query.
    '''
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchone()[0]
    conn.close()

    return result


def db_select_all(query, params=False):
    '''
    Helper function for queries that return a set of results

    Args:
      query: the sql statement to be excuted
      params: the parameters of the query

    Returns:
      A list of tuples, All rows returned from the query.
    '''
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, params)
    results = cur.fetchall()
    conn.close()

    return results


def deleteMatches():
    ''' Remove all the match records from the database. '''
    db_query("DELETE FROM match;")


def deletePlayers():
    ''' Remove all the player records from the database. '''
    db_query("DELETE FROM player;")


def countPlayers():
    ''' Returns the number of players currently registered. '''
    return db_select_one("SELECT COUNT(*) FROM player;")


def registerPlayer(name):
    '''
    Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    '''
    clean_name = bleach.clean(name)
    db_query("insert into player (player_name) values (%s);", (clean_name,))


def playerStandings():
    '''
    Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    '''
    return db_select_all("SELECT * FROM standings;")


def reportMatch(winner, loser):
    '''
    Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    '''
    db_query("INSERT INTO match (winner, loser) VALUES (%s, %s)",
             (winner, loser))


def swissPairings():
    '''
    Returns a list of pairs of players for the next round of a match.

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
    '''
    standings = db_select_all("SELECT * FROM standings;")
    num_players = len(standings)
    pairings = []

    for player in range(0, num_players, 2):
        pair = ((standings[player][0], standings[player][1],
                standings[player + 1][0], standings[player + 1][1]))
        pairings.append(pair)

    return pairings
