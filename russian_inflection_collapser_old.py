def ruic(dictionary:dict, name:str, breadth, style):

    import re

# Essentially all the blocks in this program follow the following pattern:
# Part 1: Go through whole Dictionary
# Part 2: Filter using checks, to ensure I've found a word of the type I want
# Part 3: Having passed those checks, vaccuum up all the forms
#           a) Sum frequency within the head (infinitive for verbs, nom-sing for nouns, nom-masc-sing for adjectives)
#           b) Go through and delete all the other entries we just summed from
#
# Alternatively put:
# Catch     (get words by qualities reminiscent of X, e.g. being a masculine noun)
# Reject    (test that suspected word passes abilities of a veritable masculine noun)
# Inflect   (if it passed, assume it is a masc noun, generate all the other forms)
# Collect   (sum the occurances, delete non-dictionary forms)


# Known deficiencies:
# Some -вать ending verbs, like создать-создавать get collapsed into their perfective form only, because создаю is treated as if a normal -ать ending word, whose infinitive must be создать.... 
# During the processing of жать/-жимать, жать/-жинать is destroyed.

# ctrl+f the phrase "in dictionary" to see the amount it relies on a broad enough webcrawler



    
    
    
# Russian Adjective take a case and a number-gender. Number-gender can be either: masculine, neuter, feminine, or plural.
# Creating lists that provide endings
    
    declensions_adj = ["ое", "ее",
                       "ая", "яя",
                       "ые", "ие", #Nominative non-masculine
                      "ого", "его", #Gen-Masc
                      "ой", "ей", #Oblique-Fem
                      "ых", "их",  #Gen/Acc-Pl
                      "ому", "ему", #Dat-Masc
                      "ым", "им", #Dat-Pl
                      "ыми", "ими", #Instr-Pl
                      "ую", "юю",  #Acc-Fem 
                      "ом", "ем"] #Instr-Masc

# сомнение - neuter nominative noun, сомнения plural nominative form   VS     виктория feminine nominative
    declensions_ия_noun = ["ие", "ия", "ий", "ии", "ию", "иям", "иями", "иях", "ию", "ией"]


# Masculine noun basic endings
    declension_masc_hard_endings_nouns = ["а", "у", "ы", "е", "ом", "ах", "ами", "ов", "ам", "и"]
    declension_fem_hard_endings_nouns = ["у", "ы", "е", "ой", "ах", "ами", "ам", "и"] # !SOFT И INCLUDED FOR SPELLING RULE!
    
    ать_endings = ["аю","аешь","ает","аем","аете","ают",
                   "аюсь","аешься","ается","аемся","аетесь","аются",
                   "ал", "ало","ала","али",
                   "ался", "алось","алась","ались",
                   "ая", "аясь",
                   "ай", "айте",
                   "айся", "айтесь"]
    
    ать_past_tense_endings = ["ал", "ало","ала","али",
                              "ался", "алось","алась","ались"]
    
        
    roots_noun = list()
    roots_adj_ий = list()
    roots_adj_ый = list()
    roots_verb = list()
    ство_words = list()
    pre_process_length = len(dictionary)
    remove_words = list()
    add_words = list()
    infinitives_list = list()

###############################################################################
# Bolstering Dictionary Presence
###############################################################################
# Find those forms that are present which definitively imply a particular 
# dictionary form, and deal with all those first
    add_words = list()

    for word in dictionary:
        if word.endswith("ией"):
            add_words.append(word.removesuffix("ией") + "ия")
            remove_words.append(word)
        if word.endswith("ения"):
            add_words.append(word.removesuffix("ения") + "ие")
            remove_words.append(word)
        if word.endswith("ания"):
            add_words.append(word.removesuffix("ания") + "ие")
            remove_words.append(word)
            
            
    for word in add_words:
        dictionary.get(word, 0) + 1
    
    for word in remove_words:
        try: del dictionary[word]
        except: continue
    
    remove_words.clear()        
    add_words.clear()
###############################################################################
# Collapse -вать special cases !EARLY!
###############################################################################



