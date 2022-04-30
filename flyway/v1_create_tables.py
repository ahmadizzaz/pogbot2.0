import sqlite3

dbClient = sqlite3.connect("discord.db")

dbClient.execute('''CREATE TABLE IF NOT EXISTS VALORANT
                    (ID        TEXT   PRIMARY KEY     NOT NULL,
                    NAME       TEXT                   NOT NULL,
                    TAG        TEXT                   NOT NULL,
                    DISCORDID  TEXT                   NOT NULL
                    );''')
dbClient.close()