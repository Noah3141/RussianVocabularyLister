from flask import Flask, request, redirect, render_template, url_for
from flask_restful import Api
from input_vocabulary_compiler import rubit
from reference_lists_creator import create_verb_list
import pickle

app = Flask(__name__)
api = Api(app)

with open("dictionary_forms.pkl", "rb") as f:
    dictionary_forms = pickle.load(f)

@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("RUBIT")) #Named after the def RUBIT


@app.route("/rubit", methods=["POST","GET"])
def RUBIT():
    if request.method == "POST":
        input_text = request.form["text_field"]
        output_breadth = request.form["Output_Breadth"]
        output_style = request.form["Output_Style"]
        output_dictionary = rubit(input_text, output_breadth, output_style)
        return render_template("RUBIT_Output.html", dictionary=output_dictionary, breadth=output_breadth, style=output_style)
    else:
        return render_template("RUBIT.html")
    
    
@app.route("/pairs", methods=["GET"])
def PairsList():
    with open("pair_list.pkl", "rb") as f:
        pair_list = pickle.load(f)
    return render_template("pairs.html", pair_list=pair_list)


@app.route("/trees", methods=["GET"])  
def TreesList():
    with open("tree_list.pkl", "rb") as f:
        tree_list = pickle.load(f)
    return render_template("trees.html", tree_list=tree_list)

@app.route("/treeModel", methods=["GET"])  
def TreeModel():
    return render_template("treeModel.html")


@app.route("/ankiDeck", methods=["GET"])  
def AnkiDeck():
    return render_template("ankiDeck.html")




if __name__ == "__main__":
    app.run(debug=True) # Add port 