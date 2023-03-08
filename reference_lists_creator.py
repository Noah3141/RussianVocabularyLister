# Master Lists Creation
      
def create_verb_list(dictionary):
  

###############################################################################
                                ## Creating verb pair list ##
    addressed_words = list() # Working from exceptions inwards (to broader scale blocks), add finished pairs to a list and stop addressing them
    pair_dictionary = dict()

    # -ы- infix pairs:
# More specifically, those verbs that take a -ы-/-и- stem change rather than a simple suffix
    infixed_ы_verbs = ["мереть", "мирать",
                       "звать", "зывать",
                       "переть", "пирать",
                       "брать", "бирать",
                       "тереть", "тирать",
                       "спать", "сыпать",
                       "мять", "минать",
                       "жать", "жимать", # -жинать has been thrown to the wolves...
                       ]


    # -сти verbs б д с 
# грести - гребать, спасти - спасать

    
    # -вать
#
    
    for word in dictionary:
        if word.endswith("ивать"): #Must check for possible stem's consonant mutations
            
            pair_dictionary[word] = word[:len(word)-len("ивать")] + "ить"
    
        elif word.endswith("ывать"): #Must check for shortlist -ы- infix words, and shortlist -вать words -- exceptions.
            pair_dictionary[word] = word[:len(word)-len("ывать")] + "ать"
        
        elif word.endswith("ять"):
            pair_dictionary[word] = word[:len(word)-len("ять")] + "ить"







                                ## Creating verb Tree lists ##
    prefix_list = ["при", "по", "от", "об", "о", "вы","в", "на","с", "со",
                   "воз","вос", "вс", "вз", "под", "раз", "про","до",
                   "за","рас"] 

    tree_dictionary = dict()

    for word in pair_dictionary: 
        for prefix in prefix_list:
            if word.startswith(prefix):
                root = "-" + word.removeprefix(prefix)
                if root not in tree_dictionary:
                    tree_dictionary[root] = [prefix + "-"]
                else:
                    tree_dictionary[root].append([prefix + "-"])
                
        
    return(pair_dictionary, tree_dictionary) 