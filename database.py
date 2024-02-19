from sqlite3 import *
def CreateDatabase():
  file = connect("ReggaeRun.db")
  cs = file.cursor()

  # enforces referential integrity
  cs.execute("PRAGMA foreign_keys = ON")

  cs.execute("""DROP TABLE music_table""")

  # create a table
  # adding NOT NULL to fields that must not be left blank
  # music table
  cs.execute("""CREATE TABLE IF NOT EXISTS music_table
      (blob_data TEXT NOT NULL, time_signature TEXT NOT NULL)
      """)

  # user table
  cs.execute("""CREATE TABLE IF NOT EXISTS user_table
      (username TEXT NOT NULL PRIMARY KEY,
      password TEXT NOT NULL, firstname TEXT NOT NULL, 
      surname TEXT NOT NULL, form TEXT NOT NULL)  
      """)

  # user score table
  cs.execute("""CREATE TABLE IF NOT EXISTS user_score_table
      (username TEXT NOT NULL, date INTEGER NOT NULL, time INTEGER NOT NULL, score INTEGER NOT NULL,
      CONSTRAINT composite PRIMARY KEY (username, date, time), FOREIGN KEY (username) REFERENCES user_table(username))  
      """)

  # answer category table
  cs.execute("""CREATE TABLE IF NOT EXISTS 
      answer_category_table (username TEXT NOT NULL, time_signature INTEGER NOT NULL, 
      correct INTEGER, incorrect INTEGER, CONSTRAINT composite PRIMARY KEY (username, time_signature), 
      FOREIGN KEY (username) REFERENCES user_table(username))
      """)

  file.commit()
  file.close()


CreateDatabase()