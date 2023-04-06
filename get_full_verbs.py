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
               "обо", "об","объ", 
               "воз", "вос", "вс", "взъ", "вз", 
               "подъ", "под",
               "надъ", "над",
               "разъ", "раз", "рас",
               "про",
               "пре",
               "ото", "отъ", "от", "о",
               "до",
               "вы",
               "из", "ис",
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

# BEING RUN INSIDE OF COMPILER, COPY CHANGES TO THERE

def root_match(word: str) -> str:
    root = "*"
    refl = word.endswith("ся") or word.endswith("сь")
    #print("\n\nRoot_Match checking word", word)
    for prefix in prefix_list: # If word starts with a prefix looking thing and you can put on any other prefix other than that prefix and the other prefix doesn't undo a mistaken prefix removal: eg. с-тавлять  вс-тавлять = в-ставлять 
        if refl:
            if word.startswith(prefix) and any(pref + word[len(prefix):] in word_list_set or (pref + word[len(prefix):-2]) in word_list_set for pref in (pf for pf in prefix_list if pf != prefix and not any(pf == undo for undo in ["вс","преду","со"])) ):
                root = word[len(prefix):]
                #print("proposed root", root)
                break
        else:
            if word.startswith(prefix) and any(pref + word[len(prefix):] in word_list_set or (pref + word[len(prefix):] + "ся") in word_list_set for pref in (pf for pf in prefix_list if pf != prefix and pf[-1] != prefix[-1] and not any(pf == undo for undo in ["вс","преду","со"])) ):
                root = word[len(prefix):]
                #print("proposed root", root)
                break
    if root.endswith("ся") or root.endswith("сь"):
        root = root[:-2]
  
    return root


def last_vowel(stem: str) -> str:
    for i in range(1, len(stem)):
        for vowel in ["а","о","ы","э","у","я","е","и","ю"]:
            if stem[-i] == vowel:
                return vowel

###############################################################################


    



word_list_set = set(word_list)

delete_words = ("пять","девять","десять","вспять","зять","память","овать")
for word in delete_words:
    if word in word_list_set:
        word_list.remove(word)


word_list_set = set(word_list)


print("Word List Ready...")
print("Getting full verbs.")
###############################################################################


# Making pair list
####################   
pair_dict = dict() 


