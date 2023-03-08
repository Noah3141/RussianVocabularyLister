import mysql.connector
import pickle


conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "nnssoteck3434###",
    database = "Database_001")

cursor = conn.cursor()
print("Connected to database!")

cursor.execute("""CREATE TABLE IF NOT EXISTS nouns (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    word varchar(32) NOT NULL, 
    frequency INT,
    ending_list varchar(16),
    gender ENUM('masculine', 'feminine', 'neuter'),
    dict_id INT
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS adjectives (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    word varchar(64) NOT NULL, 
    frequency INT,
    ending_list varchar(16),
    gender ENUM('masculine', 'feminine', 'neuter', 'plural'),
    dict_id INT
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS verbs (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    word varchar(64) NOT NULL, 
    frequency INT,
    ending_list varchar(16),
    aspect ENUM('perfective', 'imperfective'),
    pair_id INT,
    tree_id INT,
    prefix  VARCHAR(6),
    dict_id INT
    )""")

###############################################################################

 
masc_hard_endings_all =        ["ы", "а", "у", "е", "ом", "ах", "ами", "ов", "ам","и","ей", ""]
masc_hard_endings_default =    ["ы", "а", "у", "е", "ом", "ах", "ами", "ов", "ам", ""]    
masc_hard_endings_spelling_1 = ["и", "а", "у", "е", "ом", "ах", "ами", "ов", "ам", ""]
masc_hard_endings_spelling_2 = ["и", "а", "у", "е", "ом", "ах", "ами", "ей", "ам", ""]

fem_hard_endings_all =        ["а", "ы","у","е","ам","ой","ами","ах","и","ей","", "ою"]
fem_hard_endings_default =    ["а", "ы","у","е","ам","ой","ами","ах","", "ою"]
fem_hard_endings_spelling_1 = ["а", "и","у","е","ам","ой","ами","ах","", "ою"]
fem_hard_endings_spelling_2 = ["а", "и","у","е","ам","ой","ами","ах","", "ою"]
fem_hard_endings_unstressed = ["а", "и","у","е","ам","ей","ами","ах",""]

neuter_hard_endings_all = ["о", "а", "у", "е", "ом", "ах", "ами", "ам", ""]


ь_feminine_endings = ["ь", "и","ю","е","ям","ью","ей","ями","ях"]

soft_feminine_endings = ["я", "и","ю","е","ям","ями","ях","ь"]

ь_masc_endings = ["ь","я","и","ю","е","ям","ем","ей","ями","ях"]

ница_endings = ["ница", "ницы", "нице", "ницу", "ницей", "нице", "ниц", "ницам", "ницами", "ницах"]


all_adjective_endings = ["ый", "ий",
                         "ое", "ее",
                         "ая", "яя",
                         "ые", "ие", #Nominative non-masculine
                         "ого", "его", #Gen-Masc
                         "ой", "ей", #Oblique-Fem
                         "ых", "их",  #Gen/Acc-Pl
                         "ому", "ему", #Dat-Masc
                         "ым", "им", #Dat-Pl
                         "ыми", "ими", #Instr-Pl
                         "ую", "юю",  #Acc-Fem 
                         "ом", "ем"]

hard_adjective_endings = ["ый",
                         "ое",
                         "ая",
                         "ые", #Nominative non-masculine
                         "ого", #Gen-Masc
                         "ой", #Oblique-Fem
                         "ых",  #Gen/Acc-Pl
                         "ому", #Dat-Masc
                         "ым", #Dat-Pl
                         "ыми", #Instr-Pl
                         "ую",  #Acc-Fem 
                         "ом"]

soft_adjective_endings = ["ий",
                         "ее",
                         "яя",
                         "ие", #Nominative non-masculine
                         "его", #Gen-Masc
                         "ей", #Oblique-Fem
                         "их",  #Gen/Acc-Pl
                         "ему", #Dat-Masc
                         "им", #Dat-Pl
                         "ими", #Instr-Pl
                         "юю",  #Acc-Fem 
                         "ем"]

