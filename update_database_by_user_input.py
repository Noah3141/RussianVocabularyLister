###############################################################################

# Update database with all user inputted words. Run manually periodically.
# Calls database_cleaner to remove Russian spelling rule violating entries, and
# Anything less than 3 characters long (e.g. the single letter bugs)

###############################################################################
def update_database_by_user_input():
    import sys
    import mysql.connector
    from database_cleaner import clean_database
    
    
    with open("backflow_to_database_text.txt", "r", encoding="UTF-8") as f:
        user_text = f.readlines()
    
    backflow_words = []
    for line in user_text[1:]:
        line = line.strip()
        if line.endswith("**"):
            continue
        backflow_words.append(line)
    
    if len(backflow_words) == 0:
        sys.exit()
     
    backflow_words = set(backflow_words) 
    backflow_words = list(backflow_words)
        
     
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "nnssoteck3434###",
        database = "Database_001")
    cursor = conn.cursor()
    
    cursor.execute("SELECT word FROM words")
    db_words = cursor.fetchall()
    
    # Prepare stop words filter
    stop_words = set()
    stop_words_txt = open("stop_words.txt", 'r', encoding='UTF-8')
    for line in stop_words_txt:
        stop_words.add(line.rstrip())
    
    # Make the list of database words from the cursor
    db_list = list()
    for row in db_words:
        word = row[0]
        if word not in stop_words:
            db_list.append(word)
    
    db_list_set = set(db_list)
    
    
    for word in backflow_words:
        
        print("Next word: ", word)
        if word not in db_list_set:
            print("          not found in database. Adding...")
            cursor.execute(f"INSERT INTO words (word) VALUES ('{word}');")
            conn.commit()
        else: 
            continue
        
    
    with open("backflow_to_database_text.txt", "w", encoding="UTF-8") as f:
        f.write("")
        
    cursor.close()
    conn.close() 
    
    clean_database()
        
