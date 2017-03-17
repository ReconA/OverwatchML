from OwApi import OverwatchApi
import db.Insert as Insert
import Heroes
import JsonParser
from db import BattleTag, Soldier


# Init OverwatchAPI
api = OverwatchApi()

# Iterate through every battle tag
all = BattleTag.select_all_tags()
for player in all:
    tag, region, games =  player[0], player[1], player[2]
    print 'Checking profile of %s' % tag
    # Check if the player has played since the last check
    try:
        profile = api.get_profile(tag)
        current_games = JsonParser.parse_games_played(profile)
    except Exception:
        print 'Skipping tag %s' % tag
        continue 

    # Has not played since the last time we checked, so nothing more to do.
    if current_games == games:
        print "Tag %s does not need updating" % tag
        continue

    # Parse rating for future use.
    rating = JsonParser.parse_rating(profile)

    # Insert
    for hero in Heroes.hero_list.values():
        stats = api.get_hero_stats(tag, hero)
        #print stats
        #Soldier.insert_total(tag, rating, stats)
        Insert.insert_stats(tag, rating, hero, stats)

    # Finally, update the game count
    BattleTag.update_tag(tag, current_games)