spelling_rule_1_letters = ["г", "к", "х"] # not Ы - write И
spelling_rule_1_adjective_endings = ["ий",
                                     "ое",
                                     "ая",
                                     "ие", #Nominative non-masculine
                                     "ого", #Gen-Masc
                                     "ой", #Oblique-Fem
                                     "их",  #Gen/Acc-Pl
                                     "ому", #Dat-Masc
                                     "им", #Dat-Pl
                                     "ими", #Instr-Pl
                                     "ую",  #Acc-Fem 
                                     "ом"]
 
spelling_rule_2_letters = ["ж", "ч", "ш", "щ"] # not Ы - write И, not unstressed O - E, not Ю - У, not Я - А
spelling_rule_2_adjective_endings = ["ий",
                                     "ее",
                                     "ая",
                                     "ие", #Nominative non-masculine
                                     "его", #Gen-Masc
                                     "ей", #Oblique-Fem
                                     "их",  #Gen/Acc-Pl
                                     "ему", #Dat-Masc
                                     "им", #Dat-Pl
                                     "ими", #Instr-Pl
                                     "ую",  #Acc-Fem 
                                     "ем"]
spelling_rule_ц_letters = ["ц"] #  not Ю - У, not Я - А, not unstressed O - E
spelling_rule_ц_adjective_endings = ["ый",
                                     "ее",
                                     "ая",
                                     "ые", # Nominative non-masculine
                                     "его", # Gen-Masc
                                     "ей", # Oblique-Fem
                                     "ых",  # Gen/Acc-Pl
                                     "ему", # Dat-Masc
                                     "ым", # Dat-Pl
                                     "ыми", # Instr-Pl
                                     "ую",  # Acc-Fem 
                                     "ем"]
   
reflexive_participle_endings = ["ийся",
                                "ееся",
                                "аяся",
                                "иеся", #Nominative non-masculine
                                "егося", #Gen-Masc
                                "ейся", #Oblique-Fem
                                "ихся",  #Gen/Acc-Pl
                                "емуся", #Dat-Masc
                                "имся", #Dat-Pl
                                "имися", #Instr-Pl
                                "уюся",  #Acc-Fem 
                                "емся"]



тель_endings = ["тель", "теля", "телей", "телю", "телях", "телями", "телям", "телем", "тели"]
 
ание_endings = ["ание",
                "ания",	"аний",
                "анию",	"аниям",
                "анием", "аниями",
                "ании","аниях"]

ение_endings = [ "ение",
                "ения",	"ений",
                "ению",	"ениям",
                "ением", "ениями",
                "ении","ениях"]


ость_endings = ["ость",
                "ости",	"остей",
                "остью","остями",
                        "остям",
                        "остях"]

ство_endings = ["ство", "ства", "ству", "стве", "ством",
                        "ств", "ствам", "ствах", "ствами"]

ия_endings = ["ия","ий", "ию", "ии", "иям", "ией", "иями", "иях"]
ие_endings = ["ие", "ия", "ий", "ию", "ии", "иям", "ием", "иями", "иях"]

ать_endings = ["ать", "аю","аешь","ает","аем","аете","ают",
               "аюсь","аешься","ается","аемся","аетесь","аются",
               "ал", "ало","ала","али",
               "ался", "алось","алась","ались",
               "ая", "аясь",
               "ай", "айте",
               "айся", "айтесь"]




ать_trns_endings = ["ать", "аю","аешь","ает","аем","аете","ают",
                    "ал", "ало","ала","али",
                    "ая", "ай", "айте"]

ать_refl_endings = ["аться","аюсь","аешься","ается","аемся","аетесь","аются",
                    "ался", "алось","алась","ались","айся", "айтесь", "аясь"]

ять_trns_endings = ["ять", "яю","яешь","яет","яем","яете","яют",
                    "ял", "яло","яла","яли",
                    "яя", "яй", "яйте"]

ять_refl_endings = ["яться","яюсь","яешься","яется","яемся","яетесь","яются",
                    "ялся", "ялось","ялась","ялись","яйся", "яйтесь", "яясь"]



