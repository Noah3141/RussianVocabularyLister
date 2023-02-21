# Master Lists Creation
      
def create_verb_list(reference_dictionary):
  

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
    
    for word in reference_dictionary:
        if word.endswith("ивать"): #Must check for possible stem's consonant mutations
            word.removesuffix("ивать")
            pair_dictionary[word] = word.removesuffix("ивать") + "ить"
    
        if word.endswith("ывать"): #Must check for shortlist -ы- infix words, and shortlist -вать words -- exceptions.
            pair_dictionary[word] = word.removesuffix("ывать") + "ать"
    pass







                                ## Creating verb Tree lists ##
    prefix_list = ["в", "на","с","воз","вос"] 

    tree_dictionary = dict()

    for word in pair_dictionary: 
        for prefix in prefix_list:
            if word.startswith(prefix):
                word.removeprefix(prefix)
                
        
    return(pair_dictionary, tree_dictionary) 