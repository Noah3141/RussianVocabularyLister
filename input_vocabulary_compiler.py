import re
import pickle
from russian_inflection_collapser import ruic 
# This file supposed to take:
# 1) WebCrawler's master list (RUBIT'ed)
# 2) Input from user from website (RUBIT'ed)
# and create an output file that:
# 1) follows the settings from the site (broad, full, tree, pairs)
# 2) creates a table with:
    # A) entry word from input
    # B) frequency in input
    # C) indicator(s) of frequency in master list
    # D) culled entries by breadth setting
    # E) grouped/ordered entries by Output_Style setting 


def rubit(input_text, breadth, style):
    input_dictionary = dict()
    ruic_input_dictionary = dict()
    
    # cleaning text
    input_text = re.sub("[А-Я]{2, 10}+", "", input_text) # Acronym/Abbreviation filter (more of a cultural than vocabulary thing)
    input_text = re.sub("[А-Я]\.\s", "", input_text)
    input_text = input_text.lower() # Now lowercase words, e.g. beginning of sentence
    input_text = re.sub("[0-9]", "", input_text) # Remove any digits
    input_text = re.sub('[()[\]{}\-"—«»]', "", input_text) # Remove special symbols, especially Russian «» chevron quotes and their beloved m-dash
    input_russian_words = re.findall("([а-я]+)", input_text) # Now find me all the sequences of Russian letters (e.g. "words")
    
    # Creating raw dictionary
    for word in input_russian_words:
        input_dictionary[word] = input_dictionary.get(word, 0) + 1
    
    # Importing stop words and removing from input dictionary
    stop_words = list()
    stop_words_txt = open("stop_words.txt", 'r', encoding='UTF-8')
    for line in stop_words_txt:
        stop_words.append(line.rstrip())
    
    for word in stop_words:
        if word in input_dictionary:
            del input_dictionary[word]
    
    
    # Import the current state of the reference_dictionary produced by webcrawler
    with open("reference_dictionary.pkl", "rb") as f:
        reference_dictionary = pickle.load(f)
    
    # Create a dictionary within which to embed input dictionary with reference
    def create_incubation_dictionary(reference_dictionary, input_dictionary):
        incubation_dictionary = dict()
        for word in reference_dictionary:
            incubation_dictionary[word] = reference_dictionary[word] + input_dictionary.get(word, 0)
        for word in input_dictionary:
            incubation_dictionary[word] = reference_dictionary.get(word, 0) + input_dictionary[word]
        return incubation_dictionary
    
    incubation_dictionary = create_incubation_dictionary(reference_dictionary, input_dictionary)
    
    # Run inflection collapse on the reference and the mixed, then subtract the reference from the mixed
    ruic_incubation = ruic(incubation_dictionary, "incubation_dictionary", breadth, style)
    ruic_reference = ruic(reference_dictionary, "reference_dictionary", breadth, style)
    
    for word in ruic_incubation:
        ruic_input_dictionary[word] = ruic_incubation[word] - ruic_reference.get(word, 0)
        if ruic_input_dictionary[word] == 0:
            del ruic_input_dictionary[word]
    ruic_input_dictionary = {k: v for k, v in sorted(ruic_input_dictionary.items(), key=lambda x: x[1], reverse=True)}

    
    return ruic_input_dictionary