###############################################################################
#
# This script updates a faulty output of the pair_list
#
###############################################################################


import urllib, urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import pickle
import sys
import os
import time


# When run, the morfo pickle is opened, the words updated in the 
# dicitonary_forms pickle, and the morfo pickle is cleared of words.

def update_verb_list():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    link = "https://kak-pishetsya.com/"
    
    try:
        with open("morfo_list.pkl", "rb") as f:
            morfo = pickle.load(f)
    except:
        morfo = list()
        with open("morfo_list.pkl", "wb") as f:
            pickle.dump(morfo, f)
        print("morfo_list.pkl initialized. Nothing to more do.")
        sys.exit()
        
    with open("dictionary_forms.pkl", "rb") as f:
        dictionary_forms = pickle.load(f)
    
    updated_words = list()
    
    for word in morfo:
        
        encoded_word = urllib.parse.quote(word, safe='')
        morfo_link = link + encoded_word
        
        
        rcv = urllib.request.urlopen(morfo_link, context =ctx).read()
        
        
        soup = BeautifulSoup(rcv, 'html.parser')
        page = soup.text
        page_lines = page.split()
        
        
        dict_form = page_lines[15]
        print(f"Dictionary form of {word} found as {dict_form}!")
        if dict_form == "Если": # This is the word that is caught when a broken link is passed
            dict_form = word + "**"
            
        dictionary_forms[word] = dict_form
        updated_words.append(word)
        with open("dictionary_forms.pkl", "wb") as f:
            pickle.dump(dictionary_forms, f)
        pass
    print("New words added to key.")
    
    
    # Shorten the list morfo based on words we managed to address
    for word in updated_words:
        try:
            morfo.remove(word)
        except: continue
    
    
    # Save all our work
    with open("morfo_list.pkl", "wb") as f:
        pickle.dump(morfo, f)
        
        