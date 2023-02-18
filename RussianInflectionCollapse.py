import re
import pickle

# Essentially all the blocks in this program follow the following pattern:
# Part 1: Go through whole Dictionary
# Part 2: Filter using checks, to ensure I've found a word of the type I want
# Part 3: Having passed those checks, vaccuum up all the forms
#           a) Sum frequency within the head (infinitive for verbs, nom-sing for nouns, nom-masc-sing for adjectives)
#           b) Go through and delete all the other entries we just summed from



# Known deficiencies:
# Some -вать ending verbs, like создать-создавать get collapsed into their perfective form only, because создаю is treated as if a normal -ать ending word, whose infinitive must be создать.... 

with open('Words.pkl', 'rb') as f:
    dictionary = pickle.load(f)
    

#def rui(dictionary): 
    
    
    
# Russian Adjective take a case and a number-gender. Number-gender can be either: masculine, neuter, feminine, or plural.
# Creating lists that provide endings

declensions_adj = ["ое","ая","ие","ее","яя","ые", #Nominative non-masculine
                  "ого","его", #Gen-Masc
                  "ой","ей", #Oblique-Fem
                  "их","ых",  #Gen/Acc-Pl
                  "ему", "ому", #Dat-Masc
                  "ым", "им", #Dat-Pl
                  "ими","ыми", #Instr-Pl
                  "ую", "юю",  #Acc-Fem 
                  "ом", "ем"] #Instr-Masc

# сомнение - neuter nominative noun, сомнения plural nominative form   VS     виктория feminine nominative
declensions_noun = ["ие", "ия", "ий", "ии", "ию", "иям", "иями", "иях", "ию", "ией"]


# Masculine noun basic endings
declension_hard_endings_nouns = ["а", "у", "ы", "е", "ом", "ах", "ами", "ов", "ам"]

ать_endings = ["аю","аешь","ает","аем","аете","ают",
               "аюсь","аешься","ается","аемся","аетесь","аются",
               "ал", "ало","ала","али",
               "ался", "алось","алась","ались",
               "ая", "аясь",
               "ай", "айте",
               "айся", "айтесь"]


    
roots_noun = list()
roots_adj_ий = list()
roots_adj_ый = list()
roots_verb = list()
ство_words = list()
PreProcessLength = len(dictionary)
remove_words = list()
add_words = list()
infinitives_list = list()


                         ## Collapse oblique -ый Adjectives into Nominative ##

for word in dictionary:
        if word.endswith('ый'):
                roots_adj_ый.append(word.removesuffix("ый"))

for root in roots_adj_ый:
    for declension in declensions_adj: #Go through the combination of a root, and each possible ending
        proposed_adj = root + declension #Build a non-nominative-masculine proposed word such as: *последное or коммунистического
        dictionary[root+"ый"] = dictionary[root+"ый"] + dictionary.get(proposed_adj, 0) # Find the nom-masc entry, and add the proposed word's count, 0 if does not exist
        try: del dictionary[proposed_adj]
        except: continue





                          ## Collapse oblique -ий Adjectives into Nominative ##   

# Sorts ий ending words into nouns or adjectives based on presence of -ия
for word in dictionary: 
        if word.endswith('ий'):
            root = word.removesuffix("ий")
            if root + "ия" not in dictionary:
                roots_adj_ий.append(root)
            else:
                roots_noun.append(root)


# -ий occurs at the end of: genitive plural abstract nouns, and half of 
# nominative adjectives. We will need to distinguish which root belongs to 
# which, in order to correctly collapse dictionary entries to their *nominative.*



## -ий adjective collapse
for root in roots_adj_ий:
    for declension in declensions_adj: #Go through the combination of a root, and each possible ending
        proposed_adj = root + declension #Build a non-nominative-masculine proposed word such as: *последное or коммунистического
        dictionary[root+"ий"] = dictionary[root+"ий"] + dictionary.get(proposed_adj, 0) # Find the nom-masc entry, and add the proposed word's count, 0 if does not exist
        try: del dictionary[proposed_adj]
        except: continue
    
    
## -ий noun collapse  

# If a noun can be found as -ия but can't be found as -ие, the nominative head is -ия (виктория),
# Else, if the noun can be found as either, the -ие is the nominative (сомнение, сомнения)

for root in roots_noun:
    for declension in declensions_noun: #Go through the combination of a root, and each possible ending
        proposed_noun = root + declension #Build a non-nominative-masculine proposed word such as: *последное or коммунистического
        try: 
            dictionary[root+"ие"] = dictionary[root+"ие"] + dictionary.get(proposed_adj, 0) # Find the nom-masc entry, and add the proposed word's count, 0 if does not exist
            #print("oh look an иe word: ", root+"иe")
        except: 
            dictionary[root+"ия"] = dictionary[root+"ия"] + dictionary.get(proposed_adj, 0)
            #print("oh look an ия word: ", root+"ия")
            try: del dictionary[proposed_adj]
            except: continue
        try: del dictionary[proposed_adj]
        except: continue
        


                            ## Collapsing Nouns ending in -ство ##

ство_endings = ["ства", "ств", "ству", "ством","стве","ствах","ствами","ствам"]
for word in dictionary:
    if word.endswith("ство"):
        root = word.removesuffix("ство")
        for ending in ство_endings:
            proposed_noun = root + ending
            remove_words.append(proposed_noun)
            dictionary[word] = dictionary[word] + dictionary.get(proposed_noun, 0)
for word in remove_words:
    try: del dictionary[word]
    except: continue
