###############################################################################

# This script is run as an admin on a PC for creating updated .pkl files.
# Those .pkl files can then be pushed to the GIT repository, for use in the site.

# This file pulls the database, and creates a .pkl file, to push to GIT.

###############################################################################
###############################################################################

# Define test set

def Test_Output(dictionary: dict):
    print(        "Test        Input    Dictionary   Should Be")
    test_input = ["языки", "языков","стреляют","кошку","кошек","разговаривает","говорит", "сказал","хороших", "последнем"]
    test_output = [dictionary.get(word, "-") for word in test_input]
    
    test_key =   ["язык",   "язык","стрелять","кошка", "кошка","разговаривать","говорить","сказать","хороший", "последний"]

    for idx in range(0,len(test_input)):
        word = test_input[idx]
        test_output = dictionary.get(word,"-")
        if test_output == test_key[idx]:
            print(f"Passed:     {word}   {test_output}   {test_key[idx]}")
        else:
            print(f"FAILED:     {word}   {test_output}   {test_key[idx]}")
        


###############################################################################


import mysql.connector
import pickle


conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "nnssoteck3434###",
    database = "Database_001")

cursor = conn.cursor()
print("Connected to database!")


###############################################################################

 
masc_hard_endings_all =        ["ы", "а", "у", "е", "ом", "ах", "ами", "ов", "ам","и","ей", ""]
masc_hard_endings_default =    ["ы", "а", "у", "е", "ом", "ах", "ами", "ов", "ам", ""]    
masc_hard_endings_spelling_1 = ["и", "а", "у", "е", "ом", "ах", "ами", "ов", "ам", ""]
masc_hard_endings_spelling_2 = ["и", "а", "у", "е", "ом", "ах", "ами", "ей", "ам", ""]
masc_hard_endings_spelling_ц = ["и", "а", "у", "е", "ем", "ах", "ами", "ев", "ам", ""]

fem_hard_endings_all =        ["а", "ы","у","е","ам","ой","ами","ах","и","ей","", "ою"]
fem_hard_endings_default =    ["а", "ы","у","е","ам","ой","ами","ах","", "ою"]
fem_hard_endings_spelling_1 = ["а", "и","у","е","ам","ой","ами","ах","", "ою"]
fem_hard_endings_spelling_2 = ["а", "и","у","е","ам","ой","ами","ах","", "ою"]
fem_hard_endings_unstressed = ["а", "и","у","е","ам","ей","ами","ах",""]

neuter_hard_endings_all = ["о", "а", "у", "е", "ом", "ах", "ами", "ам", ""]

я_feminine_endings = ["я", "и","ю","е","ям","ями","ях","ь"]

ь_feminine_endings = ["ь", "и","ю","е","ям","ью","ей","ями","ях"]
ь_masc_endings =     ["ь","я","и","ю","е","ям","ем","ей","ями","ях"]

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

ница_endings = ["ница", "ницы", "нице", "ницу", "ницей", "нице", "ниц", "ницам", "ницами", "ницах"]


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

овать_endings = ["овать", "ую", "уешь","ует","уем","уете","уют",
                 "овал","овала","овало","овали","уй","уйте","уя",
                 "оваться", "уюсь", "уешься","уется","уемся","уетесь","уются",
                 "овался","овалсь","овалось","овались","уйся","уйтесь","уясь"]

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

сти_trns_endings = ["сти","у","ешь","ет","ем","ете","ут","и","ши","я"]
сти_refl_endings = ["стись","усь","ешься","ется","емся","етесь","утся","ись","шись","ясь"]
сти_infixes = ["д", "с", "б","т"]

ой_stems = set(["зл", "прост", "люб", "остальн", "друг", "ин", "чуж","втор", "густ","годов", "трудов",
            "языков","адов", "путев", "сед", "полов","смыслов", "седьм", "худ"])

енний_stems = set(["внутр","утр","ос","вес","искр","неискр","ранневес","предутр"])





print("Lists initialized.")
###############################################################################

