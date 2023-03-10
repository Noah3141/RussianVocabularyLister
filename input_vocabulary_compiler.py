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

with open("dictionary_forms.pkl", "rb") as f:
    dictionary_forms = pickle.load(f)

def rubit(input_text, breadth, style) -> dict:
    del_list = ()
    output_dictionary = {}
    
        # cleaning text
    input_text = re.sub("[А-Я]{2, 10}+", "", input_text) # Acronym/Abbreviation filter (more of a cultural than vocabulary thing)
    input_text = re.sub("[А-Я]\.\s", "", input_text)
    input_text = input_text.lower() # Now lowercase words, e.g. beginning of sentence
    input_text = re.sub("[0-9]", "", input_text) # Remove any digits
    input_text = re.sub('[()[\]{}\-"—«»]', "", input_text) # Remove special symbols, especially Russian «» chevron quotes and their beloved m-dash
    input_russian_words = re.findall("([а-я]+)", input_text) # Now find me all the sequences of Russian letters (e.g. "words")
        
    
    input_count = {}
    
    stop_words = list()
    stop_words_txt = open("stop_words.txt", 'r', encoding='UTF-8')
    for line in stop_words_txt:
        stop_words.append(line.rstrip())

    
    
    # Creating raw count of inflected forms
    for word in input_russian_words:
        if word in stop_words:
            continue
        input_count[word] = input_count.get(word, 0) + 1
    
    
    dictionary_input_words = {}
    
    for word in input_count:
        try: 
            dict_form = dictionary_forms[word]
            dictionary_input_words[dict_form] = dictionary_input_words.get(dict_form, 0) + input_count.get(word, 0)
        except:
            dictionary_input_words[word] = "*"
        
    
    output_dictionary = dictionary_input_words
    
###############################################################################    
    
    # Breadth
    
    if breadth == "Top Words":
        for word in output_dictionary:
            if output_dictionary[word] <= 4: # Filter certain threshold of words
                del_list.append(word)
                pass

    if breadth == "Broad List":
       for word in output_dictionary:
           if output_dictionary[word] <= 1: # Filter certain threshold of words
               del_list.append(word)
               pass
               
    for word in del_list:
        del output_dictionary[word]
    
    # Style
    #################################################### In need of update to phase out "reference_lists_creator" and "create_verb_list"
    if style == "Verb Pairs":
        output_dictionary, _ = create_verb_list(output_dictionary)

    if style == "Verb Trees":
        _ , output_dictionary = create_verb_list(output_dictionary)
    

    return output_dictionary