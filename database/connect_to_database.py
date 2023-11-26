import sqlite3


def connect():
    with sqlite3.connect("database/database.db") as db:
        db.execute("CREATE TABLE IF NOT EXISTS `guilds` ("
                   "`ID` INTEGER , "
                   "`guild_id` VARCHAR(99) NOT NULL , "
                   "PRIMARY KEY(`ID` AUTOINCREMENT))")

        db.execute("CREATE TABLE IF NOT EXISTS `schools` ("
                   "`ID` INTEGER, "
                   "`school_name` VARCHAR(99) NOT NULL , "
                   "`guild_id` VARCHAR(99) NOT NULL ,"
                   "`lucky_number` VARCHAR(99) NOT NULL,"
                   "PRIMARY KEY(`ID` AUTOINCREMENT))")

        db.execute("CREATE TABLE IF NOT EXISTS `classes` ("
                   "`ID` INTEGER, "
                   "`school_name` VARCHAR(99) NOT NULL, "
                   "`class_name` VARCHAR(99) NOT NULL , "
                   "`guild_id` VARCHAR(99) NOT NULL, "
                   "PRIMARY KEY(`ID` AUTOINCREMENT))")

        db.execute("CREATE TABLE IF NOT EXISTS `group` ("
                   "`ID` INTEGER, "
                   "`school_name` VARCHAR(99) NOT NULL, "
                   "`class_name` VARCHAR(99) NOT NULL , "
                   "`group_name` VARCHAR(99) NOT NULL , "
                   "`keystore` TEXT NOT NULL , "
                   "`account` TEXT NOT NULL , "
                   "`guild_id` VARCHAR(99) NOT NULL, "
                   "`user_vulcan` VARCHAR(99) NOT NULL, "
                   "`channel_id` VARCHAR(99) NOT NULL, "
                   "`role_id` INT DEFAULT 0,"
                   "PRIMARY KEY(`ID` AUTOINCREMENT))")

        db.execute("CREATE TABLE IF NOT EXISTS `user` ("
                   "`ID` INTEGER, "
                   "`user_id` VARCHAR(999) NOT NULL , "
                   "`class_name` VARCHAR(999) NOT NULL , "
                   "`school_name` VARCHAR(999) NOT NULL , "
                   "`group_name` VARCHAR(999) NOT NULL , "
                   "`guild_id` VARCHAR(99) NOT NULL, "
                   "`number` VARCHAR(99) NOT NULL, "
                   "`exams_ids` TEXT,"
                   "PRIMARY KEY(`ID` AUTOINCREMENT))")

        db.execute("CREATE TABLE IF NOT EXISTS `exams` ("
                   "`ID` INTEGER NOT NULL, "
                   "`exam_id` INTEGER NOT NULL, "
                   "`group_id` INTEGER NOT NULL, "
                   "`message_id` INTEGER NOT NULL, "
                   "`date_modified` VARCHAR(999) NOT NULL, "
                   "`deadline` VARCHAR(999) NOT NULL,"
                   "`removed` INTEGER NOT NULL, "
                   " PRIMARY KEY(`ID` AUTOINCREMENT), "
                   "FOREIGN KEY(group_id) REFERENCES 'group'(ID))")

        db.execute("CREATE TABLE IF NOT EXISTS `messages` ("
                   "`ID` INTEGER NOT NULL, "
                   "`msg_id` VARCHAR(999) NOT NULL, "
                   "`group_id` INTEGER NOT NULL, "
                   "`message_id` INTEGER NOT NULL, "
                   " PRIMARY KEY(`ID` AUTOINCREMENT), "
                   "FOREIGN KEY(group_id) REFERENCES 'group'(ID))")

        db.execute("CREATE TABLE IF NOT EXISTS `views` ("
                   "`ID` INTEGER NOT NULL, "
                   "`message_id` INT NOT NULL, "
                   " PRIMARY KEY(`ID` AUTOINCREMENT)) ")

        db.execute("CREATE TABLE IF NOT EXISTS `homework` ("
                   "`ID` INTEGER NOT NULL, "
                   "`homework_id` INTEGER NOT NULL, "
                   "`group_id` INTEGER NOT NULL, "
                   "`message_id` INTEGER NOT NULL, "
                   "`deadline` VARCHAR(999) NOT NULL,"
                   "`removed` INTEGER NOT NULL, "
                   " PRIMARY KEY(`ID` AUTOINCREMENT), "
                   "FOREIGN KEY(group_id) REFERENCES 'group'(ID))")
        db.commit()