word_list = list()


###############################################################################

def russ_match(word: str, ending_list: set) -> int:
    #match = 0
    #if any(word.endswith(ending) for ending in ending_list):
    match = 1
    global stem # If word ends in NONE of endings in ending list, it is never assigned a stem and the previous call is used [!!!]
    for ending in ending_list:
        if word.endswith(ending):
            stem = word[:-len(ending)]
            for other_ending in {e for e in ending_list if e != ending}:
                if stem + other_ending in word_list_set:
                    match += 1
            break
    print("\nMatch calculated for", word, "against", ending_list, "as", match)
    print("Stem calculated as : ", stem)
    return match  

###############################################################################

print("Inputting data from database...")
cursor.execute("SELECT word FROM words")
words = cursor.fetchall()


stop_words = set()
stop_words_txt = open("stop_words.txt", 'r', encoding='UTF-8')
for line in stop_words_txt:
    stop_words.add(line.rstrip())

    
for row in words:
    word = row[0]
    if word not in stop_words:
        word_list.append(word)

try:
    with open("dictionary_forms.pkl", "rb") as f: # Bring up the current state of pickle
        dictionary_forms = pickle.load(f) # BEWARE: Alterations to this script will not remove past flawed entries unless it contains a catch for their words!
except: 
    dictionary_forms = dict() # or make it 

# Close the cursor and connection
cursor.close()
conn.close()

word_list_set = set(word_list)
###############################################################################
#  The higher the ending length scanned, the lower the threshold can be.
# The lower the threshold, the less comprehensive the database needs to be.
# And, the easier to complete those words out from the task, allowing less
# reliable catches down the road to have lower thresholds, making them more likely
# to successfully catch poorly documented hyper-generic words (that don't have
# one of these easy, long, static endings)