ить_trns_endings = ["ить", "ю", "ишь", "ит", "ите", "им", "ят",
                    "ил", "или", "ило", "ила", "я",
                    "и"]

ить_refl_endings = ["иться", "юсь", "ишься", "ится", "итесь", "имся", "ятся",
                    "ился", "ились", "илось", "илась", "ясь",
                    "ись"]





ой_stems = ["прост", "остальн", "друг", "ин", "чуж","втор", "густ","годов", "трудов"]



print("Lists initialized.")
###############################################################################

word_list = list()

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
    word_list.append(word)


russ_match("сомнения", ение_endings)

dictionary_forms = {}



# Close the cursor and connection
cursor.close()
conn.close()




###############################################################################
#  The higher the ending length scanned, the lower the threshold can be.
# The lower the threshold, the less comprehensive the database needs to be.
# And, the easier to complete those words out from the task, allowing less
# reliable catches down the road to have lower thresholds, making them more likely
# to successfully catch poorly documented hyper-generic words (that don't have
# one of these easy, long, static endings)

print("Database inputted. Beginning scan...")
for word in word_list[::3]:
    

    if russ_match(word, ание_endings) > 3:
        for ending in ание_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                break
        dict_form = stem + "ание"
        dictionary_forms[word] = dict_form
        print("ание      ", word, dict_form, "\n")
    
    
    elif russ_match(word, ение_endings) > 3: # If word seems to fit ение_endings above 3 forms, assume it's a -ение word...
        for ending in ение_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                break
        dict_form = stem + "ение"
        dictionary_forms[word] = dict_form
        print("ение      ", word, dict_form, "\n")
        

        
    
    elif russ_match(word, ство_endings) > 3: # If word seems to fit ение_endings above 3 forms, assume it's a -ение word...
        for ending in ство_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                break
        dict_form = stem + "ство"
        dictionary_forms[word] = dict_form
        print("ство      ", word, dict_form, "\n")
    
   
    
    elif russ_match(word, ница_endings) > 2: # If word seems to fit ение_endings above 3 forms, assume it's a -ение word...
        for ending in ница_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                break
        dict_form = stem + "ница"
        dictionary_forms[word] = dict_form
        print("ница      ", word, dict_form, "\n")
    
    
    elif russ_match(word, ить_trns_endings) > 4:
        for ending in ить_trns_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                dict_form = stem + "ить"    
                break
        dictionary_forms[word] = dict_form
        print("ить       ", word, dict_form, "\n") 
        
    elif russ_match(word, ить_refl_endings) > 4:
        for ending in ить_refl_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                dict_form = stem + "иться"    
                break
        dictionary_forms[word] = dict_form
        print("иться       ", word, dict_form, "\n") 
    
    
                
    elif russ_match(word, ать_trns_endings) > 4:
        for ending in ать_trns_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                dict_form = stem + "ать"    
                break
        dictionary_forms[word] = dict_form
        print("ать       ", word, dict_form, "\n")    
        
        
    elif russ_match(word, ать_refl_endings) > 4:
        for ending in ать_refl_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                dict_form = stem + "аться"    
                break
        dictionary_forms[word] = dict_form
        print("аться     ", word, dict_form, "\n")  
        
    elif russ_match(word, ять_trns_endings) > 4:
        for ending in ять_trns_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                dict_form = stem + "ять"    
                break
        dictionary_forms[word] = dict_form
        print("ять       ", word, dict_form, "\n")    
        
        
    elif russ_match(word, ять_refl_endings) > 4:
        for ending in ять_refl_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                dict_form = stem + "яться"    
                break
        dictionary_forms[word] = dict_form
        print("яться     ", word, dict_form, "\n") 
        


    
    elif russ_match(word, ость_endings) >= 2:
        for ending in ость_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                break
        dict_form = stem + "ость"
        dictionary_forms[word] = dict_form
        print("ость      ", word, dict_form, "\n")
    
        
    elif russ_match(word, ие_endings) >= 8: 
        for ending in ие_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                break
        dict_form = stem + "ие"
        dictionary_forms[word] = dict_form
        print("ие        ", word, dict_form, "\n")
      
    
    elif russ_match(word, ия_endings) > 4: 
        for ending in ия_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                break
        dict_form = stem + "ия"
        dictionary_forms[word] = dict_form
        print("ия        ", word, dict_form, "\n")
        
    elif russ_match(word, тель_endings) > 2: # If word seems to fit ение_endings above 3 forms, assume it's a -ение word...
        for ending in тель_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                break
        dict_form = stem + "тель"
        dictionary_forms[word] = dict_form
        print("тель      ", word, dict_form, "\n")
    
    
    elif russ_match(word, ь_masc_endings) > 6: # If word seems to fit ение_endings above 3 forms, assume it's a -ение word...
        for ending in ь_masc_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                break
        dict_form = stem + "ь"
        dictionary_forms[word] = dict_form
        print("ь masc     ", word, dict_form, "\n")
    
    
    elif russ_match(word, soft_feminine_endings) > 6: # If word seems to fit ение_endings above 3 forms, assume it's a -ение word...
        for ending in soft_feminine_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                break
        dict_form = stem + "я"
        dictionary_forms[word] = dict_form
        print("soft fem  ", word, dict_form, "\n")
        
    
    
        
    
    elif russ_match(word, ь_feminine_endings) > 4: # If word seems to fit ение_endings above 3 forms, assume it's a -ение word...
        for ending in ь_feminine_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                break
        dict_form = stem + "ь"
        dictionary_forms[word] = dict_form
        print("ь fem     ", word, dict_form, "\n")
    
    
    elif russ_match(word, reflexive_participle_endings) > 3: # If word seems to fit ение_endings above 3 forms, assume it's a -ение word...
        for ending in reflexive_participle_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                break
        dict_form = stem + "ийся"
        dictionary_forms[word] = dict_form
        print("ийся      ", word, dict_form, "\n")
    
    
    elif russ_match(word, all_adjective_endings) >= 6: # Is AN adjective
        for ending in all_adjective_endings:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                
                if stem in ой_stems:
                    dict_form = stem + "ой"
                elif stem[-1] in spelling_rule_1_letters: # Stem possibility 1
                    dict_form = stem + "ий"
                    
                elif stem[-1] in spelling_rule_2_letters: # Stem possibility 2
                     dict_form = stem + "ий"
                     
                elif stem[-1] in spelling_rule_ц_letters: # Stem possibility ц
                     dict_form = stem + "ый"
                     
                elif russ_match(word, soft_adjective_endings) >= 3:
                    dict_form = stem + "ий" 
                    
                elif russ_match(word, hard_adjective_endings) >= 3:
                    dict_form = stem + "ый"
                
                break
                    
        dictionary_forms[word] = dict_form
        print("adjective ", word, dict_form, "\n")

    
    elif russ_match(word, fem_hard_endings_all) > 8:
        for ending in fem_hard_endings_all:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                dict_form = stem + "а"
                break
        dictionary_forms[word] = dict_form
        print("feminine  ", word, dict_form, "\n")
        
        
    elif russ_match(word, neuter_hard_endings_all) == 9:
        for ending in neuter_hard_endings_all:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                dict_form = stem + "о"
                break
        dictionary_forms[word] = dict_form
        print("neuter    ", word, dict_form, "\n")
                
        
    
    elif russ_match(word, masc_hard_endings_all) > 6:
        for ending in masc_hard_endings_all:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                dict_form = stem 
                break
        dictionary_forms[word] = dict_form
        print("masculine ", word, dict_form, "\n")
                
        
     
        
     
    else: 
        dictionary_forms[word] = word + " not captured by compiler."
        print("Escaped all capture!      ", word, "\n")
    

###############################################################################

# Manual Overrides

# долг's forms as долг, because долгий interferes
# компания as компания




with open("dictionary_forms.pkl", "wb") as f:
    pickle.dump(dictionary_forms, f)

