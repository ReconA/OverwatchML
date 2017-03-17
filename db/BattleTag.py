import sqlite3


def create_table() :
    conn = sqlite3.connect('overwatch.db')

    conn.execute(
    '''CREATE TABLE BATTLETAG
    (battletag TEXT PRIMARY KEY NOT NULL,
    region TEXT NOT NULL,
    games INT NOT NULL);''')

    print 'Created table for BattleTags'

    conn.close()


# Insert every mod-th battletag from given file.
def insert_battletags(file_name, mod):
    tag_file = open(file_name, "r")
    i = 0
    for tag in tag_file.readlines():
        if i%mod == 0:
            insert_battletag(tag.replace("\n", "").replace("\r",""), "eu")
        i += 1


def insert_battletag(tag, region):
    print "Inserting tag %s from region %s" % (tag, region)
    conn = sqlite3.connect('overwatch.db')
    c = conn.cursor()
    c.execute('INSERT INTO BATTLETAG (battletag, region, games) VALUES (?,?,?);',((tag), (region), 0,))
    conn.commit()
    conn.close()


def select_all_tags():
    conn = sqlite3.connect('overwatch.db')
    c = conn.cursor()
    rows = c.execute(''' SELECT * FROM BATTLETAG;''')
    res = rows.fetchall()
    conn.close()
    return res


def select_tag(tag):
    print "Selecting tag %s" %tag
    conn = sqlite3.connect('overwatch.db')
    c = conn.cursor()
    rows = c.execute('SELECT * FROM BATTLETAG where battletag=?;', (tag,))
    res = rows.fetchone()
    conn.close()
    return res


def update_tag(tag, games):
    conn = sqlite3.connect('overwatch.db')
    c = conn.cursor()
    c.execute('UPDATE BATTLETAG set games=? where battletag=?', (games,tag))
    conn.commit()
    conn.close()


#Dangerous method...
def drop_table():
    var =  raw_input("Are you sure you want to drop table BATTLETAG? (answer yes to drop)")
    if var != 'yes':
        return
    print "Dropping table BATTLETAG"
    conn = sqlite3.connect('overwatch.db')
    conn.execute('DROP TABLE BATTLETAG;')
    conn.close()
