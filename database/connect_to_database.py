import sqlite3


def connect():
    db = sqlite3.connect("database/database.db")
    db.execute("CREATE TABLE IF NOT EXISTS `guilds` ("
               "`ID` INTEGER , "
               "`guild_id` VARCHAR(99) NOT NULL , "
               "PRIMARY KEY(`ID` AUTOINCREMENT))")

    db.execute("CREATE TABLE IF NOT EXISTS `schools` ("
               "`ID` INTEGER, "
               "`school_name` VARCHAR(99) NOT NULL , "
               "`guild_id` VARCHAR(99) NOT NULL , "
               "PRIMARY KEY(`ID` AUTOINCREMENT))")

    db.execute("CREATE TABLE IF NOT EXISTS `classes` ("
               "`ID` INTEGER, "
               "`class_name` VARCHAR(99) NOT NULL , "
               "`school_name` VARCHAR(99) NOT NULL, "
               "`guild_id` VARCHAR(99) NOT NULL, "
               "PRIMARY KEY(`ID` AUTOINCREMENT))")

    db.execute("CREATE TABLE IF NOT EXISTS `group` ("
               "`ID` INTEGER, "
               "`class_name` VARCHAR(99) NOT NULL , "
               "`keystore` LONGTEXT NOT NULL , "
               "`account` LONGTEXT NOT NULL , "
               "`guild_id` VARCHAR(99) NOT NULL, "
               "PRIMARY KEY(`ID` AUTOINCREMENT))")

    db.execute("CREATE TABLE IF NOT EXISTS `user` ("
               "`ID` INTEGER, "
               "`user_id` VARCHAR(999) NOT NULL , "
               "`class_id` VARCHAR(999) NOT NULL , "
               "`school_id` VARCHAR(999) NOT NULL , "
               "`group_id` VARCHAR(999) NOT NULL , "
               "`guild_id` VARCHAR(99) NOT NULL, "
               "PRIMARY KEY(`ID` AUTOINCREMENT))")
    db.commit()
    return db


cursor = connect()
