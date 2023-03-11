# Intended to remove clearly not real words from the database

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

я_feminine_endings = ["я", "и","ю","е","ям","ями","ях","ь"]

ь_feminine_endings = ["ь", "и","ю","е","ям","ью","ей","ями","ях"]
ь_masc_endings =     ["ь","я","и","ю","е","ям","ем","ей","ями","ях"]

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

all_endings = ить_refl_endings \
+ ить_trns_endings \
+ ять_refl_endings \
+ ять_trns_endings \
+ ать_endings \
+ ие_endings \
+ ия_endings \
+ ство_endings \
+ ость_endings \
+ ение_endings \
+ ание_endings \
+ тель_endings \
+ reflexive_participle_endings \
+ all_adjective_endings \
+ neuter_hard_endings_all \
+ fem_hard_endings_all \
+ masc_hard_endings_all \
+ ь_feminine_endings

vowels = ["а", "о", "ы", "э", "у", 
          "я", "ё", "и", "е", "ю"]

hard_vowels = ["а", "о", "ы", "э", "у"]

soft_vowels = ["я", "ё", "и", "е", "ю"]

consonants = ["ь","б", "в", "г", "д", "ж", "з", "к", "л", "м", "н", "п", "р", "с", "т", "ф", "х", "ц", "ч", "ш", "щ"]
###############################################################################



import mysql.connector


conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "nnssoteck3434###",
    database = "Database_001")

cursor = conn.cursor()
print("Connected to database!")




print("Inputting data from database...")
cursor.execute("SELECT word FROM words")
words = cursor.fetchall()

    
word_list = []
for row in words:
    word = row[0]
    word_list.append(word)

clear_list = []

###############################################################################

# for word in word_list:
#     if len(word) < 3:
#         clear_list.append(word)

# for word in word_list:
#     if "ця" in word:
#         clear_list.append(word)

# for word in word_list:                 # Empty
#     if "-" in word or "ё" in word:
#         clear_list.append(word)

# for word in word_list:
#     if word.startswith("ы"):
#         clear_list.append(word)


# DO NOT USE, CONTAINS MANY REAL WORDS
# for word in word_list: # Checks for consonant clusters of 
#     for i in range(0,10):
#         try:
#             if word[i] in consonants and word[i + 1] in consonants and word[i + 2] in consonants and word[i + 3] in consonants  and word[i + 4] in consonants:
#                 clear_list.append(word)
#         except: continue

# DO NOT USE, CONTAINS MANY REAL WORDS
# for word in word_list: # Checks for consonant clusters of vowels
#     for i in range(0,10):
#         try:
#             if word[i] in vowels and word[i + 1] in hard_vowels:
#                     clear_list.append(word)
#         except: continue


# This does remove technically Russian words, but essentially only ones with
# Alternative spellings. Pretty much all words caught are related to Kyrgyz.
# for word in word_list: # Russian spelling rule 1
#     if "кы" in word or "шы" in word or "гы" in word or "щы" in word or "хы" in word or "жы" in word or "чы" in word:
#         clear_list.append(word)
 

       
# for word in word_list: # Russian spelling rule 3
#     if "кя" in word or "шя" in word or "гя" in word or "щя" in word or "хя" in word or "жя" in word or "чя" in word or "ця" in word:
#         clear_list.append(word)

# for word in word_list: # Russian spelling rule 4
#     if "кю" in word or "шю" in word or "гю" in word or "щю" in word or "хю" in word or "жю" in word or "чю" in word or "цю" in word:
#         clear_list.append(word)
        
                
        


###############################################################################

# Comment out the following section, check the clear list for accuracy,
# If clear list only contains words to remove, un-comment the following block,
# And run script.



# for word in clear_list:
#     cursor.execute(f"DELETE FROM words WHERE word = '{word}';")
#     conn.commit()
#     print("Deleted word ", word, " from database.")







cursor.close()
conn.close() 