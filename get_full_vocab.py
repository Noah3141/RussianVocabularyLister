import mysql.connector
import pickle


conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "nnssoteck3434###",
    database = "Database_001")

cursor = conn.cursor()
print("Connected to database!")


word_list = list()
###############################################################################



ывать_trns_endings = ["ывать", "ываю","ываешь","ывает","ываем","ываете","ывают",
                    "ывал", "ывало","ывала","ывали",
                    "ывая", "ывай", "ывайте"]










###############################################################################


def russ_match(word: str, ending_list: list) -> int:
    match = 0
    if any(word.endswith(ending) for ending in ending_list):
        match = 1
        for ending in ending_list:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                for other_ending in (e for e in ending_list if e != ending):
                    if stem + other_ending in word_list:
                        match += 1
                break
    print(word, ending_list, match)
    #print("Match calculated for", word, "against", ending_list, "as", match)
    return match  


prefix_list = ["при", "у", "пере", "от", "об", "объ", "отъ", "вы", "на","с",
               "воз","вос", "вс", "вз", "под", "раз", "про","до",
               "за","рас","по", "в"] 

# под  -   по
# со   -   с
# вы   -   в
# вос/воз -  во, в
# вс - в
# от    -  о
#
# 
# подставлять - *дставлять
# отворить - *ворить


def root_match(word):
    root = "default"
    print("\n\nChecking word", word)
    for prefix in prefix_list:
        if word.startswith(prefix):
            root = word[len(prefix):]
            print("proposed root", root)
            break
    if root == "default":
        print(word, "this word didn't have any endings found!")
    return root


###############################################################################
print("Inputting data from database...")
cursor.execute("SELECT id, word, frequency FROM words")
words = cursor.fetchall()

# Words is a list of tuples, each tuple: [0 - id, 1 - word, 2 - freq]
# for row in words:
#     id_  = row[0]
#     word = row[1]
#     freq = row[2]
    
    
for row in words:
    word = row[1]
    word = word.replace("'","")
    word_list.append(word)


cursor.close()
conn.close()    
 

###############################################################################


# Making pair list
####################   
pair_list= {} # Not calling a "dictionary" because the relationship between key and value is not any sort of change. Key and values are just pairs, arranged in a list


for word in word_list[:250000]:
    if word.endswith("ивать"): #Must check for possible stem's consonant mutations
        
        pair_list[word] = word[:len(word)-len("ивать")] + "ить"

    elif word.endswith("ывать"): #Must check for shortlist -ы- infix words, and shortlist -вать words -- exceptions.
        pair_list[word] = word[:len(word)-len("ывать")] + "ать"
    
    elif word.endswith("ять"):
        pair_list[word] = word[:len(word)-len("ять")] + "ить"
    
    elif russ_match(word, ывать_trns_endings) > 4:
        for ending in ывать_trns_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                dict_form = stem + "ывать"    
                break
        pair_list[dict_form] = stem + "ать"
        

    
# Overrides:
override_list = {"калывать":"колоть", "говаривать": "говорить","крывать":"крыть",
                 "кладывать":"класть", "рывать":"рвать","мирать":"мереть", "бирать": "брать",
                 "секать":"сечь"}
    
for override in override_list:
    for entry in [entry for entry in pair_list if root_match(entry) == override]:
        pair_list[entry] = (entry[:len(entry)-len(override)] + override_list[override])
    
    
# Making tree list
####################   

root_list = list()
tree_list = {}

# # Find Roots
for word in pair_list:
    root_list.append(root_match(word))

    
       
# Find prefixes those roots go with   
prefixes = dict()  

for root in root_list:
    for prefix in prefix_list:
        if prefix + root in pair_list:
            if prefix not in prefixes.get(root,""):
                prefixes[root] = prefixes.get(root,"") + "  " + prefix + "-"
    
for word in pair_list:
   root = root_match(word)
   tree_list[root_match(pair_list[word])] = ("-" + root, prefixes.get(root, "")) 

    
###############################################################################    
    

with open("pair_list.pkl", "wb") as f:
    pickle.dump(pair_list, f)


with open("tree_list.pkl", "wb") as f:
    pickle.dump(tree_list, f)