for word in word_list:
    next_up = False
    if len(word) <= 6: continue
    if word.endswith("ться") or word.endswith("стись"): 
        word = word[:-2]
    
    elif word.endswith("ивать"): #Must check for possible stem's consonant mutations
        stem = word[:len(word) - 5]
        # выплач , заканч, рассматр, огораж, затраг, покрик
        
        
        for i in range(0, len(mutation_key)): # Going one by one through possible mutations
            #            if stem looks mutated            and    you can propose and undoal of the mutation and add "ить" to make a real word
            if stem.endswith(mutation_key[i][0]):
                # Catch о > а mutations in stem
                if last_vowel(stem) == "а": # Check to see if the stem has an "а", if so, check if an "о" replacement exists (e.g. отговорить when analyzing отговаривать), IF it exists, you may assume отговорить instead of отговарить
                    before = stem.rfind("а")
                    after = stem.rfind("а") + 1
                    if (stem[:before] + "о" + mutation_key[i][1] + "ить") in word_list_set or (stem[:before] + "о" + "нуть") in word_list_set:
                        stem = stem[:before] + "о" + stem[after:]

                    if stem[:-len(mutation_key[i][0])] + mutation_key[i][1] + "ить" in word_list_set:
                        stem = stem[:-len(mutation_key[i][0])] + mutation_key[i][1]
                        break
                    if stem[:before] + "о" + "нуть" in word_list_set:
                        pair_dict[word] = stem[:before] + "о" + "нуть"
                        next_up = True
                        break
                
            elif stem.endswith(mutation_key[i][1]):
                
                if last_vowel(stem) == "а": # Check to see if the stem has an "а", if so, check if an "о" replacement exists (e.g. отговорить when analyzing отговаривать), IF it exists, you may assume отговорить instead of отговарить
                    before = stem.rfind("а")
                    after = stem.rfind("а") + 1
                    if (stem[:before] + "о" + mutation_key[i][0] + "ать") in word_list_set or (stem[:before] + "о" + "нуть") in word_list_set:
                        stem = stem[:before] + "о" + stem[after:]
                
                if stem[:-len(mutation_key[i][1])] + mutation_key[i][0] + "ать" in word_list_set:
                    pair_dict[word] = stem[:-len(mutation_key[i][1])] + mutation_key[i][0] + "ать"
                    next_up = True
                    break
                
        if next_up: continue
        
        if last_vowel(stem) == "а": # Check to see if the stem has an "а", if so, check if an "о" replacement exists (e.g. отговорить when analyzing отговаривать), IF it exists, you may assume отговорить instead of отговарить
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
                break
        
        # # Catch consonant mutations in stem
        # if any(stem.endswith(mutation) for mutation in mutation_key):
        #     for mutation in mutation_key:
        #         if stem.endswith(mutation):
        #             stem = stem[:len(stem)-len(mutation)] + mutation_key[mutation]
        #             break
        
        # Catch о > а mutations in stem
        try:
            if last_vowel(word) == "а": # Check to see if the stem has an "а", if so, check if an "о" replacement exists (e.g. отговорить when analyzing отговаривать), IF it exists, you may assume отговорить instead of отговарить
                if (stem[:len(stem)-2] + "о" + stem[len(stem)-1] + "ить") in word_list_set:
                    stem = stem[:len(stem)-2] + "о" + stem[len(stem)-1]
        except:
            pair_dict[stem + "инать"] = word
            try:
                del pair_dict[word]
                continue
            except: continue
            
        pair_dict[word] = stem + "ить"
        pass
 
        
    elif word.endswith("нуть") and any(word.startswith(prefix) for prefix in prefix_list):
         if word.endswith("ануть"):
             pair_dict[word] = word[:-5] + "ать"
         elif word == "заснуть" or word == "уснуть" or word == "проснуть":
             stem = word[:-4]
             pair_dict[stem + "ыпать"] = word
             continue
         else:
             stem = word[:-4]
             #if any(stem.endswith(vowel) for vowel in ["а","о","э","ы","у","я","е","и","ю"]:
             
             
             pair_dict[stem + "ать"] = word
         continue
     
    
    
    
    pass
     
    # elif russ_match(word, ывать_trns_endings) > 4:
    #     for ending in ывать_trns_endings:
    #         if word.endswith(ending):
    #             stem = word[:len(word)-len(ending)]
    #             dict_form = stem + "ывать"    
    #             break
    #     pair_dict[dict_form] = stem + "ать"
    
    # Before adding these blocks in, finished the above
        
   
   

    




# Overrides:
############################################################################### 


        
        
# Clear out perfectives that look like branch imperfectives, and resest their imperfective:

# Flips fake-imperfective into perfective, and adds real imperfective
for word in list(pair_dict):
    if word.endswith("стоять"):
        del pair_dict[word]
        pair_dict[word[:-4] + "аивать"] = word
try:
    del pair_dict["противостаивать"]
except:pass
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







# Input full check of stem for these forms, and overwrite 
##########################################################

