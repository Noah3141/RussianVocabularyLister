###############################################################################

# This script is run as an admin on a PC for creating updated .pkl files.
# Those .pkl files can then be pushed to the GIT repository, for use in the site.

# This file pulls the database, and creates a .pkl file, to push to GIT.

###############################################################################
###############################################################################

#  #  #  #  #  #  #  #  #  #  #   WARNING  #  #  #  #   #  #  #  #   #  #  #  #
#                 RESETS SOME USER UPDATES TO SCRIPT OUTPUT                   #                           
###############################################################################
###############################################################################


import pickle


with open("dictionary_forms.pkl", "rb") as f:
    word_dict = pickle.load(f)

word_list = list()
for value in word_dict.values():
    word_list.append(value)
    
word_list = list(set(word_list))
###############################################################################



ывать_trns_endings = ["ывать", "ываю","ываешь","ывает","ываем","ываете","ывают",
                    "ывал", "ывало","ывала","ывали",
                    "ывая", "ывай", "ывайте"]

ать_trns_endings = ["ать", "аю","аешь","ает","аем","аете","ают",
                    "ал", "ало","ала","али",
                    "ая", "ай", "айте"]


spelling_rule_1_letters = ["г", "к", "х"]
spelling_rule_2_letters = ["ж", "ч", "ш", "щ"]


mutation_key = [("пл","п"),   # mutation_key, list
                ("бл","б"),   # mutation_key[1] = tuple
                ("фл","ф"),   # mutation_key[1][1] = unmutated
                ("вл","в"),   # mutation_key[1][0] = mutated
                ("мл","м"),
                ("ч","к"),
                ("ч", "т"),
                ("ж","з"),
                ("ж", "д"),
                ("ж", "г"),
                ("ш","с"),
                ("ш", "х"),
                ("щ","ст"),
                ("щ","ск")]

# If ends in ивать and ends in mutated, then check for score on coverted roots + ить ил ило ила
# закручивать закрукать закрутить
#
#
#
#
###############################################################################


def russ_match(word: str, ending_list: list) -> int:
    match = 0
    if any(word.endswith(ending) for ending in ending_list):
        match = 1
        for ending in ending_list:
            if word.endswith(ending):
                stem = word[:len(word)-len(ending)]
                for other_ending in (e for e in ending_list if e != ending):
                    if stem + other_ending in word_list_set:
                        match += 1
                break
    print(f'{word} checked for {ending_list} reached {match}')
    #print("Match calculated for", word, "against", ending_list, "as", match)
    return match  

# Longest to shortest, fractally, with hard signs before their counterpart: else it won't work in root_match()
prefix_list = ["преду", "предъ", "пред",
               "пере",
               "при",
               "обо", "об","объ", "о",
               "воз", "вос", "вс", "взъ", "вз", 
               "подъ", "под",
               "надъ", "над",
               "разъ", "раз", "рас",
               "про",
               "пре",
               "ото", "отъ", "от",
               "до",
               "вы",
               "на",
               "за",
               "по",
               "со", "съ", "с",
               "в",
               "у"] 

# prefix_list = ["преду", "пред",
#                "пере",
#                "при",
#                "обо", "об", "о",
#                "воз","вос", "вс", "вз", 
#                "под",
#                "раз", "рас",
#                "про",
#                "пре",
#                "ото", "от",
#                "до",
#                "вы",
#                "на",
#                "за",
#                "по",
#                "со", "с",
#                "в",
#                "у"] 

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


def root_match(word: str) -> str:
    root = "*"
    #print("\n\nRoot_Match checking word", word)
    for prefix in prefix_list:
        if word.startswith(prefix) and any(pref + word[len(prefix):] in word_list_set for pref in (pf for pf in prefix_list if pf != prefix) ):
            root = word[len(prefix):]
            #print("proposed root", root)
            break
    if root == "*":
        root == word
    return root


def last_vowel(stem: str) -> str:
    for i in range(1, len(stem)):
        for vowel in ["а","о","ы","э","у","я","е","и","ю"]:
            if stem[-i] == vowel:
                return vowel

###############################################################################


    


word_list_set = set(word_list)


