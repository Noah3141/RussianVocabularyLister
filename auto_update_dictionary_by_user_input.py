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
# Simultaneous calling of this function (e.g. a second person hitting "Create List"
# Before the script is done) will result in the updates of the first call being
# undone by the save of the the second function call (only the second person's
# input will be updated). Repeatedly inputting large amounts of text will cause 
# this, as just 10 links to update can take unfortunately long. 
#
###############################################################################

import urllib, urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import pickle
import sys
import os
import time
import datetime


# When run, the morfo pickle is opened, the words updated in the 
# dicitonary_forms pickle, and the morfo pickle is cleared of words.

def update_dictionary(setting: str):
    
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
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
    new_forms = list()
    
    for word in morfo:
        if word.endswith("**"):
            morfo.remove(word)
            with open("user_flagged_update_log.txt", "a", encoding="UTF-8") as f:
                f.write(f"\n{log_time}\n{word} was entered in morfo. Skipping...")
    
    if setting == "soft":
        if len(morfo) > 0:
            start = 0
            end = 5
        else:     
            return updated_words, new_forms
        
    elif setting == "hard":
        start = 0
        end = len(morfo)
    elif setting == "last":
        start == -1
        end == None
            
    for word in morfo[start:end]:
        
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
        new_forms.append(dict_form)
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
        
    log_time_end = datetime.now().strftime("%H:%M:%S")
    with open("user_flagged_update_log.txt", "a", encoding="UTF-8") as f:
        f.write(f"\n{log_time}-{log_time_end}\nUpdated Inputs: [")
        for item in updated_words:
            f.write(item + "   ")
        f.write("]\nWith dict forms: [")
        for item in new_forms:
            f.write(item + "   ")
        f.write("]\n")

    
    
    
    return updated_words, new_forms


# update_dictionary()
    
# # Get the initial modification time of the pickle file
# last_modified = os.path.getmtime('morfo_list.pkl')

# while True:
#     # Check if the pickle file has been modified
#     current_modified = os.path.getmtime('morfo_list.pkl')
#     if current_modified > last_modified:
#         # Call the function if the file has been modified
#         update_dictionary()
#         last_modified = current_modified

#     # Wait for some time before checking again
#     time.sleep(10)
