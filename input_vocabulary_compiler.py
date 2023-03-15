###############################################################################

# This is the script to take inputted Russian text, and return a lemmatized
# dictionary. Input is passed through website__init.py as a POST request
# on the input page, and fed into the HTML of the output page, to display the
# user's vocabulary list.

# This is the file that utilizes the dictionary_forms.pkl (arranged as 
# key = word:value = dictionary form

###############################################################################
###############################################################################


import re
import pickle
from reference_lists_creator import create_verb_list


# Cleans user input, then creates a dictionary_input_words which is used to generate
# the HTML for the output page. Words that are not in the key are given a label instead
# of a dictionary form, and that input word is entered into the "morfo" pickle, to be later updated
# by "from auto_update_dictionary_by_user_input import update_dictionary" in website__init.py

def rubit(input_text: str, breadth: str, style: str) -> dict:
    
    
    try:
        with open("dictionary_forms.pkl", "rb") as f:
            dictionary_forms = pickle.load(f)
    except:
        raise FileNotFoundError("No dictionary_forms.pkl found! Run get_reference_russian_key.py")
    
    del_list = []
    dictionary_input_words = {}
    
        # cleaning text

    input_text = re.sub("ё", "е", input_text)
    input_text = re.sub("[А-Я]{2, 10}+", "", input_text) # Acronym/Abbreviation filter (more of a cultural than vocabulary thing)
    input_text = re.sub("[А-Я]\.\s", "", input_text)
    
    input_text = input_text.lower() # Now lowercase words, e.g. beginning of sentence
    input_text = re.sub('([а-я]+-[а-я]+)', "", input_text)
    
    input_text = re.sub("[0-9]", "", input_text) # Remove any digits
    input_text = re.sub('[()[\]{}\-"—«»]', "", input_text) # Remove special symbols, especially Russian «» chevron quotes and their beloved m-dash
    input_russian_words = re.findall("([а-я]+)", input_text) # Now find me all the sequences of Russian letters (e.g. "words")
        
    
    input_count = {}
    
    stop_words = set()
    stop_words_txt = open("stop_words.txt", 'r', encoding='UTF-8')
    for line in stop_words_txt:
        stop_words.add(line.rstrip())
    
    
    
    # Creating raw count of inflected forms
    for word in input_russian_words:
        if word in stop_words:
            continue
        input_count[word] = input_count.get(word, 0) + 1
    
    
    try:
        with open("morfo_list.pkl", "rb") as f:
            morfo = pickle.load(f)
    except:
        morfo = list()
         
    
    for word in input_count:
        try: 
            dict_form = dictionary_forms[word]
            dictionary_input_words[dict_form] = dictionary_input_words.get(dict_form, 0) + input_count.get(word, 0)
        except:
            dictionary_input_words[word] = "*"
            if word not in morfo:
                morfo.append(word)
        
        
    with open("morfo_list.pkl", "wb") as f:
        pickle.dump(morfo, f)
            
        
    dictionary_input_words = {k: v for k, v in sorted(dictionary_input_words.items(), key=lambda item: (isinstance(item[1], int), item[1]), reverse=True)}
    
###############################################################################    
    
    # Breadth
    
    try: 
        ave_count = (sum(dictionary_input_words.values()) / len(dictionary_input_words))
    except: ave_count = 0
    
    if breadth == "Top Words":
        for word in dictionary_input_words:
            if dictionary_input_words[word] <= (ave_count): # Filter certain threshold of words
                del_list.append(word)
                pass

    if breadth == "Broad List":
       for word in dictionary_input_words:
           if dictionary_input_words[word] <= (ave_count - 1): # Filter certain threshold of words
               del_list.append(word)
               pass
               
    for word in del_list:
        del dictionary_input_words[word]
    
    # Style
    #################################################### In need of update to phase out "reference_lists_creator" and "create_verb_list"
    if style == "Verb Pairs":
        dictionary_input_words, _ = create_verb_list(dictionary_input_words)

    if style == "Verb Trees":
        _ , dictionary_input_words = create_verb_list(dictionary_input_words)
    

    return dictionary_input_words, input_count