delete_words = ("пять","девять","десять","вспять","зять","память")
for word in delete_words:
    if word in word_list_set:
        word_list.remove(word)
 
print("Word List Ready...")
print("Getting full verbs.")
###############################################################################


# Making pair list
####################   
pair_dict = dict() 


for word in word_list:
    if len(word) <= 6: continue

    
    if word.endswith("ивать"): #Must check for possible stem's consonant mutations
        stem = word[:len(word)-len("ивать")]
        # выплач , заканч, рассматр, огораж
        
        
        for i in range(0, len(mutation_key)): # Going one by one through possible mutations
            #            if stem looks mutated            and    you can propose and undoal of the mutation and add "ить" to make a real word
            if stem.endswith(mutation_key[i][0]):
                # Catch о > а mutations in stem
                if last_vowel(stem) == "а": # Check to see if the stem has an "а", if so, check if an "о" replacement exists (e.g. отговорить when analyzing отговаривать), IF it exists, you may assume отговорить instead of отговарить
                    before = stem.rfind("а")
                    after = stem.rfind("а") + 1
                    if (stem[:before] + "о" + mutation_key[i][1] + "ить") in word_list_set:
                        stem = stem[:before] + "о" + stem[after:]

                if stem[:-len(mutation_key[i][0])] + mutation_key[i][1] + "ить" in word_list_set:
                    stem = stem[:-len(mutation_key[i][0])] + mutation_key[i][1]
                    break
            elif last_vowel(stem) == "а": # Check to see if the stem has an "а", if so, check if an "о" replacement exists (e.g. отговорить when analyzing отговаривать), IF it exists, you may assume отговорить instead of отговарить
                before = stem.rfind("а")
                after = stem.rfind("а") + 1
                if (stem[:before] + "о" + stem[after:] + "ить") in word_list_set:
                    stem = stem[:before] + "о" + stem[after:]
                    
                    
        # # Catch consonant mutations in stem
        # if any(stem.endswith(mutation) for mutation in mutation_key):
        #     for mutation in mutation_key:
        #         if stem.endswith(mutation) and stem + mutation_key[mutation] in word_list:
        #             stem = stem[:len(stem)-len(mutation)] + mutation_key[mutation]
        #             break
        
        
        if len(stem) <= 2:
            pair_dict[word] = stem + "ить"
            continue

       
        
        if stem[-1] in (spelling_rule_1_letters or spelling_rule_2_letters):
            pair_dict[word] = stem + "ать"
        else:
            pair_dict[word] = stem + "ить"

    






    elif word.endswith("ывать"): #Must check for shortlist -ы- infix words, and shortlist -вать words -- exceptions.
        stem = word[:len(word)-len("ывать")]
        # смотать сматывать cмат
        # разбросать разбрасывать разбрас

        
        # Catch consonant mutations in stem
        # if any(stem.endswith(mutation) for mutation in mutation_key):
        #     for mutation in mutation_key:
        #         if stem.endswith(mutation):
        #             stem = stem[:len(stem)-len(mutation)] + mutation_key[mutation]
        #             break
        
        
        
        # Catch о > а mutations in stem
        if last_vowel(stem) == "а": # Check to see if the stem has an "а", if so, check if an "о" replacement exists (e.g. отговорить when analyzing отговаривать), IF it exists, you may assume отговорить instead of отговарить
            before = stem.rfind("а")
            after = stem.rfind("а") + 1
            if (stem[:before] + "о" + stem[after:] + "ать") in word_list_set or (stem[:before] + "о" + stem[after:] + "ить") in word_list_set:
                stem = stem[:before] + "о" + stem[after:]

        
        pair_dict[word] = stem + "ать"
    
    
    
    
    elif word.endswith("ять"):
        stem = word[:len(word)-len("ять")]
        
        # поставить поставлять поставл
        # селять
        #
        
        for i in range(0, len(mutation_key)): # Going one by one through possible mutations
            #            if stem looks mutated            and    you can propose and undoal of the mutation and add "ить" to make a real word
            if stem.endswith(mutation_key[i][0]) and stem[:-len(mutation_key[i][0])] + mutation_key[i][1] + "ить" in word_list_set:
                stem = stem[:-len(mutation_key[i][0])] + mutation_key[i][1]
        
        # # Catch consonant mutations in stem
        # if any(stem.endswith(mutation) for mutation in mutation_key):
        #     for mutation in mutation_key:
        #         if stem.endswith(mutation):
        #             stem = stem[:len(stem)-len(mutation)] + mutation_key[mutation]
        #             break
        
        # Catch о > а mutations in stem
        try:
            if stem[-2] == "а": # Check to see if the stem has an "а", if so, check if an "о" replacement exists (e.g. отговорить when analyzing отговаривать), IF it exists, you may assume отговорить instead of отговарить
                if (stem[:len(stem)-2] + "о" + stem[len(stem)-1] + "ить") in word_list_set:
                    stem = stem[:len(stem)-2] + "о" + stem[len(stem)-1]
        except:
            pair_dict[stem + "инать"] = word
            try:
                del pair_dict[word]
                continue
            except: continue
            
        pair_dict[word] = stem + "ить"

    # # откинуть - откидать, отряхнуть - отрясать
    elif word.endswith("нуть"):
        if word.endswith("ануть"):
            pair_dict[word] = word[:-5] + "ать"
        else:
            pair_dict[word] = word[:-4] + "ать"
        continue
        

    
    # elif russ_match(word, ывать_trns_endings) > 4:
    #     for ending in ывать_trns_endings:
    #         if word.endswith(ending):
    #             stem = word[:len(word)-len(ending)]
    #             dict_form = stem + "ывать"    
    #             break
    #     pair_dict[dict_form] = stem + "ать"
    
    # Before adding these blocks in, finished the above
        

   

    




