# Catch
# Verify
# Permutate
# Collect
# Label for deletion/skipping


#def ruic(dictionary:dict, name:str, breadth, style):
import pickle 
with open("reference_dictionary.pkl", "rb") as f:
    dictionary = pickle.load(f) 
    
   
def russ_match(word: str, ending_list: list):
    match = 0
    for ending in ending_list: # Going through all the endings
        if word.endswith(ending): # We proc ONE of the endings
            for other_ending in ending_list:
                if ending == other_ending: continue
                if word.removesuffix(ending) + other_ending in dictionary:
                    match = match + 1
    
    #if match >= threshold:
    return match
    #else: return False
   
masc_hard_endings_nouns_all =        ["а", "у", "ы", "е", "ом", "ах", "ами", "ов", "ам","и","ей"]
masc_hard_endings_nouns_default =    ["а", "у", "ы", "е", "ом", "ах", "ами", "ов", "ам"]    
masc_hard_endings_nouns_spelling_1 = ["а", "у", "и", "е", "ом", "ах", "ами", "ов", "ам"]
masc_hard_endings_nouns_spelling_2 = ["а", "у", "и", "е", "ом", "ах", "ами", "ей", "ам"]

fem_hard_endings_all =        ["ы","","у","е","ам","ой","ами","е","ах","и","ей"]
fem_hard_endings_default =    ["ы","","у","е","ам","ой","ами","е","ах"]
fem_hard_endings_spelling_1 = ["и","","у","е","ам","ой","ами","е","ах"]
fem_hard_endings_spelling_2 = ["и","","у","е","ам","ой","ами","е","ах"]
fem_hard_endings_unstressed = ["и","","у","е","ам","ей","ами","е","ах"]


addressed_words = list()