override_list = {"калывать":"колоть","крывать":"крыть", "едать":"есть","ведать":"вести","метать":"мести","ключать":"ключить","водить":"вести","дергивать":"дергать","мазывать":"мазать","даривать":"дарить","кутывать":"кутать","бегать":"бежать",
                 "кладывать":"класть", "рывать":"рвать","мирать":"мереть", "бирать": "брать", "падать":"пасть","пасать":"пасти","возить":"везти","тесывать":"тесать","становлять":"становить","вращать":"вратить","личать":"личить","прягать":"прячь",
                 "секать":"сечь", "зывать":"звать", "бывать":"быть", "бивать": "бить", "ращивать":"расти", "нимать":"нять","казывать":"казать","леживать":"лежать","клевывать":"клевать","рубать":"рубить","дивлять":"дивить","езжать":"ехать","рабатывать":"работать",
                 "плывать":"плыть","мывать":"мыть", "гонять":"гнать","вывать":"выть","нывать":"ныть","забывать":"забыть","орать":"орать","плескивать":"плескать", "слонять":"слонить","стигать":"стигнуть","ветвлять":"ветвить","мещать":"местить","толковывать":"толковать",
                 "вертывать":"вертеть","швыривать":"швырнуть","сыпать":"сыпать","тягивать":"тянуть","пускать":"пустить","жидать":"ждать","брасывать":"бросать","хлестывать":"хлестать", "стригать":"стричь","целивать":"целить","таскивать":"таскать","слушивать":"слушать",
                 "тирать":"тереть","буждать":"будить","плетать":"плести","влекать":"влечь","тыкать":"ткнуть","берегать":"беречь","читывать":"читать","давать":"дать", "шибать":"шибить","рекать":"речь","гублять":"губить","лезать":"лезть","сыхать":"сохнуть",
                 "трагивать":"трогать","лизывать":"лизать","касать":"каснуть","сматривать":"смотреть","равнивать":"ровнять","равнять":"равнить","кипать":"кипеть","воротить":"ворачивать","шаривать":"шарить","далбливать":"долбить","молатывать":"молоть","корять":"корить",
                 "жигать":"жечь","ражать":"разить","драгивать":"дрожать","льщать":"льстить","зревать":"зреть", "ванивать":"вонять","ласкивать":"ласкать","черкивать":"черкать","волакивать":"волочь","давлять":"давить","летать":"лететь","страшать":"страшить","пугивать":"пугать","баивать":"боять",
                 "зирать":"зреть","мечать":"метить","пинать":"пнуть","горать":"гореть","минать":"мять","гребать":"грести","значать":"значить","хмуривать":"хмурить","еживать":"ежить","ряжать":"рядить","волновать":"волновать","ползать":"ползти","носить":"нести",
                 "чинивать":"чинить","чинять":"чинить","гибать":"гибать","качивать":"качать","следовать":"следовать","цветать":"цвести","хваливать":"хвалить","сылать":"слать","манивать":"манить","блуждать":"блудить","цапать":"цапывать","сачивать":"сочить",
                 "решать":"решить","гружать":"грузить","бредать":"брести","винчивать":"винтить","ливать":"лить","вивать":"вить","мучивать":"мучить","молять":"молить","рушать":"рушить","кушивать":"кушать","селять":"селить","мешивать":"мешать","сверливать":"сверлить",
                 "пихивать":"пихать","растать":"расти","ронять":"ронить","топать":"тонуть","теривать":"терять", "мыкать":"мкнуть","дыхать":"дохнуть","капливать":"копить","морщивать":"морщить", "жирать":"жрать","целовывать":"целовать","стывать":"стыть",
                 "пекать":"печь","вирать":"врать","лыгать":"лгать","тушать":"тушить","стаивать":"стоить","грызать":"грызть","седать":"сесть","гревать":"греть","дувать":"дуть","маивать":"маять","мигивать":"мигать","цеплять":"цепить","увечивать":"увечить","ступать":"ступить",
                 "таивать":"таить","манывать":"мануть","шагивать":"шагать","стерегать":"стеречь","хлынивать":"хлынуть","плавливать":"плавить","валивать":"валить","купать":"купить","прятывать":"прятать","вевать":"веять","хаживать":"ходить","гнетать":"гнести",
                 "станывать":"стонать","шипывать":"шипеть","званивать":"звонить","звенивать":"звенеть","сапывать":"сопеть","хрипывать":"хрипеть","жевывать":"жевать", "девать":"деть","грабастывать":"грабастать","путывать":"путать","кращать":"кратить",
                 "пискивать":"пищать","храмывать":"хромать","жинать":"жать","жимать":"жать","мелькивать":"мелькать","тряхивать":"трясти", "храпывать":"храпеть","стукивать":"стучать","треблять":"требить","дваивать":"двоить","колачивать":"колотить","калечивать":"калечить",
                 "глядывать":"глядеть","длевать":"длить","рождать":"родить","спаривать":"спорить","стегивать":"стегать","бадривать":"бодрить","даивать":"доить","совывать":"совать","двигать":"двигать","поминать":"помнить","карабкивать":"карабкать","скакивать":"скочить",
                 }

