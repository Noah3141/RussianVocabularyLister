###############################################################################

# This script is run as an admin on a PC for creating updated .pkl files.
# Those .pkl files can then be pushed to the GIT repository, for use in the site.

# This file feeds the database, others pull that database into a .pkl file.

###############################################################################
###############################################################################






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

stop_words = set()
stop_words_txt = open("stop_words.txt", 'r', encoding='UTF-8')
for line in stop_words_txt:
    stop_words.add(line.rstrip())


reference_dictionary = dict()


non_russian_stop_words = [" нея "," воно "," він "," це ", " тя ", " мене ", " па ", " з ", " від "]



# Build links
book_page_links = []








# link = "https://ilibrary.ru/text/"

# (["span"], class_="p")

# "https://ilibrary.ru/text/    11/      p.1/      index.html"
#                           война и мир   page 1    look for: "span.p"
#
# https://ilibrary.ru/text/      1199/   p.97/      index.html


# War and Peace
# for i in range(1 , 361):
#     book_page_links.append(link + "11/p." + str(i) + "/index.html") 
# # Brothers Karamazov
# for i in range(1 , 97):
#     book_page_links.append(link + "1199/p." + str(i) + "/index.html")
# # The Idiot
# for i in range(1 , 50):
#     book_page_links.append(link + "94/p." + str(i) + "/index.html")
# # Anna Karenina
# for i in range(1 , 239):
#     book_page_links.append(link + "1099/p." + str(i) + "/index.html")



link = "http://loveread.ec/read_book.php?id=104731&p="
#(["p"], class_="MsoNormal")  << Insert this  at the "body_paras = soup.find_all" below

for i in range (1, 107):              # Check the final page number, and insert here
    book_page_links.append(link + str(i))




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

    body_paras = soup.find_all(["p"], class_="MsoNormal")
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
               
        
        
# Run the script and review the sucess of the scraping. 
# Once done, reference_dictionary is in the variables.
# Now uncomment, copy, comment, and paste the code from below
# Into the console. I generally had 4 or 5 consoles running from that
# point, at the same time.

     
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "nnssoteck3434###",
    database = "Database_001")

cursor = conn.cursor()

for word in reference_dictionary:
    
    #print("Next word: ", word)
    cursor.execute(f"SELECT 1 FROM words WHERE word = '{word}'")
    find = cursor.fetchall()
    if len(find) == 0:
        print(word, " not found in database. Adding...")
        cursor.execute(f"INSERT INTO words (word, frequency) VALUES ('{word}', {reference_dictionary[word]});")
        conn.commit()
    else: 
        continue
    