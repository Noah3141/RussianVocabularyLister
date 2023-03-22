###############################################################################

# This script runs the website, and provides the VIEWS and CONTROLLERS.

# Object relational mapping is completed by administrative scripts, which
# process database data into saved .pkl files, which are then used 
# in the functions/scripts referenced in this file.

###############################################################################
###############################################################################


from flask import Flask, request, redirect, render_template, url_for
from flask_restful import Api
from input_vocabulary_compiler import rubit
import pickle
import threading
from auto_update_dictionary_by_user_input import update_dictionary
from datetime import datetime
import time
import os
import re


app = Flask(__name__)
api = Api(app)


###############################################################################

@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("RUBIT")) #Named after the def RUBIT


@app.route("/rubit", methods=["POST","GET"])
def RUBIT():
        return render_template("RUBIT.html")
    
@app.route("/rubit/output", methods=["POST"])
def RUBIT_OUTPUT():
    if request.method == "POST":
        
        input_text = request.form["text_field"]        
        output_breadth = request.form["Output_Breadth"]
        output_style = request.form["Output_Style"]
        
        output_dictionary, _ = rubit(input_text, output_breadth, output_style)
        
        updates, _ = update_dictionary("soft")
        if len(updates) >= 3:
            thread = threading.Thread(target=update_dictionary,args=["hard"])
            thread.start()

        missing_count = 0
        for word in output_dictionary:
            if output_dictionary[word] == "*":
                missing_count += 1
        missing_count = round(missing_count / 14)
                                            # In the format:   HTML_Jinja_Variable = Python_Variable
        return render_template("RUBIT_Output.html", dictionary = output_dictionary, breadth = output_breadth, style = output_style, input_text=input_text, missing = missing_count)


@app.route("/pairs", methods=["GET"])
def PairsList():
    if request.method == "GET":
        with open("pair_list.pkl", "rb") as f:
            pair_list = pickle.load(f)
        return render_template("pairs.html", pair_list = pair_list)


@app.route("/trees", methods=["GET"])  
def TreesList():
    if request.method == "GET":
        with open("tree_list.pkl", "rb") as f:
            tree_list = pickle.load(f)
        return render_template("trees.html", tree_list = tree_list)
    
    
@app.route("/flag-word", methods=["POST"])
def FlagWord():
    data = request.json
    value = data['value']
    
    while True: # This allows us to double-dutch into the update at exactly the right moment not to trip over unpickling error from overlapping open-&-save
        with open("updater_status.txt", "r", encoding="UTF-8") as f:
            status = f.read()
        if status == "Open": break
        else: time.sleep(0.5)

    # The data sent from each of the three pages looks like the following:



    
    # "Raw Vocabulary: языка - 1" , "Raw Vocabulary: рядо - 1" 
    # "Raw Vocabulary: ый - 2"
    # Update dictionary_forms through 'auto_update_dictionary_by_user_input.py'
    if value.startswith("Raw Vocabulary:"):
        
        input_text = data['input_text'] 
        input_text = re.sub("\n", " ", input_text) # Remove newlines for when we file away the input txt in the log
        
        with open("dictionary_forms.pkl", "rb") as f:
            dictionary_forms = pickle.load(f)
        
        with open("morfo_list.pkl", "rb") as f:
            morfo = pickle.load(f)
        
        flag_word_start = value.find(": ") + 2
        flag_word_end = value.find(" -")
        problem_word_out = value[flag_word_start:flag_word_end] # Extract the problem word from the list-entry (e.g. "казить - 12")
        
        if problem_word_out.endswith("**"): #
            log_time = datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")
            with open("user_flagged_update_log.txt", "a", encoding="UTF-8") as f:
                f.write(f"\n\n{log_time}:{problem_word_out} was flagged. Ignored.")
                return '', 405 # Return an empty response with a "Method not allowed" code
        
        
        
        _, input_count = rubit(input_text, "Full List", "Raw Vocabulary")
        
        for word in input_count:
            try:
                test_output = dictionary_forms[word]
            except:
                continue # Runs risk of never assigning problem_word_in
            if test_output == problem_word_out:
                problem_word_in = word
                if problem_word_in not in morfo:
                    morfo.append(problem_word_in) 
                break
            pass
        
        with open("morfo_list.pkl", "wb") as f:
            pickle.dump(morfo, f)
    
        thread_2 = threading.Thread(target=update_dictionary,args=["last"])
        thread_2.start()
        
        log = f"\n\nInput text:    {input_text}\nFlagged entry: <{problem_word_out}> generated from '{problem_word_in}'"
        # Save log of all this in user_flagged_update_log.txt
        with open("user_flagged_update_log.txt", "a", encoding="UTF-8") as f:
            f.write(log)
        
        pass
    
    
    
    
    
    # "Verb Pairs: поддерзить - поддерживать" 
    # Update verb list (will be undone when get_full_verbs.py is run)
    if value.startswith("Verb Pairs:"):
        with open("pair_list.pkl", "rb") as f:
            pair_list = pickle.load(f)  
        
        word_start = value.find("- ") + 2
        caught_imperfective = value[word_start:]
        
        
        
        
        with open("morfo_list.pkl", "wb") as f:
            pickle.dump(morfo, f)
        pass
    
    # "Verb Trees: канкать (-канчивать): за-"
    # Update verb list (will be undone when get_full_verbs.py is run)
    if value.startswith("Verb Trees:"):        
        with open("tree_list.pkl", "rb") as f:
            tree_list = pickle.load(f)
            
            
            

        pass
    
    
    
    
    
 
    
    
    return '', 201 # Return an empty response with a "Created" status code

    


@app.route("/ankiDeck", methods=["GET"])  
def AnkiDeck():
    return render_template("ankiDeck.html")

###############################################################################





if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port='5500') # Add port 
    