with open("dictionary_forms.pkl", "rb") as f:
    dictionary_forms = pickle.load(f)
all_infinitives = list()

for key in dictionary_forms:
    if dictionary_forms[key].endswith("ть") or dictionary_forms[key].endswith("ться") or dictionary_forms[key].endswith("сти") or dictionary_forms[key].endswith("стись"):
        all_infinitives.append(dictionary_forms[key])

all_infinitives = list(set(all_infinitives))

for i in range(0, len(all_infinitives)):
    if all_infinitives[i].endswith("ться") or all_infinitives[i].endswith("тись"):
        all_infinitives[i] = all_infinitives[i][:-2]

# Our pair list is arranged as imperfective:perfective. We catch verb pairs from the database
# by catching the imperfective (almost always -ывать/-ивать). A handful of verbs
# end in these endings in the imperfective, but their perfective form ends in a non-routine
# form, e.g. откалывать - отколоть. 

for word in list(pair_dict):
    if any(word.endswith(imp) for imp in override_list) or not any(word.startswith(pref) for pref in prefix_list):
        try: del pair_dict[word]
        except:pass

for override_imp in override_list: # For each imperfective form, tied to a perfective override
    print(f"\n\nChecking for {override_imp}:")
    for imperfective in [imperfective for imperfective in all_infinitives if root_match(imperfective) == override_imp]:
        print(f"For {override_imp} found {imperfective}")
        pair_dict[imperfective] = (imperfective[:len(imperfective)-len(override_imp)] + override_list[override_imp])
    
# For each pair we made up above, look at the imperfective, and remove the prefix,
# Does this form now look like the override's imperfective? If so, we found one
# of the pairs for which we should: set the perfective of that 'entry' equal to
# the entry's prefix + the corresponding perfective tied to the given 
# imperfective, from the override list. 
# e.g. We find скрывать, it matches крывать, therefore с- + крыть is its REAL perfective.
    


# two different branch perfectives correspond to: -таивать (таить таять) -капывать (копать капать)

 
###############################################################################

  
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





# Iterative roots shouldn't come up as pairs
iterative_forms = ["певать", "говаривать","леживать","стреливать","едать"]
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
        if prefix + root in pair_dict or prefix + root + "ся" in pair_dict or prefix + root + "сь" in pair_dict:
            if "  " + prefix + "-" not in words_prefixes.get(root,""):
                words_prefixes[root] = words_prefixes.get(root,"") + "  " + prefix + "-"
 
 # Fill in the branch inperfective forms by rootmatching the prefixed imperfectives
for word in pair_dict:
   imp_root = root_match(word)
   
   if imp_root in override_list:
       perf_root = override_list[imp_root]
   else:
       perf_root = root_match(pair_dict[word])
   
   #print(word, imp_root, perf_root, words_prefixes.get(imp_root, ""))
   tree_dict[perf_root] = ["-" + imp_root, words_prefixes.get(imp_root, "")] 



# I have NO IDEA why this is necessary and not executed by above
tree_dict["казать"] = ["-" + "казывать", words_prefixes.get("казывать", "")]
 
# Unite these two spellings into one entry
doubled_roots = {"искать":"ыскать","играть":"ыграть"}
for correct in doubled_roots:
    try: imp = tree_dict.get(correct,"")[0]
    except: continue
    prefs = tree_dict.get(correct,"")[1]
    more_prefs = tree_dict.get(doubled_roots[correct], "")[1]
    tree_dict[correct] = (imp, prefs + more_prefs)
    del tree_dict[doubled_roots[correct]]





# Tree list overrides:
    
