import sqlite3
import datetime
import Utils as Utils

columns = ['ScopedHits',
           'ScopedShots',
           'NanoBoostsApplied',
           'NanoBoostAssists',
           'Eliminations',
           'FinalBlows',
           'SoloKills',
           'ShotsFired',
           'ShotsHit',
           'DamageDone',
           'ObjectiveKills',
           'MeleeFinalBlows',
           'HealingDone',
           'OffensiveAssists',
           'SelfHealing',
           'Deaths',
           'UnscopedShots',
           'UnscopedHits',
           'EnemiesSlept',
           'TimeSpentonFire',
           'ObjectiveTime',
           'DefensiveAssists',
           'GamesPlayed',
           'GamesWon'
           ]

games_won_idx = 26

def create_table():
    conn = sqlite3.connect('overwatch.db')
    conn.execute(
    '''CREATE TABLE ANA
    (battletag TEXT NOT NULL,
    datetime   TEXT NOT NULL,
    rating INT NOT NULL,
    scoped_hits INT NOT NULL,
    scoped_shots INT NOT NULL,
    nano_boosts INT NOT NULL,
    nano_assists INT NOT NULL,
    elims INT NOT NULL,
    fins INT NOT NULL,
    solos INT NOT NULL,
    shots INT NOT NULL,
    hits INT NOT NULL,
    damage INT NOT NULL,
    obj_kills INT NOT NULL,
    melee INT NOT NULL,
    heal INT NOT NULL,
    off_assists INT NOT NULL,
    self_heal INT NOT NULL,
    deaths INT NOT NULL,
    unscoped_shots INT NOT NULL,
    unscoped_hits INT NOT NULL,
    slept INT NOT NULL,
    fire INT NOT NULL,
    obj_time INT NOT NULL,
    def_assist INT NOT NULL,
    games INT NOT NULL,
    wins INT NOT NULL,
    win INT NOT NULL,
    total INT NOT NULL,
    PRIMARY KEY (battletag, datetime)
    );''')

    print 'Created game table for Ana'
    conn.close()


def drop_table():
    conn = sqlite3.connect('overwatch.db')
    conn.execute("DROP TABLE ANA")
    conn.close()


def insert_single_game(tag,rating,new_stats):
    # Calculate stats from a single game
    old_stats = select_total(tag)
    stats = calculate_match_stats(tag, rating, new_stats, old_stats)

    # If games played != old games, we know that player played Soldier
    if stats[15] != old_stats[15]:
        insert(stats)

    # Must always update the total.
    update_total(tag,rating,new_stats)


def insert_total(tag, rating, stats):
    print "Inserting total Ana stats"
    ana_stats = stats['Ana']
    t  = create_column(tag,rating,2,1,ana_stats)
    insert(t)


# Calculates a single match stats from the old and new totals
def calculate_match_stats(tag, rating, stats, old_stats):
    new_stats=stats['Ana']
    match_stats = [tag,datetime.datetime.now(),rating]
    print old_stats
    i = 3
    for s in columns:
        if s == 'ObjectiveTime' or s == 'TimeSpentonFire':
            match_stats.append(int(Utils.to_seconds(new_stats[s])) - int(old_stats[i]))
        else:
            match_stats.append(int(Utils.remove_commas(new_stats[s])) - int(old_stats[i]))
        i += 1

    # Append win/loss
    new_wins = int(new_stats['GamesWon'])
    old_wins = int(old_stats[games_won_idx])
    print "old_wins %s" %old_wins
    print "new_wins %s" %new_wins
    if new_wins > old_wins:
        match_stats.append(1)
    else:
        match_stats.append(0)
    # This is not total stats
    match_stats.append(0)
    print match_stats
    return match_stats


def select_total(tag):
    print "Selecting total Soldier76 stats for tag %s" % tag
    conn = sqlite3.connect('overwatch.db')
    c = conn.cursor()
    rows = c.execute('SELECT * FROM ANA where total=1 AND battletag=?;', (tag,))
    res = rows.fetchone()
    conn.close()
    return res


def delete_total(tag):
    print "Deleting total Ana stats for tag %s" % tag
    conn = sqlite3.connect('overwatch.db')
    c = conn.cursor()
    c.execute('DELETE FROM ANA where total=1 AND battletag=?;', (tag,))
    conn.commit()
    conn.close()


# Lazy way to update.
def update_total(tag,rating, stats):
    delete_total(tag)
    insert_total(tag, rating, stats)


def insert(t):
    conn = sqlite3.connect('overwatch.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO ANA VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);',t)
    conn.commit()
    conn.close()

# Create a column from json
# Win: 0=loss, 1=win, 2=this is the total row
def create_column(tag,rating,win,total,stats):
        t  = [tag, datetime.datetime.now(), rating]

        for s in columns :
            if s == 'ObjectiveTime' or s == 'TimeSpentonFire':
                t.append(Utils.to_seconds(stats[s]))
            else:
                t.append(Utils.remove_commas(stats[s]))

        t.append(win)
        t.append(total)
        return  t