print("Database inputted. Beginning scan...")
for word in word_list:
    
    print("\033[0m==========================================")
    print("\nCurrent word: ", word)
    
    if any(word.endswith(ending) for ending in ие_endings): 
        if russ_match(word, ие_endings) >= 8: 
            
            dict_form = stem + "ие"
            dictionary_forms[word] = dict_form
            print("\033[0;32mие        ", word, dict_form, "\033[0m\n\n======================================")
            continue
      
    if any(word.endswith(ending) for ending in ия_endings): 
        if russ_match(word, ия_endings) >= 4: # Singular forms need to be enough to catch words like Австралия (Австралия,Австралии,Австралию,Австралией)
            
            dict_form = stem + "ия"
            dictionary_forms[word] = dict_form
            print("\033[0;32mия        ", word, dict_form, "\033[0m\n\n======================================")
            continue
    
        
    if any(word.endswith(ending) for ending in reflexive_participle_endings): 
        if russ_match(word, reflexive_participle_endings) > 3: # If word seems to fit ение_endings above 3 forms, assume it's a -ение word...
            
            dict_form = stem + "ийся"
            dictionary_forms[word] = dict_form
            print("\033[0;32mийся      ", word, dict_form, "\033[0m\n\n======================================")
            continue
        
    
    
    if any(word.endswith(ending) for ending in ание_endings):
        if russ_match(word, ание_endings) > 3:
            
            dict_form = stem + "ание"
            dictionary_forms[word] = dict_form
            print("\033[0;32mание      ", word, dict_form, "\033[0m\n\n======================================")
            continue
    
    if any(word.endswith(ending) for ending in ение_endings):
        if russ_match(word, ение_endings) > 3: # If word seems to fit ение_endings above 3 forms, assume it's a -ение word...
            
            dict_form = stem + "ение"
            dictionary_forms[word] = dict_form
            print("\033[0;32mение      ", word, dict_form, "\033[0m\n\n======================================")
            continue
            

        
    if any(word.endswith(ending) for ending in ство_endings):
        if russ_match(word, ство_endings) > 3: # If word seems to fit ение_endings above 3 forms, assume it's a -ение word...
            
            dict_form = stem + "ство"
            dictionary_forms[word] = dict_form
            print("\033[0;32mство      ", word, dict_form, "\033[0m\n\n======================================")
            continue
    
   
    if any(word.endswith(ending) for ending in ница_endings):
        if russ_match(word, ница_endings) > 2: # If word seems to fit ение_endings above 3 forms, assume it's a -ение word...
           
            dict_form = stem + "ница"
            dictionary_forms[word] = dict_form
            print("\033[0;32mница      ", word, dict_form, "\033[0m\n\n======================================")
            continue
    
    
    if any(word.endswith(ending) for ending in all_adjective_endings): 
        print("\n\n          all_adjective_endings")
        if russ_match(word, all_adjective_endings) >= 3: # Is AN adjective
                    

                if stem in ой_stems:
                    dict_form = stem + "ой"
                    dictionary_forms[word] = dict_form
                    print("\033[0;32mой adjective ", word, dict_form, "\033[0m\n\n======================================")
                    continue
                
                elif stem.endswith("енн") and stem not in енний_stems:
                    dict_form = stem + "ый"
                    for ending in hard_adjective_endings:
                        dictionary_forms[(stem + ending)] = dict_form
                        print("\033[0;32mенный adjective ", stem + ending, dict_form, "\033[0m\n\n======================================")
                        continue

                elif stem[-1] in spelling_rule_1_letters: # Stem possibility 1
                    dict_form = stem + "ий"
                    dictionary_forms[word] = dict_form
                    print("\033[0;32mspelling rule 1 adjective ", word, dict_form, "\033[0m\n\n======================================")
                    continue

                    
                elif stem[-1] in spelling_rule_2_letters: # Stem possibility 2
                     dict_form = stem + "ий"
                     dictionary_forms[word] = dict_form
                     print("\033[0;32mspelling rule 2 adjective ", word, dict_form, "\033[0m\n\n======================================")
                     continue

                     
                elif stem[-1] in spelling_rule_ц_letters: # Stem possibility ц
                     dict_form = stem + "ый"
                     dictionary_forms[word] = dict_form
                     print("\033[0;32m ц adjective ", word, dict_form, "\033[0m\n\n======================================")
                     continue
                

                     
                if any(word.endswith(ending) for ending in soft_adjective_endings):
                    if russ_match(word, soft_adjective_endings) >= 3:
                        dict_form = stem + "ий"
                        dictionary_forms[word] = dict_form
                        print("\033[0;32madjective ", word, dict_form, "\033[0m\n\n======================================")
                        continue
                
                elif word.endswith("ее"):
                    if russ_match(word[:-2] + "ый", hard_adjective_endings) >= 4:
                        dict_form = stem + "ый"
                        dictionary_forms[word] = dict_form
                        print("\033[0;32mcomparative ", word, dict_form, "\033[0m\n\n======================================")
                        continue
                
                if any(word.endswith(ending) for ending in hard_adjective_endings):
                    if russ_match(word, hard_adjective_endings) >= 3:
                        dict_form = stem + "ый"
                        dictionary_forms[word] = dict_form
                        print("\033[0;32madjective ", word, dict_form, "\033[0m\n\n======================================")
                        continue



    
    
    
    
    
    if any(word.endswith(ending) for ending in ить_trns_endings):
        if russ_match(word, ить_trns_endings) > 4:
            
            dict_form = stem + "ить"    
            dictionary_forms[word] = dict_form
            print("\033[0;32mить       ", word, dict_form, "\033[0m\n\n======================================") 
            continue
    
    if any(word.endswith(ending) for ending in ить_refl_endings):
        if russ_match(word, ить_refl_endings) > 4:
            
            dict_form = stem + "иться"    
            dictionary_forms[word] = dict_form
            print("\033[0;32mиться       ", word, dict_form, "\033[0m\n\n======================================")
            continue
    
    
    if any(word.endswith(ending) for ending in ать_trns_endings):      
        score = russ_match(word, ать_trns_endings)
        
        if (score >= 1) and (stem[-2:] == "ыв" or stem[-2:] == "ив"):
            dict_form = stem + "ать"
            dictionary_forms[word] = dict_form
            print("\033[0;32mать       ", word, dict_form, "\033[0m\n\n======================================")    
            continue
        
        if score > 4:
           
            dict_form = stem + "ать"    
            dictionary_forms[word] = dict_form
            print("\033[0;32mать       ", word, dict_form, "\033[0m\n\n======================================")    
            continue
        
    if any(word.endswith(ending) for ending in ать_refl_endings):    
        if russ_match(word, ать_refl_endings) > 4:
           
            dict_form = stem + "аться"    
            dictionary_forms[word] = dict_form
            print("\033[0;32mаться     ", word, dict_form, "\033[0m\n\n======================================")  
            continue
        
    if any(word.endswith(ending) for ending in ять_trns_endings):
        if russ_match(word, ять_trns_endings) > 4:
           
            dict_form = stem + "ять"    
            dictionary_forms[word] = dict_form
            print("\033[0;32mять       ", word, dict_form, "\033[0m\n\n======================================")
            continue
        
    if any(word.endswith(ending) for ending in ять_refl_endings):  
        if russ_match(word, ять_refl_endings) > 4:
    
            dict_form = stem + "яться"    
            dictionary_forms[word] = dict_form
            print("\033[0;32mяться     ", word, dict_form, "\033[0m\n\n======================================") 
            continue


    if any(word.endswith(ending) for ending in ость_endings):  
        if russ_match(word, ость_endings) >= 2:
            
            dict_form = stem + "ость"
            dictionary_forms[word] = dict_form
            print("\033[0;32mость      ", word, dict_form, "\033[0m\n\n======================================")
            continue
        
    
    
    
    if any(word.endswith(ending) for ending in тель_endings):     
        if russ_match(word, тель_endings) > 2: 
           
            dict_form = stem + "тель"
            dictionary_forms[word] = dict_form
            print("\033[0;32mтель      ", word, dict_form, "\033[0m\n\n======================================")
            continue
   
    
       
    if any(word.endswith(ending) for ending in я_feminine_endings):
        print("\n\n          я_feminine_endings")
        if word[:-1] + "ем" not in word_list:
            if russ_match(word, я_feminine_endings) > 6: 
                
                dict_form = stem + "я"
                dictionary_forms[word] = dict_form
                print("\033[0;32mя fem  ", word, dict_form, "\033[0m\n\n======================================")
                continue


    
    if any(word.endswith(ending) for ending in ь_masc_endings):
        print("\n\n          ь_masc_endings")
        if (word[:-1] + "ью") not in word_list and (word[:-2] + "ью") not in word_list:
            if russ_match(word, ь_masc_endings) > 6: # Hardset Minimum 
                
                dict_form = stem + "ь"
                dictionary_forms[word] = dict_form
                print("\033[0;32mь masc     ", word, dict_form, "\033[0m\n\n======================================")
                continue
    
    
        
    if any(word.endswith(ending) for ending in ь_feminine_endings):
        print("\n\n          ь_feminine_endings")
        if russ_match(word, ь_feminine_endings) > 4: 
            
            dict_form = stem + "ь"
            dictionary_forms[word] = dict_form
            print("\033[0;32mь fem     ", word, dict_form, "\033[0m\n\n======================================")
            continue

    
    
    

    if any(word.endswith(ending) for ending in fem_hard_endings_all):
        print("\n\n          fem_hard_endings_all")
        if russ_match(word, fem_hard_endings_all) > 8:
            
            dict_form = stem + "а"
            dictionary_forms[word] = dict_form
            print("\033[0;32mfeminine  ", word, dict_form, "\033[0m\n\n======================================")
            continue
        
    if any(word.endswith(ending) for ending in neuter_hard_endings_all): # Beware sneaking vocative forms
        print("\n\n          neuter_hard_endings_all")
        if russ_match(word, neuter_hard_endings_all) == 6:
            if stem + "о" in word_list_set:
                
                dict_form = stem + "о"
                dictionary_forms[word] = dict_form
                print("\033[0;32mneuter    ", word, dict_form, "\033[0m\n\n======================================")
                continue
                
        
    if any(word.endswith(ending) for ending in masc_hard_endings_all):
        print("\n\n          masc_hard_endings_all")
        if russ_match(word, masc_hard_endings_all) > 6:
           
            dict_form = stem 
            dictionary_forms[word] = dict_form
            print("\033[0;32mmasculine ", word, dict_form, "\033[0m\n\n======================================")
            continue
                
    if any(word.endswith(ending) for ending in сти_trns_endings):
        print("\n\n          сти_trns_endings")
        if russ_match(word, сти_trns_endings) > 5:
            if stem[-1] in сти_infixes:
                stem = stem[:-1]
            dict_form = stem + "сти"
            dictionary_forms[word] = dict_form
            print("\033[0;32mсти ", word, dict_form, "\033[0m\n\n======================================")
            continue    
    
    if any(word.endswith(ending) for ending in сти_refl_endings):
        print("\n\n          сти_refl_endings")
        if russ_match(word, сти_refl_endings) > 5:
            if stem[-1] in сти_infixes:
                stem = stem[:-1]
            dict_form = stem + "стись"
            dictionary_forms[word] = dict_form
            print("\033[0;32mстись ", word, dict_form, "\033[0m\n\n======================================")
            continue  
    
    if any(word.endswith(ending) for ending in овать_endings):
        print("\n\n          овать_endings")
        if russ_match(word, овать_endings) > 4:
            if word.endswith("cь") or word.endswith("ся"):
                dict_form = stem + "оваться"
            else:
                dict_form = stem + "овать"
            dictionary_forms[word] = dict_form
            print("\033[0;32mовать ", word, dict_form, "\033[0m\n\n======================================")
            continue 
        
    if "ц" in word[-4:] and any(word.endswith(ending) for ending in masc_hard_endings_spelling_ц):
        print("\n\n          masc_hard_endings_spelling_ц")
        if russ_match(word, masc_hard_endings_all) > 6:
            dict_form = stem 
            dictionary_forms[word] = dict_form
            print("\033[0;32masc ц ", word, dict_form, "\033[0m\n\n======================================")
            continue