###############################################################################
# Collapse oblique -ый Adjectives into Nominative
###############################################################################    
    for word in dictionary:
            if word.endswith('ый'):
                    roots_adj_ый.append(word.removesuffix("ый"))
                    
    for root in roots_adj_ый:
        for declension in declensions_adj: #Go through the combination of a root, and each possible ending
            proposed_adj = root + declension #Build a non-nominative-masculine proposed word such as: *последное or коммунистического
            dictionary[root + "ый"] = dictionary[root + "ый"] + dictionary.get(proposed_adj, 0) # Find the nom-masc entry, and add the proposed word's count, 0 if does not exist
            try: del dictionary[proposed_adj]
            except: continue

###############################################################################
# Collapse oblique -ий Adjectives into Nominative
###############################################################################

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
            dictionary[root + "ий"] = dictionary[root + "ий"] + dictionary.get(proposed_adj, 0) # Find the nom-masc entry, and add the proposed word's count, 0 if does not exist
            try: del dictionary[proposed_adj]
            except: continue
        
        
## -ий noun collapse  

# If a noun can be found as -ия but can't be found as -ие, the nominative head is -ия (виктория),
# Else, if the noun can be found as either, the -ие is the nominative (сомнение, сомнения)

    for root in roots_noun:
        for declension in declensions_ия_noun: #Go through the combination of a root, and each possible ending
            proposed_noun = root + declension #Build a non-nominative-masculine proposed word such as: *последное or коммунистического
            try: 
                dictionary[root +" ие"] = dictionary[root + "ие"] + dictionary.get(proposed_adj, 0) # Find the nom-masc entry, and add the proposed word's count, 0 if does not exist
            except: 
                dictionary[root + "ия"] = dictionary[root + "ия"] + dictionary.get(proposed_adj, 0)
                try: del dictionary[proposed_adj]
                except: continue
            try: del dictionary[proposed_adj]
            except: continue
            



###############################################################################
# Collapsing Nouns ending in -ство 
###############################################################################
    # ство_endings = ["ства", "ств", "ству", "ством","стве","ствах","ствами","ствам"]
    # for word in dictionary:
    #     if word.endswith("ство"):
    #         root = word.removesuffix("ство")
    #         for ending in ство_endings:
    #             proposed_noun = root + ending
    #             remove_words.append(proposed_noun)
    #             dictionary[word] = dictionary[word] + dictionary.get(proposed_noun, 0)
    
    # for word in remove_words:
    #     try: del dictionary[word]
    #     except: continue
    # remove_words.clear()



###############################################################################
# Collapsing cases of feminine nouns
###############################################################################                        
# for word in dictionary:
#     if word.endswith("а"

###############################################################################
#Сollapsing -ать verbs FOUND AS present conjugations
###############################################################################

# For those words who only have (at least) third-person singular and plural (one would
# expect very few first person conjugations in the dictionary)

    for word in dictionary:
        if word.endswith("ает") or word.endswith("ают") and word.removesuffix("ает") + "ают" in dictionary or word.removesuffix("ают")+"ает" in dictionary:
            if word.endswith("ает"):
                add_words.append(word.removesuffix("ает") + "ать")
            if word.endswith("ают"):
                add_words.append(word.removesuffix("ают") + "ать")
            remove_words.append(word) # First add to the remove list the word, then all its other forms
            for suffix in ать_endings:
                remove_words.append(word.removesuffix("ать") + suffix) # Take the FOUND word's presumed infinitive, and generate me all the other stable forms and add them to remove list
             
    for word in add_words: # Take the FOUND word, checked to be derived from -ать, and subsume all the forms' frequencies under the infinitive
        for suffix in ать_endings:
            dictionary[word] = dictionary.get(word, 0) + dictionary.get(word.removesuffix("ать") + suffix, 0)
    
    for word in remove_words: # Having subsumed all the frequencies under infinitive, clear out other forms where extant
        try: del dictionary[word]
        except: continue
    remove_words.clear()
    



