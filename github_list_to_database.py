
import mysql.connector

with open("lemma by gengel.txt", "r", encoding="UTF-8") as f:
    lemmas = f.readlines()

add_words = []
for line in lemmas:
    cols = line.split()
    
    if cols[3] == "verb" or cols[3] == "noun" or cols[3] == "adj":
        add_words.append(cols[2])
    
    else:
        continue
    pass


conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "nnssoteck3434###",
    database = "Database_001")

cursor = conn.cursor()

for word in add_words:
    
    print("Next word: ", word)
    cursor.execute(f"SELECT 1 FROM words WHERE word = '{word}'")
    find = cursor.fetchall()
    if len(find) == 0:
        print(word, " not found in database. Adding...")
        cursor.execute(f"INSERT INTO words (word) VALUES ('{word}');")
        conn.commit()
    else: 
        continue
    

cursor.close()
conn.close() 

