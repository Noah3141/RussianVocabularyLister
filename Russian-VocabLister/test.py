import requests

BASE = "http://127.0.0.1:5000/"

Create_List = True
text_field = "Whatever you want man I don't know"
Output_Breadth = "Full List"
Output_Style = "Tree'd"

response = requests.post("http://127.0.0.1:5000/?text_field=%D0%BF%D0%BE%D1%87%D0%B5%D0%BC%D1%83-%D1%82%D0%BE+%D1%8F+%D0%BD%D0%B5+%D0%B4%D0%BE%D0%B2%D0%BE%D0%BB%D0%B5%D0%BD&Create_List=&Output-Breadth=Broad+List&Output-Style=Verbs+Paired")
print(response.json())

# http://127.0.0.1:5000/?text_field=%D0%BF%D0%BE%D1%87%D0%B5%D0%BC%D1%83-%D1%82%D0%BE+%D1%8F+%D0%BD%D0%B5+%D0%B4%D0%BE%D0%B2%D0%BE%D0%BB%D0%B5%D0%BD&Create_List=&Output-Breadth=Broad+List&Output-Style=Verbs+Paired