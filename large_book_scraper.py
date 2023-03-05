import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
import pickle
import mysql.connector


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


links = []

stop_words = list()
stop_words_txt = open("stop_words.txt", 'r', encoding='UTF-8')
for line in stop_words_txt:
    stop_words.append(line.rstrip())


reference_dictionary = dict()


non_russian_stop_words = [" нея "," воно "," він "," це ", " тя ", " мене ", " па ", " з ", " від "]



# Build links

link = "https://ilibrary.ru/text/"

# "https://ilibrary.ru/text/    11/      p.1/      index.html"
#                           война и мир   page 1    look for: "span.p"
#
# https://ilibrary.ru/text/      1199/   p.97/      index.html

book_page_links = []
# War and Peace
for i in range(1 , 361):
    book_page_links.append(link + "11/p." + str(i) + "/index.html") 
# Brothers Karamazov
for i in range(1 , 97):
    book_page_links.append(link + "1199/p." + str(i) + "/index.html")
# The Idiot
for i in range(1 , 50):
    book_page_links.append(link + "94/p." + str(i) + "/index.html")
# Anna Karenina
for i in range(1 , 239):
    book_page_links.append(link + "1099/p." + str(i) + "/index.html")



# Collect words from famous books:
for link in book_page_links:
    old_size = len(reference_dictionary)
    page = ""
    try:
        rcv = urllib.request.urlopen(link, context =ctx).read()
    except: 
        print("\n\n!Something went wrong opening this link:\n", link, "\n\n")
        continue
    
    soup = BeautifulSoup(rcv, 'html.parser')
    print("================================")
    print(link)
    
    body_paras = soup.find_all(["span"], class_="p")
    for p in body_paras:
        page = page + p.text
    
    print(page)
    #Word processing
    page_words = re.findall('([А-Я]*[а-я]+)', page)
    
    #   If a non-Russian slavic language is found, we need to reject the whole page and move on:
    if any(word in non_russian_stop_words for word in page_words):
        print("\x1b[31mThis page may have not been Russian: \x1b[0m", link)
        continue
    
    page_words = [word.lower() for word in page_words if word not in stop_words]
    for word in page_words:
        reference_dictionary[word] = reference_dictionary.get(word, 0) + 1
    
    print('New length of dictionary:', len(reference_dictionary))
    new_size = len(reference_dictionary)
    print("Number of new words:", new_size-old_size)
    if new_size-old_size > 100:
        print("Found at:", link)
    