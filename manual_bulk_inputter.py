# Used for inputting the "related words" sections in Викисловарь in order to
# cause a word to proc properly to form a tree

import mysql.connector

with open("manual_add_words.txt", encoding="UTF-8") as f:
    line = f.read()
    
manual_words = line.split(", ")



     
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "nnssoteck3434###",
    database = "Database_001")

cursor = conn.cursor()


cursor.execute("SELECT word FROM words")
words = cursor.fetchall()


stop_words = set()
stop_words_txt = open("stop_words.txt", 'r', encoding='UTF-8')
for line in stop_words_txt:
    stop_words.add(line.rstrip())

word_list = list()  
for row in words:
    word = row[0]
    if word not in stop_words:
        word_list.append(word)

word_list_set = set(word_list)

for word in manual_words:
    
    print("Next word: ", word)
    if word not in word_list_set:
        print(word, " not found in database. Adding...")
        cursor.execute(f"INSERT INTO words (word) VALUES ('{word}');")
        #conn.commit()
    else: 
        continue
    
    
cursor.close()
conn.close() 