all_adjective_endings = ["ое", "ее",
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

hard_adjective_endings = ["ое",
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

soft_adjective_endings = ["ее",
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
spelling_rule_1_adjective_endings = ["ое",
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
spelling_rule_2_adjective_endings = ["ее",
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
spelling_rule_ц_adjective_endings = ["ее",
                                     "ая",
                                     "ые", #Nominative non-masculine
                                     "его", #Gen-Masc
                                     "ей", #Oblique-Fem
                                     "ых",  #Gen/Acc-Pl
                                     "ему", #Dat-Masc
                                     "ым", #Dat-Pl
                                     "ыми", #Instr-Pl
                                     "ую",  #Acc-Fem 
                                     "ем"]
    
ание_endings = [
                "ания",	"аний",
                "анию",	"аниям",
                "анием", "аниями",
                "ании","аниях"]

ение_endings = [
                "ения",	"ений",
                "ению",	"ениям",
                "ением", "ениями",
                "ении","ениях"]

ия_endings = ["ий", "ию", "ии", "иям", "ией", "иями", "иях"]




stop_words = list()
stop_words_txt = open("stop_words.txt", 'r', encoding='UTF-8')
for line in stop_words_txt:
    stop_words.append(line.rstrip())

for word in stop_words:
    if word in dictionary:
        del dictionary[word]
###############################################################################

ой_stressed_adjectives = ["такой", "простой", "смешной", "другой", "пустой"]
for word in ой_stressed_adjectives:
    for ending in all_adjective_endings:
        oblique_form = word.removesuffix("ой") + ending
        dictionary[word] = dictionary.get(word, 0) + dictionary.get(oblique_form, 0)
        try:
            del dictionary[oblique_form]
        except:
            continue
    addressed_words.append(word)

unstressed_ending_feminine_nouns = ["кожа"]
for word in unstressed_ending_feminine_nouns:
    for ending in fem_hard_endings_unstressed:
        oblique_form = word.removesuffix("а") + ending
        dictionary[word] = dictionary.get(word, 0) + dictionary.get(oblique_form, 0)
        try:
            del dictionary[oblique_form]
        except:
            continue
    addressed_words.append(word)


###############################################################################
###############################################################################    
for word in list(dictionary): # One section represents all the *non-overlapping* first-pass scans
###############################################################################        
    
# ение stem catcher       
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #        
    if len(word) < 2: 
        try:
            del dictionary[word]
        except:
            continue
    if word not in dictionary: continue # We do deletion during the loop, so missing keys will be called
    if word in addressed_words: continue # We want successful catch-&-process procs to block re-processing
    if russ_match(word, ение_endings) >= 3: # If word seems to fit ение_endings above 3 forms, assume it's a -ение word...
        for ending in ение_endings: # So, go through the endings...
            if word.removesuffix(ending) != word: # Until you can succesfully remove one, giving me the stem
                stem = word.removesuffix(ending)
                dict_form = stem + "ение"  # Name the dictionary form because they aren't in the lists above
                addressed_words.append(dict_form) # Save this for later to be extra sure not to include in later catches
                for ending in ение_endings: # Go through the endings, then
                    dictionary[dict_form] = dictionary.get(dict_form, 0) + dictionary.get(stem + ending, 0)
                                            # Take the dictionary form's value (add it as 0 if not present yet)
                                            # and add the oblique forms
                    addressed_words.append(stem + ending) # Save this for later to be extra sure not to include in later catches
                    # try: del dictionary[stem + ending] # then delete any of those oblique forms found in the dictionary
                    # except: continue # If it wasn't in there, move on to next oblique form
                break # Be done with the first for loop, as we only needed it to proc through the 'if' once
            pass

# ание stem catcher
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #                 
    if word not in dictionary: continue
    if word in addressed_words: continue
    if russ_match(word, ание_endings) >=3:
        for ending in ание_endings:
            if word.removesuffix(ending) != word:
                stem = word.removesuffix(ending)
                dict_form = stem + "ание"
                addressed_words.append(dict_form)
                for ending in ание_endings:
                    dictionary[dict_form] = dictionary.get(dict_form, 0) \
                                            + dictionary.get(stem + ending, 0) 
                    addressed_words.append(stem + ending) 
                    # try: del dictionary[stem + ending]
                    # except: continue
                    pass
                break
            pass

# Adjective catcher      
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    if word not in dictionary: continue
    if word in addressed_words: continue
    if russ_match(word, all_adjective_endings) >= 6: # Is AN adjective
        for ending in all_adjective_endings:
            if word.removesuffix(ending) != word:
                stem = word.removesuffix(ending) # We have an adjective stem
                if stem[-1] in spelling_rule_1_letters: # Stem possibility 1
                    dict_form = stem + "ий"
                    addressed_words.append(dict_form)
                    for ending in spelling_rule_1_adjective_endings:
                        dictionary[dict_form] = dictionary.get(dict_form, 0) \
                                                + dictionary.get(stem + ending, 0) 
                        addressed_words.append(stem + ending) 
                        # try: 
                        #     del dictionary[stem + ending]
                        # except: 
                        #     continue
                        pass
                    break
                if stem[-1] in spelling_rule_2_letters: # Stem possibility 2
                     dict_form = stem + "ий"
                     addressed_words.append(dict_form)
                     for ending in spelling_rule_2_adjective_endings:
                         dictionary[dict_form] = dictionary.get(dict_form, 0) \
                                                 + dictionary.get(stem + ending, 0) 
                         addressed_words.append(stem + ending) 
                         # try: del dictionary[stem + ending]
                         # except: continue
                         pass
                     break
                if stem[-1] in spelling_rule_ц_letters: # Stem possibility ц
                     dict_form = stem + "ый"
                     addressed_words.append(dict_form)
                     for ending in spelling_rule_ц_adjective_endings:
                         dictionary[dict_form] = dictionary.get(dict_form, 0) \
                                                 + dictionary.get(stem + ending, 0) 
                         addressed_words.append(stem + ending) 
                         # try: del dictionary[stem + ending]
                         # except: continue
                         pass
                     break
                if russ_match(word, hard_adjective_endings) >= 3:
                    dict_form = stem + "ый"
                    addressed_words.append(dict_form)
                    for ending in hard_adjective_endings:
                        dictionary[dict_form] = dictionary.get(dict_form, 0) + dictionary.get(stem + ending, 0) 
                        addressed_words.append(stem + ending) 
                        # try: 
                        #     del dictionary[stem + ending]
                        # except: 
                        #     continue
                        pass
                    break
                if russ_match(word, soft_adjective_endings) >= 3:
                    dict_form = stem + "ий"
                    addressed_words.append(dict_form)
                    for ending in soft_adjective_endings:
                        dictionary[dict_form] = dictionary.get(dict_form, 0) \
                                                + dictionary.get(stem + ending, 0) 
                        addressed_words.append(stem + ending) 
                        # try: del dictionary[stem + ending]
                        # except: continue
                        pass
                    break
# Feminine Nouns
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    if word not in dictionary: continue
    if word in addressed_words: continue
    if russ_match(word, fem_hard_endings_all) >= russ_match(word, masc_hard_endings_nouns_all):
        # If this statement procs the word IS a feminine noun, but not all feminine nouns will enter, e.g. only indeterminate forms are found in dictionary :(
        for ending in fem_hard_endings_all:
            if word.removesuffix(ending) != word:
                stem = word.removesuffix(ending)
                dict_form = stem + "а"
                addressed_words.append(dict_form)
                
                if stem[-1] in spelling_rule_1_letters:
                    for ending in fem_hard_endings_spelling_1:
                        dictionary[dict_form] =  dictionary.get(dict_form, 0) \
                                                + dictionary.get(stem + ending, 0)
                        addressed_words.append(stem + ending)
                        # try: del dictionary[stem + ending]
                        # except: continue
                        pass
                    break
                pass
                if stem[-1] in spelling_rule_2_letters:
                    for ending in fem_hard_endings_spelling_2:
                        dictionary[dict_form] =  dictionary.get(dict_form, 0) \
                                                + dictionary.get(stem + ending, 0)
                        addressed_words.append(stem + ending)
                        # try: del dictionary[stem + ending]
                        # except: continue
                        pass
                    break
                # if stem[-1] in spelling_rule_ц_letters:
                #     for ending in fem_hard_endings_spelling_ц:
                #         dictionary[dict_form] =  dictionary.get(dict_form, 0) \
                #                                 + dictionary.get(stem + ending, 0)
                #         addressed_words.append(stem + ending)
                #         try: del dictionary[stem + ending]
                #         except: continue
                #         pass
                #     break
                else:
                    for ending in fem_hard_endings_default:
                        dictionary[dict_form] =  dictionary.get(dict_form, 0) \
                                                + dictionary.get(stem + ending, 0)
                        addressed_words.append(stem + ending)
                        # try: del dictionary[stem + ending]
                        # except: continue
                        pass
                    break

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         



# for ending in declension_masc_hard_endings_nouns:
#         if word.endswith(ending): # Find me words that look like they end in masc case endings (but not the nominative)
#             if word.removesuffix(ending) in dictionary and (word.removesuffix(ending) + "ом" or word.removesuffix(ending) + "ов") in dictionary:
#                 # Test IF you can remove the ending and still find a real word (still might be a feminine noun until:), AND you can add on a standard masc-only ending and still find a word...
#                 # If so, sounds like a masculine word in a
#                 dictionary[word.removesuffix(ending)] = dictionary[word.removesuffix(ending)] + dictionary.get(word, 0)

#     for condition in masc_ending:
#         if condition:
#             masc_chance = masc_chance + 1
#     if masc_chance < 3:
#         #permutate
#         #sum
#         # add all to no-fly list
        
#return(dictionary)