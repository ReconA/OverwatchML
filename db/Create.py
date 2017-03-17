# Create DB tables for all heroes.

import sqlite3


# Overall notes:
# win column: 0 means loss/draw, 1 is win.
# total column: holds the total stats of a battletag. Needed for calculating single match results.
# Every hero has 2 tables:
#   Table for individual game stats
#   Table for total stats per battle tag.
# The second table is needed to calculate values for the first table.






# Soldier

# Soldier
def createAnaTable() :
    conn = sqlite3.connect('overwatch.db')
    conn.execute(
    '''CREATE TABLE ANA
    (battletag TEXT NOT NULL,
    datetime   TEXT NOT NULL,
    elims  INT NOT NULL,
    fins   INT NOT NULL,
    solos  INT NOT NULL,
    crits  INT NOT NULL,
    shots  INT NOT NULL,
    damage INT NOT NULL,
    objkills INT NOT NULL,
    multi    INT NOT NULL,
    melee    INT NOT NULL,
    critacc  REAL NOT NULL,
    acc      REAL NOT NULL,
    deaths   INT NOT NULL,
    selfheal INT NOT NULL,
    rocketkills INT NOT NULL,
    tacvisorkills INT NOT NULL,
    fields INT NOT NULL,
    fieldheal INT NOT NULL,
    win INT NOT NULL,
    PRIMARY KEY (battletag, datetime)
    );''')

    print 'Created table for Ana'

    conn.close()