# Overrides:
############  


        
        
# Clear out perfectives that look like branch imperfectives, and resest their imperfective:

# Flips fake-imperfective into perfective, and adds real imperfective
for word in list(pair_dict):
    if word.endswith("стоять"):
        del pair_dict[word]
        pair_dict[word[:-4] + "аивать"] = word
del pair_dict["противостаивать"]

for word in list(pair_dict):
    if word.endswith("кашлять"):
        del pair_dict[word]
        pair_dict[word[:-3] + "ивать"] = word
        
for word in list(pair_dict):
    if word.endswith("стрелять"):
        del pair_dict[word]
        pair_dict[word[:-3] + "ивать"] = word
        
for word in list(pair_dict):
    if word.endswith("гулять"):
        del pair_dict[word]
        pair_dict[word[:-3] + "ивать"] = word
        
for word in list(pair_dict):
    if word.endswith("сеять"):
        del pair_dict[word]
        pair_dict[word[:-3] + "ивать"] = word
  
        
  
    
# Overwrites faulty perfective
    
for word in list(pair_dict):
    if word.endswith("страивать"):
        del pair_dict[word]
        pair_dict[word] =  word[:-6] + "оить"
        
for word in list(pair_dict):
    if word.endswith("держивать"):
        del pair_dict[word]
        pair_dict[word] =  word[:-5] + "ать"


# Override all prefixed forms

override_list = {"калывать":"колоть","крывать":"крыть",
                 "кладывать":"ложить", "рывать":"рвать","мирать":"мереть", "бирать": "брать",
                 "секать":"сечь", "зывать":"звать", "бывать":"быть", "бивать": "бить", "ращивать":"расти", 
                 "плывать":"плыть","мывать":"мыть", "гонять":"гнать","вывать":"выть","нывать":"ныть"}
# Our pair list is arranged as imperfective:perfective. We catch verb pairs from the database
# by catching the imperfective (almost always -ывать/-ивать). A handful of verbs
# end in these endings in the imperfective, but their perfective form ends in a non-routine
# form, e.g. откалывать - отколоть. 

for override_imp in override_list: # For each imperfective form, tied to a perfective override
    for imperfective in [imperfective for imperfective in pair_dict if root_match(imperfective) == override_imp]:
        pair_dict[imperfective] = (imperfective[:len(imperfective)-len(override_imp)] + override_list[override_imp])
    
