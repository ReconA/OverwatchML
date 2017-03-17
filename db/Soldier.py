import sqlite3
import datetime
import Utils as Utils

columns = ['Eliminations',
          'FinalBlows',
          'SoloKills',
          'CriticalHits',
          'ShotsFired',
          'DamageDone',
          'ObjectiveKills',
          'Multikill',
          'MeleeFinalBlows',
          'Deaths',
          'SelfHealing',
          'HelixRocketsKills',
          'TacticalVisorKills',
          'BioticFieldsDeployed',
          'BioticFieldHealingDone',
          'GamesPlayed',
          'GamesWon',
     ]

count = 0

def create_table() :
    conn = sqlite3.connect('overwatch.db')
    conn.execute(
    '''CREATE TABLE SOLDIER
    (battletag TEXT NOT NULL,
    datetime   TEXT NOT NULL,
    rating INT NOT NULL,
    elims  INT NOT NULL,
    fins   INT NOT NULL,
    solos  INT NOT NULL,
    crits  INT NOT NULL,
    shots  INT NOT NULL,
    damage INT NOT NULL,
    objkills INT NOT NULL,
    multi    INT NOT NULL,
    melee    INT NOT NULL,
    deaths   INT NOT NULL,
    selfheal INT NOT NULL,
    rocketkills INT NOT NULL,
    tacvisorkills INT NOT NULL,
    fields INT NOT NULL,
    fieldheal INT NOT NULL,
    games INT NOT NULL,
    wins INT NOT NULL,
    win INT NOT NULL,
    total INT NOT NULL,
    PRIMARY KEY (battletag, datetime)
    );''')

    print 'Created game table for Soldier'
    conn.close()


def insert_single_game(tag,rating,new_stats):
    # Calculate stats from a single game
    old_stats = select_total(tag)
    stats = calculate_match_stats(tag, rating, new_stats, old_stats)

    # If games played != old games, we know that player played Soldier
    try:
        old_games = old_stats[18]
    except Exception:
        #print 'Defaulting old games to 0'
        old_games = 0

    
    if stats[18] != 0:
        global count 
        count += 1
        print 'Insertion %s' % count
        insert(stats)

    # Must always update the total.
    update_total(tag,rating,new_stats)


# Calculates a single match stats from the old and new totals
def calculate_match_stats(tag, rating, stats, old_stats):
    soldier_stats=stats['Soldier76']
    match_stats = [tag,datetime.datetime.now(),rating or 0]
    i = 3
    
    for s in columns:
        try:
            old_stat = int(old_stats[i])
        except Exception:
            old_stat = 0
        try:
            new_stat = int(Utils.remove_commas(soldier_stats[s]))
        except KeyError:
            new_stat = 0
        match_stats.append(new_stat - old_stat)
        i += 1
    
    # Append win/loss
    try:
        new_wins = int(soldier_stats['GamesWon'])
        print "New wins=%s" % new_wins
    except KeyError:
        print "Default new wins to 0"
        new_wins = 0
    try:
        old_wins = int(old_stats[19])
        print "Old wins=%s" % old_wins
    except Exception:
        print 'Defaulting old wins to 0'
        old_wins = 0
    
    wins = new_wins-old_wins
    print "Wins=%s" % wins
    match_stats.append(wins)

    #This is not total stats
    match_stats.append(0)
    return match_stats


# First time insertion of total stats
def insert_total(tag, rating, stats):
    print "Inserting total Soldier76 stats of tag %s" %tag
    soldier_stats = stats['Soldier76']
    t  = create_column(tag,rating,2,1,soldier_stats)
    insert(t)


def select_total(tag):
    #print "Selecting total Soldier76 stats for tag %s" % tag
    conn = sqlite3.connect('overwatch.db')
    c = conn.cursor()
    rows = c.execute('SELECT * FROM SOLDIER where total=1 AND battletag=?;', (tag,))
    res = rows.fetchone()
    conn.close()
    return res


def select_all_match_stats():
    conn = sqlite3.connect('overwatch.db')
    c = conn.cursor()
    rows = c.execute('SELECT * FROM SOLDIER where total=0;')
    res = rows.fetchall()
    conn.close()
    return res

def delete_total(tag):
    #print "Deleting total Soldier76 stats for tag %s" % tag
    conn = sqlite3.connect('overwatch.db')
    c = conn.cursor()
    c.execute('DELETE FROM SOLDIER where total=1 AND battletag=?;', (tag,))
    conn.commit()
    conn.close()


# Lazy way to update.
def update_total(tag,rating, stats):
    delete_total(tag)
    insert_total(tag, rating, stats)


def drop_table():
    conn = sqlite3.connect('overwatch.db')
    conn.execute("DROP TABLE SOLDIER")
    conn.close()


def insert(t):
    conn = sqlite3.connect('overwatch.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO SOLDIER '
                '(battletag,'
                'datetime,'
                'rating,'
                'elims,'
                'fins,'
                'solos,'
                'crits,'
                'shots,'
                'damage,'
                'objkills,'
                'multi,'
                'melee,'
                'deaths,'
                'selfheal,'
                'rocketkills,'
                'tacvisorkills,'
                'fields,'
                'fieldheal,'
                'games,'
                'wins,'
                'win,'
                'total) '
                'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);',t)
    conn.commit()
    conn.close()


# Create a column from json
# Win: 0=loss, 1=win, 2=this is the total row
def create_column(tag,rating,win,total,stats):
     t = [tag, datetime.datetime.now()]
     t.append(rating or 0)
     for s in columns:
         if s not in stats:
             t.append(0)
         elif s == 'ObjectiveTime' or s == 'TimeSpentonFire':
             t.append(Utils.to_seconds(stats[s]))
         else:
             t.append(Utils.remove_commas(stats[s]))

     t.append(win)
     t.append(total)
     return t