# tree_overrides = {"имать":"-ять"}
# for imperfective in tree_overrides:
#     tree_dict[imperfective] = [tree_overrides[imperfective] ,  (words_prefixes.get(root, "")) ]



for key in list(tree_dict):
    if key.startswith("ъ"):
        del tree_dict[key]
    elif tree_dict[key][1].startswith("ъ"):
        del tree_dict[key]

try: del tree_dict["ать"] # Faulty interpretation of взывать as вз-ывать
except:pass
try: del tree_dict["елить"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass
try: del tree_dict["елать"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass
try: del tree_dict["ить"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass
try: del tree_dict["авить"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass
try: del tree_dict["тавить"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass
try: del tree_dict["тучить"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass
try: del tree_dict["кать"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass
try: del tree_dict["ть"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass
try: del tree_dict["адить"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass
try: del tree_dict["овать"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass
try: del tree_dict["аить"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass    
try: del tree_dict["орить"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass   
try: del tree_dict["ять"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass  
try: del tree_dict["глянуть"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass  
try: del tree_dict["кинуть"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass  
try: del tree_dict["мыкать"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass  
try: del tree_dict["чать"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass  
try: del tree_dict["стрить"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass 
try: del tree_dict["острить"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass 
try: del tree_dict["рить"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass 
try: del tree_dict["падать"] # produced by the rare overlap of на-делить в-селить mixing as над-елить вс-елить
except:pass 

# Certain prefixes naturally gain a vowel to prevent consonant clusters.
# When an imperfective is converted to its perfective form, consonant arrangements
# Can change in a subset of verbs, causing the vowel to appear, e.g. -рывать -рвать
# Fixing consonant cluster mistakes

#Build me a dictioanry with all the clusters as keys and their opened up form as values
clusters = dict()
for start in ["от","раз","об","с","под","над","вз","в"]:
    for end in ["рв","зв","гн","ткн","мкн"]:
        clusters[start+end] = start+"о"+end

# Go through the pairs, if the perfective contains a cluster, replace it with the opened form
for word in pair_dict:
    for cluster in clusters:
        if cluster in pair_dict[word]:
            mismade_word = pair_dict[word]
            pair_dict[word] = mismade_word.replace(cluster, clusters[cluster])
# If you find "отрв" in the perfective of a pair (that is, the one we generated,
# not the one we found naturalistically), take that word and replace the cluster
# with the corresponding fix.


###############################################################################
# Returning to the pair list to add in the reflexives which... Don't matter as much to show in tree model

for word in list(pair_dict):
    if word + "ся" in word_list_set:
        if pair_dict[word].endswith("и"):
                pair_dict[word + "ся"] = pair_dict[word] + "сь"
        else:
            pair_dict[word + "ся"] = pair_dict[word] + "ся"
    elif word + "сь" in word_list_set:
        if pair_dict[word].endswith("и"):
                pair_dict[word + "сь"] = pair_dict[word] + "сь"
        else:
            pair_dict[word + "сь"] = pair_dict[word] + "ся"

###############################################################################    
def ignore_suffix_and_flip_backwards(word:str) -> str:
    if word.endswith("ся") or word.endswith("сь"):
        word = word[:-2]
    word = word[::-1]
    return word


# Sorting pair dictionary by root, by sorting back to front of the word alphabetically
pair_dict = {v: k for k, v in pair_dict.items()}
pair_dict_sub = dict()
alphabetized_list = sorted(pair_dict.keys(), key = lambda x: ignore_suffix_and_flip_backwards(x))

for key in alphabetized_list:
    pair_dict_sub[key] = pair_dict[key]

pair_dict = pair_dict_sub


# Sorting for trees occurs in front_face_tree.py, whose function is called in website__init.py

with open("pair_list.pkl", "wb") as f:
    pickle.dump(pair_dict, f)


with open("tree_list.pkl", "wb") as f:
    pickle.dump(tree_dict, f)

print("Verb lists saved to pickles.")