# For each pair we made up above, look at the imperfective, and remove the prefix,
# Does this form now look like the override's imperfective? If so, we found one
# of the pairs for which we should: set the perfective of that 'entry' equal to
# the entry's prefix + the corresponding perfective tied to the given 
# imperfective, from the override list. 
# e.g. We find скрывать, it matches крывать, therefore с- + крыть is its REAL perfective.
    
 
    
# These words got caught by their PERFECTIVE, and so this block does the converse
# of the above.

нятьs = [word for word in pair_dict if root_match(word) == "нять"]
for нять_word in нятьs:    
    del pair_dict[нять_word]
    pair_dict[(нять_word[:len(нять_word)-4] + "нимать")] = нять_word
    

# The above overrides rely on being able to peel out a root from prefixes.
# If a found entry is completely unprefixed, it needs different processing:
unprefixed_override_list = {"бывать":"быть", "брать":"взять", "учитывать":"учесть","говорить":"сказать"}
for imp in unprefixed_override_list:
    try: del pair_dict[imp]
    except: pass
    pair_dict[imp] = unprefixed_override_list[imp]




# Certain prefixes naturally gain a vowel to prevent consonant clusters.
# When an imperfective is converted to its perfective form, consonant arrangements
# Can change in a subset of verbs, causing the vowel to appear, e.g. -рывать -рвать
# Fixing consonant cluster mistakes
clusters = dict()
for start in ["от","раз","об","с","под","над","вз"]:
    for end in ["рв","зв","гн"]:
        clusters[start+end] = start+"о"+end


for word in pair_dict:
    for cluster in clusters:
        if cluster in pair_dict[word]:
            mismade_word = pair_dict[word]
            pair_dict[word] = mismade_word.replace(cluster, clusters[cluster])
# If you find "отрв" in the perfective of a pair (that is, the one we generated,
# not the one we found naturalistically), take that word and replace the cluster
# with the corresponding fix.

# Iterative roots shouldn't come up as pairs
iterative_forms = ["певать", "говаривать","леживать"]
for imp in iterative_forms:
    try: del pair_dict[imp]
    except: continue



    
###############################################################################

#                                                       key/word       value
#                                        PAIR LIST = {imperfective: perfective}
# Making tree list from the pair list
####################   

root_list = list()
tree_dict = dict()
words_prefixes = dict() 

# # Find Roots
for imperfective in pair_dict:
    root = root_match(imperfective)
    root_list.append(root)

    
       
# Find prefixes those roots go with   
 
for root in root_list:
    for prefix in prefix_list:
        if prefix + root in pair_dict:
            if prefix not in words_prefixes.get(root,""):
                words_prefixes[root] = words_prefixes.get(root,"") + "  " + prefix + "-"
 
    
 # Fill in the branch inperfective forms by rootmatching the prefixed imperfectives
for word in pair_dict:
   root = root_match(word)
   tree_dict[root_match(pair_dict[word])] = ("-" + root, words_prefixes.get(root, "")) 

 

doubled_roots = {"искать":"ыскать","играть":"ыграть"}
for correct in doubled_roots:
    tree_dict[correct] = tree_dict.get(correct,"")[1] + tree_dict.get(doubled_roots[correct], "")[1] 
    del tree_dict[doubled_roots[correct]]





# Tree list overrides:
    
tree_overrides = {"имать":"-ять"}
for imperfective in tree_overrides:
    tree_dict[imperfective] = [tree_overrides[imperfective] ,  (words_prefixes.get(root, "")) ]



for key in list(tree_dict):
    if key.startswith("ъ"):
        del tree_dict[key]
    elif tree_dict[key][1].startswith("ъ"):
        del tree_dict[key]


del tree_dict["ать"] # Faulty interpretation of взывать as вз-ывать
del tree_dict["елить"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
###############################################################################    


pair_dict = {v: k for k, v in pair_dict.items()}
pair_dict_sub = dict()
alphabetized_list = sorted(pair_dict.keys(), key = lambda x: x[::-1])

for key in alphabetized_list:
    pair_dict_sub[key] = pair_dict[key]

pair_dict = pair_dict_sub

with open("pair_list.pkl", "wb") as f:
    pickle.dump(pair_dict, f)


with open("tree_list.pkl", "wb") as f:
    pickle.dump(tree_dict, f)

print("Verb lists saved to pickles.")
