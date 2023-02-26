from flask import Flask, request, redirect, render_template, url_for
from flask_restful import Api
from input_vocabulary_compiler import rubit
from reference_lists_creator import create_verb_list
import pickle

app = Flask(__name__)
api = Api(app)

with open("reference_dictionary.pkl", "rb") as f:
    reference_dictionary = pickle.load(f)

@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("RUBIT")) #Named after the def RUBIT


@app.route("/rubit", methods=["POST","GET"])
def RUBIT():
    if request.method == "POST":
        text = request.form["text_field"]
        Output_Breadth = request.form["Output_Breadth"]
        Output_Style = request.form["Output_Style"]
        ruic_dictionary = rubit(text, Output_Breadth, Output_Style)
        return render_template("RUBIT_Output.html", dictionary=ruic_dictionary, breadth=Output_Breadth, style=Output_Style)
    else:
        return render_template("RUBIT.html")
    
    
@app.route("/pairs", methods=["GET"])
def PairsList():
    pair_list, tree_list = create_verb_list(reference_dictionary)
    return render_template("pairs.html", pair_list=pair_list)


@app.route("/trees", methods=["GET"])  
def TreesList():
    pair_list, tree_list = create_verb_list(reference_dictionary)
    return render_template("trees.html", tree_list=tree_list)

@app.route("/treeModel", methods=["GET"])  
def TreeModel():
    return render_template("treeModel.html")


@app.route("/ankiDeck", methods=["GET"])  
def AnkiDeck():
    return render_template("ankiDeck.html")




if __name__ == "__main__":
    app.run(debug=True)