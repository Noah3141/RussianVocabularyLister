from flask import Flask, request, redirect, render_template
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

@app.route("/", methods=["POST","GET"])
def RUBIT():
    if request.method == "POST":
        text_field = request.form["text_field"]
        Output_Breadth = request.form["Output_Breadth"]
        Output_Style = request.form["Output_Style"]
        print(text_field)
        return render_template("RUBIT.html")
    else:
        return render_template("RUBIT.html")





# class RUBIT(Resource):
#     def get(self): #Information sent in the GET request URL
#         return {self} # If GET request sent according to template, we got a name string, pass back this JSON dictionary, having inputted the variables from the GET URL 
#     def post(self, Create_List, Output_Breadth, Output_Style, text_field):
#         print(request.form)
#         return {}
# api.add_resource(RUBIT, "/") #Format and variables sendable to URL


if __name__ == "__main__":
    app.run(debug=True)