# The previous section checked for either third person, spanning number, but in order to succintly collect all forms, this section spans *person*, within number
    for word in dictionary:
        if word.endswith("аю") or word.endswith("аешь") and word.removesuffix("аю") + "аешь" in dictionary or word.removesuffix("аешь")+"аю" in dictionary:
            if word.endswith("аю"):
                add_words.append(word.removesuffix("аю") + "ать")
            if word.endswith("аешь"):
                add_words.append(word.removesuffix("аешь") + "ать")
            for suffix in ать_endings:
                remove_words.append(word.removesuffix("ать") + suffix) # Add all its forms to remove list
                
    for word in add_words:
        for suffix in ать_endings:
            dictionary[word] = dictionary.get(word, 0) \
                          + dictionary.get(word.removesuffix("ать") + suffix, 0)
    
    for word in remove_words:
        try: del dictionary[word]
        except: continue
    remove_words.clear()

###############################################################################
# Collapsing words FOUND ONLY in past-test form of -ать verbs
###############################################################################

    for word in dictionary:
        for ending in ать_past_tense_endings:
            if (word.endswith(ending)):
                match = re.search("ал", word) # Find me where the "ал" occurs in this word (think скандал, e.g. NOT a verb)
                index = match.start() # give me the index of the start of that "ал" or "алось" etc.
                # If the root plus one of our other endings exists :
                if (word[:index:] + ("ало" or "али" or "ала" or "ать" or "ал" or "алась" or "ался") in dictionary) \
                    and word[:index:] + "ы" not in dictionary and word[:index:] + "у" not in dictionary: # But a noun form doesn't (скандалы now removes скандал from consideration)
                    infinitive = word[:index:] + "ать"
                    if infinitive not in infinitives_list:
                        infinitives_list.append(infinitive)
        
    for infinitive in infinitives_list:
            dictionary[infinitive] = dictionary.get(infinitive, 0) \
                                    +dictionary.get(infinitive.removesuffix("ать") + "ал", 0) \
                                    +dictionary.get(infinitive.removesuffix("ать") + "ала", 0) \
                                    +dictionary.get(infinitive.removesuffix("ать") + "ало", 0) \
                                    +dictionary.get(infinitive.removesuffix("ать") + "али", 0)
            for ending in ["ал", "ало", "али", "ала"]:
                conjugated_form = infinitive.removesuffix("ать") + ending
                try: del conjugated_form
                except: continue
        

    infinitives_list.clear()

###############################################################################
# Collapsing -ить past-tense
###############################################################################

    ить_past_tense_ending = ["ил","ило","ила","или","ился","илось","илась","ились"]
    for word in dictionary:
        for ending in ить_past_tense_ending:
            if word.endswith(ending) and (word.removesuffix(ending) + "ит" in dictionary or word.removesuffix(ending) + "ится" in dictionary):
                infinitive = word.removesuffix(ending) + "ить"
                if infinitive not in infinitives_list:
                    infinitives_list.append(infinitive)
                remove_words.append(word)
    for infinitive in infinitives_list:
        for ending in ить_past_tense_ending:
                dictionary[infinitive] = dictionary.get(infinitive, 0) + dictionary.get(infinitive.removesuffix("ить") + ending, 0)       
    
    for word in remove_words:
        try: del dictionary[word]
        except: continue
    remove_words.clear()


###############################################################################
# Collapsing Masculine Nouns
###############################################################################

    for word in dictionary:
        for ending in declension_masc_hard_endings_nouns:
            if word.endswith(ending): # Find me words that look like they end in masc case endings (but not the nominative)
                if word.removesuffix(ending) in dictionary and (word.removesuffix(ending) + "ом" or word.removesuffix(ending) + "ов") in dictionary:
                    # Test IF you can remove the ending and still find a real word (still might be a feminine noun until:), AND you can add on a standard masc-only ending and still find a word...
                    # If so, sounds like a masculine word in a
                    dictionary[word.removesuffix(ending)] = dictionary[word.removesuffix(ending)] + dictionary.get(word, 0)
                    remove_words.append(word)
                
    for word in remove_words:
        try: del dictionary[word]
        except: continue
    remove_words.clear()


#Once collapsing is complete, some attempts can be made to reformulate those entries which were only 
# found in non-dictionary forms, e.g. автоматными (1) should be replaced with автоматный (1)


    print("Length of ", name, " before processing: ", pre_process_length)
    print("Length of ", name, " after processing: ", len(dictionary))

    return(dictionary)