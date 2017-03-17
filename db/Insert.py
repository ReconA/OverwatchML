# Insert operations
import sqlite3
import Soldier
import Ana


def insert_stats(tag,rating,hero, stats):
    if hero == "Soldier76":
        Soldier.insert_single_game(tag, rating, stats)
    elif hero == "Ana":
        Ana.insert_single_game(tag, rating, stats)