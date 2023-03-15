###############################################################################

# This script is run as an admin on a PC for creating updated .pkl files.
# Those .pkl files can then be pushed to the GIT repository, for use in the site.

# This file pulls the database, and creates a .pkl file, to push to GIT.

###############################################################################
###############################################################################

#  #  #  #  #  #  #  #  #  #  #   WARNING  #  #  #  #   #  #  #  #   #  #  #  #
#                   RESETS USER UPDATES TO SCRIPT OUTPUT                      #                           
###############################################################################
###############################################################################



import mysql.connector
import pickle


conn = mysql.connector.connect(
    host = "192.168.1.200", # IP Address of server computer
    user = "distant_user", # User defined in mySQL workbench as being able to have any IP
    password = "distance_connect",
    database = "Database_001")

cursor = conn.cursor()
print("Connected to database!")


word_list = list()
###############################################################################



ывать_trns_endings = ["ывать", "ываю","ываешь","ывает","ываем","ываете","ывают",
                    "ывал", "ывало","ывала","ывали",
                    "ывая", "ывай", "ывайте"]

ать_trns_endings = ["ать", "аю","аешь","ает","аем","аете","ают",
                    "ал", "ало","ала","али",
                    "ая", "ай", "айте"]


spelling_rule_1_letters = ["г", "к", "х"]
spelling_rule_2_letters = ["ж", "ч", "ш", "щ"]


mutation_key = {"пл":"п",
                "бл":"б",
                "фл":"ф",
                "вл":"в",
                "мл":"м",
                "ч":"к", # MISSING Т
                "ж":"з", # MISSING Д and Г
                "ш":"с", # MISSING Х
                "щ":"ст"}# MISSING СК



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
    print(f'{word} checked for {ending_list} reached {match}')
    #print("Match calculated for", word, "against", ending_list, "as", match)
    return match  