################ ADDRESSING INSUFFICIENT DATABASE VARIETY #####################
################## These are less necessary as db grows #######################
     
    # if "н" in word[-4:]: # Volatile block, produces "ый" outputs on some words
    #      print("\n\n          hard_adjective_endings")
    #      if russ_match(word, hard_adjective_endings + ["о", "ы", "а"]) >= 1:
    #          dict_form = stem + "ый" 
    #          dictionary_forms[word] = dict_form
    #          print("\033[35mный ", word, dict_form, "\033[0m\n\n======================================")
    #          continue
    
 

    print("\033[1;31mEscaped all capture!      ", word, "\033[0m\n\n======================================")
    pass





    

###############################################################################

# Manual Overrides




# Fleeting vowels mainly captured by words ending in к or ц (before ending)
fleeting_overrides = ["бугор"]
fleeting_overrides_к = ["крючок", "новичок","подшерсток","рожок","бугорок"]
fleeting_overrides_ц = ["танец","американец","резец","конец"]

for word in fleeting_overrides:
    dictionary_forms[word] = word
    stem = word[:-2] + word[-1]
    for ending in masc_hard_endings_default[:-1]:
        oblique_fleeting_word = stem + ending
        dictionary_forms[oblique_fleeting_word] = word
        pass
    pass
        

