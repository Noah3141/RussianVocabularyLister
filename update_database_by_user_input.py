###############################################################################

# Update database with all user inputted words. Run manually periodically.
# Calls database_cleaner to remove Russian spelling rule violating entries, and
# Anything less than 3 characters long (e.g. the single letter bugs)

###############################################################################

import sys
import mysql.connector
from database_cleaner import clean_database


with open("backflow_to_database_text.txt", "r", encoding="UTF-8") as f:
    user_text = f.readlines()

words = []
for line in user_text[1:]:
    line = line.strip()
    if line.endswith("**"):
        continue
    words.append(line)

if len(words) == 0:
    sys.exit()
  
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "nnssoteck3434###",
    database = "Database_001")

cursor = conn.cursor()

for word in words:
    
    print("Next word: ", word)
    cursor.execute(f"SELECT 1 FROM words WHERE word = '{word}'")
    find = cursor.fetchall()
    if len(find) == 0:
        print(word, " not found in database. Adding...")
        cursor.execute(f"INSERT INTO words (word) VALUES ('{word}');")
        conn.commit()
    else: 
        continue
    

with open("backflow_to_database_text.txt", "w", encoding="UTF-8") as f:
    f.write("")
    
cursor.close()
conn.close() 

clean_database()
    
