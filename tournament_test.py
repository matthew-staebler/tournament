#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *
from collections import Counter

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deleteTournaments()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deleteTournaments()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deleteTournaments()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deleteTournaments()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."
    
    
def testCreateTournament():
    deleteMatches()
    deleteTournaments()
    deletePlayers()
    tournament_id = createTournament("tournament1")
    if tournament_id < 0:
        raise ValueError("Tournament not created with valid ID.")
    print "6. Tournaments can be created."


def testStandingsBeforeMatches():
    deleteMatches()
    deleteTournaments()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    tournament_id = createTournament("tournament1")
    standings = playerStandings(tournament_id)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 5:
        raise ValueError("Each playerStandings row should have five columns.")
    [(id1, name1, wins1, ties1, matches1), (id2, name2, wins2, ties2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0 or ties1 != 0 or ties2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "7. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deleteTournaments()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    tournament_id = createTournament("tournament1")
    standings = playerStandings(tournament_id)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournament_id, id1, id2, id1)
    reportMatch(tournament_id, id3, id4, id3)
    standings = playerStandings(tournament_id)
    for (i, n, w, t, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
        if t != 0:
            raise ValueError("There should not be any ties.")
    print "8. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deleteTournaments()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    tournament_id = createTournament("tournament1")
    standings = playerStandings(tournament_id)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournament_id, id1, id2, id1)
    reportMatch(tournament_id, id3, id4, id3)
    pairings = swissPairings(tournament_id)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "9. After one match, players with one win are paired."


def testReportBye():
    deleteMatches()
    deleteTournaments()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    registerPlayer("Evelyn Smith")
    tournament_id = createTournament("tournament1")
    standings = playerStandings(tournament_id)
    [id1, id2, id3, id4, id5] = [row[0] for row in standings]
    reportMatch(tournament_id, id1, id2, id1)
    reportMatch(tournament_id, id3, id4, id3)
    reportMatch(tournament_id, id5, None, id5)
    standings = playerStandings(tournament_id)
    for (i, n, w, t, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3, id5) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
        if t != 0:
            raise ValueError("There should not be any ties.")
    print "10. After matches with byes, players have updated standings."


def testPairingsWithByes():
    deleteMatches()
    deleteTournaments()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Cheerio")
    tournament_id = createTournament("tournament1")
    [id1, id2, id3, id4, id5] = [row[0] for row in playerStandings(tournament_id)]
    reportMatch(tournament_id, id1, id2, id1)
    reportMatch(tournament_id, id3, id4, id3)
    reportMatch(tournament_id, id5, None, id5)
    pairings = swissPairings(tournament_id)
    correct_pairs = [[1L, 1L], [1L, 0L], [0L]]
    actual_pairs = []
    standings = playerStandings(tournament_id)
    for (pid1, pname1, pid2, pname2) in pairings:
        if pid2 == None and pid1 == id5:
            raise ValueError("Player should only be given one bye.")
        if pid1 == pid2:
            raise ValueError("Player should not be matched up against herself.")
        actual_pairs.append([w for (i, n, w, t, m) in standings if i==pid1 or i==pid2])
    if Counter([str(p) for p in correct_pairs]) != Counter([str(p) for p in actual_pairs]):
        raise ValueError(
            "After one match, players should be matched to nearest-win competitor.")
    print "11. After one match with byes, players are paired appropriately."


def testReportMatchesWithTies():
    deleteMatches()
    deleteTournaments()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    tournament_id = createTournament("tournament1")
    standings = playerStandings(tournament_id)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournament_id, id1, id2, id1)
    reportMatch(tournament_id, id3, id4, None)
    standings = playerStandings(tournament_id)
    for (i, n, w, t, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1,) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id3, id4) and w != 0:
            raise ValueError("Each match non-winner should have zero wins recorded.")
        if i in (id1, id2) and t != 0:
            raise ValueError("Each match winner and loser should have zero ties recorded.")
        elif i in (id3, id4) and t != 1:
            raise ValueError("Each tying player should have one tie recorded.")
    print "12. After a match with ties, players have updated standings."


def testPairingsWithTies():
    deleteMatches()
    deleteTournaments()
    deletePlayers()
    for i in range(0,6):
        registerPlayer("player" + str(i))
    tournament_id = createTournament("tournament1")
    ids = [row[0] for row in playerStandings(tournament_id)]
    reportMatch(tournament_id, ids[0], ids[1], ids[0])
    reportMatch(tournament_id, ids[2], ids[3], ids[2])
    reportMatch(tournament_id, ids[4], ids[5], None)
    pairings = swissPairings(tournament_id)
    correct_pairs = [[(1L, 0L), (1L, 0L)], [(0L, 1L), (0L, 1L)], [(0L, 0L), (0L, 0L)]]
    actual_pairs = []
    standings = playerStandings(tournament_id)
    for (pid1, pname1, pid2, pname2) in pairings:
        if pid1 == pid2:
            raise ValueError("Player should not be matched up against herself.")
        actual_pairs.append([(w, t) for (i, n, w, t, m) in standings if i==pid1 or i==pid2])
    if Counter([str(p) for p in correct_pairs]) != Counter([str(p) for p in actual_pairs]):
        raise ValueError(
            "After one match, players should be matched to nearest-win competitor.")
    print "13. After one match with ties, players are paired appropriately."


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testCreateTournament()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testReportBye()
    testPairingsWithByes()
    testReportMatchesWithTies()
    testPairingsWithTies()
    print "Success!  All tests pass!"