for word in fleeting_overrides_к:
    dictionary_forms[word] = word
    stem = word[:-2] + word[-1]
    for ending in masc_hard_endings_spelling_1[:-1]:
        oblique_fleeting_word = stem + ending
        dictionary_forms[oblique_fleeting_word] = word
        pass
    pass
        
for word in fleeting_overrides_ц:
    dictionary_forms[word] = word
    stem = word[:-2] + word[-1]
    for ending in masc_hard_endings_spelling_ц[:-1]:
        oblique_fleeting_word = stem + ending
        dictionary_forms[oblique_fleeting_word] = word
        pass
    pass

nasal_я_words = ["имя","пламя","знамя","пленя","беремя","время", "бремя","семя","темя","стремя","рамя"]
nasal_я_endings = ["ени", "енам", "енами", "енах", "ен", "енем"]

for word in nasal_я_words:
    dictionary_forms[word] = word
    stem = word[:-1]
    for ending in nasal_я_endings:
        form = stem + ending
        dictionary_forms[form] = word
        

# The dreaded class 6c verbs

   
class_6c_words = ["свистать", "искать", "чесать", "писать", "казаться", "казать", "вязать", "топтать", "хлестать", "плескать"]
    





class_6c_endings_trns = ["у","ешь","ем","ете","ет","ут","а"]
class_6c_endings_refl = ["усь","ешься","емся","етесь","ется","утся","ась"]
   

