import sqlite3
import random

def readSong(timeSig):
  file = None
  try:
    file = sqlite3.connect('ReggaeRun.db')
    cs = file.cursor()
    fetchQuery = """SELECT blob_data FROM music_table where time_signature = ?"""
    cs.execute(fetchQuery, (timeSig,))
    record = cs.fetchall()
    #randomly selects a song
    song = random.choice(record)

    #writes the blob data of the random song to the file
    blob = song[0]
    writeSong(blob)
    cs.close()
  except sqlite3.Error as error:
    print(error)
  finally:
    if file:
        file.close()

def writeSong(blob):
  if blob:
    with open('currentSong.mp3', 'wb') as file:
      file.write(blob)

readSong("4/4")

