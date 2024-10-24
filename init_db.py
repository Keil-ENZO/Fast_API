import sqlite3

connection = sqlite3.connect('database.db')
connection.execute('PRAGMA foreign_keys = ON')

connection.execute("""CREATE TABLE IF NOT EXISTS Article (
                                    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    title VARCHAR(256),
                                    slug VARCHAR(55),
                                    content TEXT,
                                    author VARCHAR(55)
                                );""")

connection.execute("""CREATE TABLE IF NOT EXISTS Comment (
                                    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    author VarChar(256),
                                    content TEXT,
                                    article_id INTEGER,
                                    FOREIGN KEY (article_id) REFERENCES Article(article_id)
                                );""")

connection.commit()
connection.close()