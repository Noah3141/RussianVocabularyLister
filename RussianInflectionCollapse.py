import re
import pickle


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



    
roots_noun = list()
roots_adj_ий = list()
roots_adj_ый = list()
roots_verb = list()
ство_words = list()
PreProcessLength = len(dictionary)
remove_words = list()
add_words = list()

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
            print("oh look an иe word: ", root+"иe")
        except: 
            dictionary[root+"ия"] = dictionary[root+"ия"] + dictionary.get(proposed_adj, 0)
            print("oh look an ия word: ", root+"ия")
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



                                ## Сollapsing -ать conjugations ##


# For those words who only have (at least) third-person singular and plural (one would
# expect very few first person conjugations in the dictionary)

for word in dictionary:
    if word.endswith("ает") or word.endswith("ают") and word.removesuffix("ает")+"ают" in dictionary or word.removesuffix("ают")+"ает" in dictionary:
        if word.endswith("ает"):
            add_words.append(word.removesuffix("ает")+"ать")
        if word.endswith("ают"):
            add_words.append(word.removesuffix("ают")+"ать")
        remove_words.append(word)
        remove_words.append(word.removesuffix("ать")+"ает")
        remove_words.append(word.removesuffix("ать")+"ают")
        remove_words.append(word.removesuffix("ать")+"аем")
        remove_words.append(word.removesuffix("ать")+"аю")
        remove_words.append(word.removesuffix("ать")+"аешь")
        remove_words.append(word.removesuffix("ать")+"аете") # 6 non-reflexive forms
        remove_words.append(word.removesuffix("ать")+"ается")
        remove_words.append(word.removesuffix("ать")+"аются")
        remove_words.append(word.removesuffix("ать")+"аемся")
        remove_words.append(word.removesuffix("ать")+"аюсь")
        remove_words.append(word.removesuffix("ать")+"аешься")
        remove_words.append(word.removesuffix("ать")+"аетесь") # 6 reflexive forms
        
        
for word in add_words:
    dictionary[word] = dictionary.get(word.removesuffix("ать")+"ает", 0) \
                     + dictionary.get(word.removesuffix("ать")+"ают", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аю", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аем", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аешь", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аете", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аются", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аюсь", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аемся", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аешься", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аетесь", 0) \
                     + dictionary.get(word.removesuffix("ать")+"ается", 0) \

for word in remove_words:
    try: del dictionary[word]
    except: continue
remove_words.clear()





for word in dictionary:
    if word.endswith("аю") or word.endswith("аем") and word.removesuffix("аю")+"аем" in dictionary or word.removesuffix("ают")+"ает" in dictionary:
        if word.endswith("ает"):
            add_words.append(word.removesuffix("ает")+"ать")
        if word.endswith("ают"):
            add_words.append(word.removesuffix("ают")+"ать")
        remove_words.append(word)
        remove_words.append(word.removesuffix("ать")+"ает")
        remove_words.append(word.removesuffix("ать")+"ают")
        remove_words.append(word.removesuffix("ать")+"аем")
        remove_words.append(word.removesuffix("ать")+"аю")
        remove_words.append(word.removesuffix("ать")+"аешь")
        remove_words.append(word.removesuffix("ать")+"аете") # 6 non-reflexive forms
        remove_words.append(word.removesuffix("ать")+"ается")
        remove_words.append(word.removesuffix("ать")+"аются")
        remove_words.append(word.removesuffix("ать")+"аемся")
        remove_words.append(word.removesuffix("ать")+"аюсь")
        remove_words.append(word.removesuffix("ать")+"аешься")
        remove_words.append(word.removesuffix("ать")+"аетесь") # 6 reflexive forms
        
        
for word in add_words:
    dictionary[word] = dictionary.get(word.removesuffix("ать")+"ает", 0) \
                     + dictionary.get(word.removesuffix("ать")+"ают", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аю", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аем", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аешь", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аете", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аются", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аюсь", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аемся", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аешься", 0) \
                     + dictionary.get(word.removesuffix("ать")+"аетесь", 0) \
                     + dictionary.get(word.removesuffix("ать")+"ается", 0) \

for word in remove_words:
    try: del dictionary[word]
    except: continue
remove_words.clear()





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








########################################################

print("Length of dictionary before processing: ", PreProcessLength)
print("Length after processing: ", len(dictionary))

#return(dictionary)