prefix_list = ["при", "у", "пере", "от", "об", "объ", "отъ", "вы", "на","с",
               "воз","вос", "вс", "вз", "под", "раз", "про","пре","до",
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
    root = "*"
    print("\n\nRoot_Match checking word", word)
    for prefix in prefix_list:
        if word.startswith(prefix):
            root = word[len(prefix):]
            print("proposed root", root)
            break
    if root == "*":
        print(word, "this word didn't have any endings found!")
    return root


###############################################################################
print("Inputting data from database...")
cursor.execute("SELECT word FROM words")
words = cursor.fetchall()

    
    
for row in words:
    word = row[0]
    word = word.replace("'","")
    word_list.append(word)


cursor.close()
conn.close()   


delete_words = ("пять","девять","десять","вспять","зять","память")
for word in delete_words:
    if word in word_list:
        word_list.remove(word)
 
print("Word List Ready...")
###############################################################################


# Making pair list
####################   
pair_list = dict() # Not calling a "dictionary" because the relationship between key and value is not any sort of change. Key and values are just pairs, arranged in a list


for word in word_list:
    if len(word) <= 6: continue
    
    if word.endswith("ивать"): #Must check for possible stem's consonant mutations
        stem = word[:len(word)-len("ивать")]
        
        
        # Catch consonant mutations in stem
        if any(stem.endswith(mutation) for mutation in mutation_key):
            for mutation in mutation_key:
                if stem.endswith(mutation):
                    stem = stem[:len(stem)-len(mutation)] + mutation_key[mutation]
                    break
        
        
        if len(stem) <= 2:
            pair_list[word] = stem + "ить"
            continue
        
        # Catch о > а mutations in stem
        if stem[-2] == "а": # Check to see if the stem has an "а", if so, check if an "о" replacement exists (e.g. отговорить when analyzing отговаривать), IF it exists, you may assume отговорить instead of отговарить
            if (stem[:len(stem)-2] + "о" + stem[len(stem)-1] + "ить") in word_list:
                stem = stem[:len(stem)-2] + "о" + stem[len(stem)-1]

       
        
        
        if stem[-1] in (spelling_rule_1_letters or spelling_rule_2_letters):
            pair_list[word] = stem + "ать"
        else:
            pair_list[word] = stem + "ить"

    






    elif word.endswith("ывать"): #Must check for shortlist -ы- infix words, and shortlist -вать words -- exceptions.
        stem = word[:len(word)-len("ывать")]
        
        
        
        # Catch consonant mutations in stem
        if any(stem.endswith(mutation) for mutation in mutation_key):
            for mutation in mutation_key:
                if stem.endswith(mutation):
                    stem = stem[:len(stem)-len(mutation)] + mutation_key[mutation]
                    break
        
        
        
        # Catch о > а mutations in stem
        
        if stem[-2] == "а":
            if (stem[:len(stem)-2] + "о" + stem[len(stem)-1] + "ать") in word_list:
                stem = stem[:len(stem)-2] + "о" + stem[len(stem)-1]
        
        pair_list[word] = stem + "ать"
    
    
    
    
    
    elif word.endswith("ять"):
        stem = word[:len(word)-len("ять")]
        
        # Catch consonant mutations in stem
        if any(stem.endswith(mutation) for mutation in mutation_key):
            for mutation in mutation_key:
                if stem.endswith(mutation):
                    stem = stem[:len(stem)-len(mutation)] + mutation_key[mutation]
                    break
        
        # Catch о > а mutations in stem
        try:
            if stem[-2] == "а": # Check to see if the stem has an "а", if so, check if an "о" replacement exists (e.g. отговорить when analyzing отговаривать), IF it exists, you may assume отговорить instead of отговарить
                if (stem[:len(stem)-2] + "о" + stem[len(stem)-1] + "ить") in word_list:
                    stem = stem[:len(stem)-2] + "о" + stem[len(stem)-1]
        except:
            pair_list[stem + "инать"] = word
            try:
                del pair_list[word]
                continue
            except: continue
            
        pair_list[word] = stem + "ить"

    # # откинуть - откидать, отряхнуть - отрясать
    # elif word.endswith("нуть"):
    #     russ_match("")
        

    
    # elif russ_match(word, ывать_trns_endings) > 4:
    #     for ending in ывать_trns_endings:
    #         if word.endswith(ending):
    #             stem = word[:len(word)-len(ending)]
    #             dict_form = stem + "ывать"    
    #             break
    #     pair_list[dict_form] = stem + "ать"
    
    # Before adding these blocks in, finished the above
        

   

    




# Overrides:
############  


# Override all prefixed forms

override_list = {"калывать":"колоть","крывать":"крыть",
                 "кладывать":"ложить", "рывать":"рвать","мирать":"мереть", "бирать": "брать",
                 "секать":"сечь", "зывать":"звать", "бывать":"быть", "ращивать":"расти", 
                 "плывать":"плыть","мывать":"мыть"}
# Our pair list is arranged as imperfective:perfective. We catch verb pairs from the database
# by catching the imperfective (almost always -ывать/-ивать). A handful of verbs
# end in these endings in the imperfective, but their perfective form ends in a non-routine
# form, e.g. откалывать - отколоть. 

for override in override_list: # For each imperfective form, tied to a perfective override
    for entry in [entry for entry in pair_list if root_match(entry) == override]:
        pair_list[entry] = (entry[:len(entry)-len(override)] + override_list[override])
    
# For each pair we made up above, look at the imperfective, and remove the prefix,
# Does this form now look like the override's imperfective? If so, we found one
# of the pairs for which we should: set the perfective of that 'entry' equal to
# the entry's prefix + the corresponding perfective tied to the given 
# imperfective, from the override list. 
# e.g. We find скрывать, it matches крывать, therefore с- + крыть is its REAL perfective.
    
 
    
# These words got caught by their PERFECTIVE, and so this block does the converse
# of the above.

нятьs = [word for word in pair_list if root_match(word) == "нять"]
for нять_word in нятьs:    
    del pair_list[нять_word]
    pair_list[(нять_word[:len(нять_word)-4] + "нимать")] = нять_word
    

# The above overrides rely on being able to peel out a root from prefixes.
# If a found entry is completely unprefixed, it needs different processing:
unprefixed_override_list = {"бывать":"быть", "брать":"взять", "учитывать":"учесть"}
for override in unprefixed_override_list:
    pair_list[override] = unprefixed_override_list[override]



# Certain prefixes naturally gain a vowel to prevent consonant clusters.
# When an imperfective is converted to its perfective form, consonant arrangements
# Can change in a subset of verbs, causing the vowel to appear, e.g. -рывать -рвать
# Fixing consonant cluster mistakes
clusters = {"отрв":"оторв","разрв":"разорв","обрв":"оборв"}

for word in pair_list:
    for cluster in clusters:
        if cluster in pair_list[word]:
            mismade_word = pair_list[word]
            pair_list[word] = mismade_word.replace(cluster, clusters[cluster])
# If you find "отрв" in the perfective of a pair (that is, the one we generated,
# not the one we found naturalistically), take that word and replace the cluster
# with the corresponding fix.


    
# Making tree list
####################   

roots = list()
tree_list = dict()
prefixes = dict() 

# # Find Roots
for word in pair_list:
    roots.append(root_match(word))

    
       
# Find prefixes those roots go with   
 
# Tree List = tree_list{ Root Space Form : prefixes{ "-Branch Imperfective Stem" : "prefix- prefix- prefix-" }  }
for root in roots:
    for prefix in prefix_list:
        if prefix + root in pair_list:
            if prefix not in prefixes.get(root,""):
                prefixes[root] = prefixes.get(root,"") + "  " + prefix + "-"
    
for word in pair_list:
   root = root_match(word)
   tree_list[root_match(pair_list[word])] = ("-" + root, prefixes.get(root, "")) 

 

# Tree list overrides:
    
tree_overrides = {"имать":"-ять"}
for imperfective in tree_overrides:
    tree_list[imperfective] = [tree_overrides[imperfective] ,  (prefixes.get(root, "")) ]

   
###############################################################################    
    

pair_list = {v: k for k, v in pair_list.items()}

with open("pair_list.pkl", "wb") as f:
    pickle.dump(pair_list, f)


with open("tree_list.pkl", "wb") as f:
    pickle.dump(tree_list, f)