for word in class_6c_words:
    for prefix in ["","по","при","с","рас","раз","о","об","за","под","от","из"]:
        
        if word == "искать" and prefix == "раз" or prefix == "от" or prefix == "под" or prefix == "об" or prefix == "с" or prefix == "из":
            word = "ыскать"
        
        word = prefix + word    
            
        if word.endswith("зать") or word.endswith("заться"):
            if word.endswith("ся"):
                stem = word[:-6] + "ж"
                for ending in class_6c_endings_refl:
                    dictionary_forms[stem + ending] = word
            else:
                stem = word[:-4] + "ж"
                for ending in class_6c_endings_trns:
                    dictionary_forms[stem + ending] = word
        
        elif word.endswith("сать") or word.endswith("саться"):
            if word.endswith("ся"):
                stem = word[:-6] + "ш"
                for ending in class_6c_endings_refl:
                    dictionary_forms[stem + ending] = word
            else:
                stem = word[:-4] + "ш"
                for ending in class_6c_endings_trns:
                    dictionary_forms[stem + ending] = word
            
        elif word.endswith("скать") or word.endswith("скаться"):
            if word.endswith("ся"):
                stem = word[:-7] + "щ"
                for ending in class_6c_endings_refl:
                    dictionary_forms[stem + ending] = word
            else:
                stem = word[:-5] + "щ"
                for ending in class_6c_endings_trns:
                    dictionary_forms[stem + ending] = word
        
        elif word.endswith("пать") or word.endswith("паться"):
            if word.endswith("ся"):
                stem = word[:-6] + "пл"
                for ending in class_6c_endings_refl:
                    dictionary_forms[stem + ending] = word
            else:
                stem = word[:-4] + "пл"
                for ending in class_6c_endings_trns:
                    dictionary_forms[stem + ending] = word
        
        elif word.endswith("стать") or word.endswith("статься"):
            if word.endswith("ся"):
                stem = word[:-7] + "щ"
                for ending in class_6c_endings_refl:
                    dictionary_forms[stem + ending] = word
            else:
                stem = word[:-5] + "щ"
                for ending in class_6c_endings_trns:
                    dictionary_forms[stem + ending] = word
        
        elif word.endswith("тать") or word.endswith("таться"):
            if word.endswith("ся"):
                stem = word[:-6] + "ч"
                for ending in class_6c_endings_refl:
                    dictionary_forms[stem + ending] = word
            else:
                stem = word[:-4] + "ч"
                for ending in class_6c_endings_trns:
                    dictionary_forms[stem + ending] = word


# долг's forms as долг, because долгий interferes

for form in ["долг","долга","долги","долгов","долгам","долгами","долгу","долге"]:
    dictionary_forms[form] = "долг"
# компания as компания


# уметь forms need to overwrite less important умести's forms



with open("dictionary_forms.pkl", "wb") as f:
    pickle.dump(dictionary_forms, f)

