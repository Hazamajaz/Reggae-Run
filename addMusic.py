import sqlite3

def insertMusic(blob, timeSig):
  file = None
  try:
    file = sqlite3.connect('ReggaeRun.db')
    insertQuery = '''INSERT INTO music_table(blob_data, time_signature)
      VALUES(?, ?)'''
    cs = file.cursor()
    cs.execute(insertQuery, (blob, timeSig, ))
    file.commit()
    lastEntry = cs.lastrowid
    return lastEntry
  except sqlite3.Error as e:
    print(e)
  finally:
    if file:
      file.close()

def convertToBinary(filePath):
  with open(filePath, 'rb') as file:
    binary = file.read()
  return binary

# blob = convertToBinary("Audio Files/12-8Song2.mp3")
# timeSig = "12/8"
# insertMusic(blob, timeSig)


  