remove_words.clear()

##
        
       
for root in roots_adj_ий:
    for ending in ство_endings: #Go through the combination of a root, and each possible ending
        proposed_noun = root + declension #Build a non-nominative-masculine proposed word such as: *последное or коммунистического
        dictionary[root+"ий"] = dictionary[root+"ий"] + dictionary.get(proposed_adj, 0) # Find the nom-masc entry, and add the proposed word's count, 0 if does not exist
        try: del dictionary[proposed_adj]
        except: continue


                        ## Сollapsing -ать verbs FOUND AS present conjugations ##


# For those words who only have (at least) third-person singular and plural (one would
# expect very few first person conjugations in the dictionary)

for word in dictionary:
    if word.endswith("ает") or word.endswith("ают") and word.removesuffix("ает")+"ают" in dictionary or word.removesuffix("ают")+"ает" in dictionary:
        if word.endswith("ает"):
            add_words.append(word.removesuffix("ает")+"ать")
        if word.endswith("ают"):
            add_words.append(word.removesuffix("ают")+"ать")
        remove_words.append(word) # First add to the remove list the word, then all its other forms
        for suffix in ать_endings:
            remove_words.append(word.removesuffix("ать")+suffix) # Take the FOUND word's presumed infinitive, and generate me all the other stable forms and add them to remove list
        
        
for word in add_words: # Take the FOUND word, checked to be derived from -ать, and subsume all the forms' frequencies under the infinitive
    for suffix in ать_endings:
        dictionary[word] = dictionary.get(word,0) + dictionary.get(word.removesuffix("ать")+suffix, 0)

for word in remove_words: # Having subsumed all the frequencies under infinitive, clear out other forms where extant
    try: del dictionary[word]
    except: continue
remove_words.clear()




# The previous section checked for either third person, spanning number, but in order to succintly collect all forms, this section spans *person*, within number
for word in dictionary:
    if word.endswith("аю") or word.endswith("аешь") and word.removesuffix("аю")+"аешь" in dictionary or word.removesuffix("аешь")+"аю" in dictionary:
        if word.endswith("аю"):
            add_words.append(word.removesuffix("аю")+"ать")
        if word.endswith("аешь"):
            add_words.append(word.removesuffix("аешь")+"ать")
        for suffix in ать_endings:
            remove_words.append(word.removesuffix("ать")+suffix) # Add all its forms to remove list
        
        
for word in add_words:
    for suffix in ать_endings:
        dictionary[word] = dictionary.get(word,0) \
                      + dictionary.get(word.removesuffix("ать")+suffix, 0)

for word in remove_words:
    try: del dictionary[word]
    except: continue
remove_words.clear()


                        ## Collapsing words FOUND ONLY in past-test form of -ать verbs ##
for word in dictionary:
    if (word.endswith("али") or word.endswith("ала") or word.endswith("ало") or word.endswith("ал")):
        match = re.search("ал", word) # Find me where the "ал" occurs in this word (think скандал, e.g. NOT a verb)
        index = match.start() # give me the index of the start of that "ал" or "алось" etc.
        # If the root plus one of our other endings exists :
        if (word[:index:]+("ало" or "али" or "ала" or "ать" or "ал") in dictionary) \
        and word[:index:]+"ы" not in dictionary and word[:index:]+"у" not in dictionary: # But a noun form doesn't (скандалы now removes скандал from consideration)
            infinitive = word[:index:]+"ать"
            infinitives_list.append(infinitive)
    
for infinitive in infinitives_list:
        dictionary[infinitive] = dictionary.get(infinitive, 0) \
                                +dictionary.get(infinitive.removesuffix("ать")+"ал",0) \
                                +dictionary.get(infinitive.removesuffix("ать")+"ала",0) \
                                +dictionary.get(infinitive.removesuffix("ать")+"ало",0) \
                                +dictionary.get(infinitive.removesuffix("ать")+"али",0)
        for ending in ["ал", "ало", "али", "ала"]:
            conjugated_form = infinitive.removesuffix("ать")+ending
            try: del conjugated_form
            except: continue
    

infinitives_list.clear()
# test_word = "рассказывать"
# print(dictionary[test_word], test_word in dictionary)

# for word in dictionary:
#     if word.endswith("аю"):
#         print(word)

##


## Collapsing perfective and imperfective verbs where there is an imperfective -ивать ##
# The ending -ивать also sometimes causes a stem change, which can be dealt with using regular expressions:
# говорить > -говаривать
# 
#
#
#



########################################################
# Once collapsing is complete, some attempts can be made to reformulate those entries which were only 
# found in non-dictionary forms, e.g. автоматными (1) should be replaced with автоматный (1)


for word in dictionary:
    for ending in declension_hard_endings_nouns:
        if word.endswith(ending): # Find me words that look like they end in masc case endings (but not the nominative)
            if word.removesuffix(ending) in dictionary and word.removesuffix(ending) + "ами" in dictionary:
                # Test IF you can remove the ending and still find a real word, AND you can add on a standard masc ending and still find a word...
                # If so, sounds like a masculine word in a
                dictionary[word.removesuffix(ending)] = dictionary[word.removesuffix(ending)] + dictionary.get(word, 0)
                remove_words.append(word)
            
for word in remove_words:
    try: del dictionary[word]
    except: continue
remove_words.clear()



#########

## Common, known irregular patterns:




########################################################

print("Length of dictionary before processing: ", PreProcessLength)
print("Length after processing: ", len(dictionary))

#return(dictionary)