###############################################################################
#
# This script is run whenever input is put into the web app.
# Input is thoroughly checked for authenticity, and then compiled into a list,
# Just as occurs in the web app's output, except here, the list is then
# progressively fed to online dictionaries, and the true dictionary form is
# acquired, whereupon this is added to the web app's underlying dictionary_forms
# pickle. This means the site dynamically updates based on user input, such that
# if it falls short, it only provides the wrong answer for a limited amount of 
# time.
#
#
###############################################################################

import urllib, urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import pickle
import sys
import datetime
import time


# When run, the morfo pickle is opened, the words updated in the 
# dicitonary_forms pickle, and the morfo pickle is cleared of words.

def update_dictionary(setting: str):
   


    
    log_time = datetime.datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")

    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    link = "https://kak-pishetsya.com/"
    
    
    # Get morfo or make it
    try:
        with open("morfo_list.pkl", "rb") as f:
            morfo = pickle.load(f)
    except:
        morfo = list()
        with open("morfo_list.pkl", "wb") as f:
            pickle.dump(morfo, f)
        print("morfo_list.pkl initialized. Nothing to more do.")
        sys.exit()
     
        
    # Get dictionary forms
    with open("dictionary_forms.pkl", "rb") as f:
        dictionary_forms = pickle.load(f)
    
    updated_words = list()
    new_forms = list()
    
    # Clear out the double asterisk from morfo variable
    for word in morfo:
        if word.endswith("**"):
            morfo.remove(word)
            with open("user_flagged_update_log.txt", "a", encoding="UTF-8") as f:
                f.write(f"\n{log_time}\n{word} was entered in morfo. Skipping...")
    
    # Save that variable back to morfo
    with open("morfo_list.pkl", "wb") as f:
        pickle.dump(morfo, f)
    
############################################################################### 
    # Prepare settings for how to loop through morfo variable 
    delayer = False 
    
    if setting == "soft":
        if len(morfo) > 0:
            start = 0
            end = 3
        else:
            with open("user_flagged_update_log.txt", "a", encoding="UTF-8") as f:
                    f.write(f"\n\n'{setting}' call: {log_time}\nNothing needed updated.")
            return updated_words, new_forms
        
    elif setting == "hard":
        start = 0
        delayer = True
        end = len(morfo)
        if len(morfo) == 0:
            with open("user_flagged_update_log.txt", "a", encoding="UTF-8") as f:
                    f.write(f"\n\n'{setting}' call: {log_time}\nNothing needed updated.")
            return updated_words, new_forms
        
    elif setting == "last":
        start = -1
        end = None
 

###############################################################################

    # Going through the words in the morfo as it was at the start, minus the **
    for word in morfo[start:end]:
        
        
        if delayer: # This is to avoid pinging their poor site 500 times relentlessly, spreading out the load over time
            time.sleep(2)
        
        with open("updater_status.txt", "w", encoding="UTF-8") as f:
            f.write(f"Running '{setting}' call on word {word}")
        
        # We need a within loop instance of morfo so that the function doesn't constantly overlap itself and overwrite previous fixes
        with open("morfo_list.pkl", "rb") as f:
            morfo_iter = pickle.load(f) # Open the current state of morfo pickle as morfo_iter

        
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
            
        dictionary_forms[word] = dict_form # Fix dictionary_forms
        updated_words.append(word) # Make a note of the word we fixed
        new_forms.append(dict_form) # and what it was fixed as
        
        # Shorten the list morfo based on words we managed to address
        for word in updated_words: # Remove the word from morfo_iter (the within loop quick save)
            try:
                morfo_iter.remove(word)
            except: continue
        
        with open("morfo_list.pkl", "wb") as f:
            pickle.dump(morfo_iter, f)
        with open("dictionary_forms.pkl", "wb") as f:
            pickle.dump(dictionary_forms, f)
        
        with open("updater_status.txt", "w", encoding="UTF-8") as f:
            f.write("Open")
        
        
        pass
    print("New words added to key.")
    
        
    # Save all our work

        
    log_time_end = datetime.datetime.now().strftime("%H:%M:%S")
    len_updated = len(updated_words)
    len_new_forms = len(new_forms)
    with open("user_flagged_update_log.txt", "a", encoding="UTF-8") as f:
 
        f.write(f"\n\n'{setting}' call: {log_time}-{log_time_end}\nUpdated {len_updated} inputs: [")
        for item in updated_words:
            f.write(item + "   ")
        f.write(f"]\nWith {len_new_forms} dict forms: [")
        for item in new_forms:
            f.write(item + "   ")
        f.write("]")

    for word in new_forms:
        with open("backflow_to_database_text.txt", "a", encoding="UTF-8") as f:
            f.write(f"\n{word}")
    
    
    return updated_words, new_forms


