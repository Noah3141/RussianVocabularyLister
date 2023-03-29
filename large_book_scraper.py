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
import time


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

all_books = {"http://loveread.ec/read_book.php?id=1352&p=" : 101,
              "http://loveread.ec/read_book.php?id=1552&p=" : 110,
              "http://loveread.ec/read_book.php?id=96079&p=" : 60,
              "http://loveread.ec/read_book.php?id=95874&p=" : 82,
              "http://loveread.ec/read_book.php?id=95141&p=" : 92,
              "http://loveread.ec/read_book.php?id=98084&p=" : 52,
              "http://loveread.ec/read_book.php?id=97951&p=" : 57,
              "http://loveread.ec/read_book.php?id=97315&p=" : 97,
              "http://loveread.ec/read_book.php?id=96170&p=" : 58,
              "http://loveread.ec/read_book.php?id=100512&p=" : 71,
              "http://loveread.ec/read_book.php?id=100192&p=" : 64,
              "http://loveread.ec/read_book.php?id=93175&p=" : 61,
              "http://loveread.ec/read_book.php?id=92959&p=" : 90,
              "http://loveread.ec/read_book.php?id=96076&p=" : 79,
              "http://loveread.ec/read_book.php?id=95998&p=" : 65,
              "http://loveread.ec/read_book.php?id=191&p=" : 84,
              "http://loveread.ec/read_book.php?id=545&p=" : 48,
              "http://loveread.ec/read_book.php?id=546&p=" : 46,
              "http://loveread.ec/read_book.php?id=187&p=" : 105,
              "http://loveread.ec/read_book.php?id=2106&p=" : 195,
              "http://loveread.ec/read_book.php?id=2293&p=" : 50,
              "http://loveread.ec/read_book.php?id=2396&p=" : 38,
              "http://loveread.ec/read_book.php?id=86776&p=" : 37,
              "http://loveread.ec/read_book.php?id=86822&p=" : 45,
              "http://loveread.ec/read_book.php?id=87064&p=" : 73,
              "http://loveread.ec/read_book.php?id=87287&p=" : 55,
              "http://loveread.ec/read_book.php?id=106287&p=" : 54,
              "http://loveread.ec/read_book.php?id=93383&p=" : 110,
              "http://loveread.ec/read_book.php?id=95041&p=" : 74,
              "http://loveread.ec/read_book.php?id=95042&p=" : 187,
              "http://loveread.ec/read_book.php?id=99493&p=" : 57,
              "http://loveread.ec/read_book.php?id=104581&p=" : 55,
              "http://loveread.ec/read_book.php?id=106286&p=" : 74,
              "http://loveread.ec/read_book.php?id=87284&p=" : 94,
              "http://loveread.ec/read_book.php?id=87344&p=" : 98,
              "http://loveread.ec/read_book.php?id=88723&p=" : 68,
              "http://loveread.ec/read_book.php?id=88724&p=" : 61,
              "http://loveread.ec/read_book.php?id=88955&p=" : 78,
              "http://loveread.ec/read_book.php?id=92253&p=" : 63,
              "http://loveread.ec/read_book.php?id=84641&p=" : 185,
              "http://loveread.ec/read_book.php?id=85211&p=" : 285,
              "http://loveread.ec/read_book.php?id=85538&p=" : 62,
              "http://loveread.ec/read_book.php?id=86080&p=" : 129,
              "http://loveread.ec/read_book.php?id=87017&p=" : 94,
              "http://loveread.ec/read_book.php?id=87119&p=" : 78,
              "http://loveread.ec/read_book.php?id=81942&p=" : 56,
              "http://loveread.ec/read_book.php?id=83427&p=" : 155,
              "http://loveread.ec/read_book.php?id=83526&p=" : 80,
              "http://loveread.ec/read_book.php?id=83672&p=" : 78,
              "http://loveread.ec/read_book.php?id=84588&p=" : 202,
              "http://loveread.ec/read_book.php?id=80349&p=" : 216,
              "http://loveread.ec/read_book.php?id=80703&p=" : 99,
              "http://loveread.ec/read_book.php?id=108795&p=" : 114,
              "http://loveread.ec/read_book.php?id=108069&p=" : 77,
              "http://loveread.ec/read_book.php?id=108042&p=" : 69,
              "http://loveread.ec/read_book.php?id=108074&p=" : 76,
              "http://loveread.ec/read_book.php?id=102060&p=" : 95,
              "http://loveread.ec/read_book.php?id=102330&p=" : 91,
              "http://loveread.ec/read_book.php?id=108683&p=" : 82,
              "http://loveread.ec/read_book.php?id=108422&p=" : 90}

#(["p"], class_="MsoNormal")  << Insert this  at the "body_paras = soup.find_all" below
book_counter = 0
for link in all_books: 
    book_counter += 1
    for i in range (1, all_books[link]):              # Check the final page number, and insert here
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


cursor.execute("SELECT word FROM words")
words = cursor.fetchall()


stop_words = set()
stop_words_txt = open("stop_words.txt", 'r', encoding='UTF-8')
for line in stop_words_txt:
    stop_words.add(line.rstrip())

word_list = list()  
for row in words:
    word = row[0]
    if word not in stop_words:
        word_list.append(word)

word_list_set = set(word_list)



for word in reference_dictionary:
    
    #print("Next word: ", word)
    if word not in word_list_set:
        print(word, " not found in database. Adding...")
        cursor.execute(f"INSERT INTO words (word, frequency) VALUES ('{word}', {reference_dictionary[word]});")
        conn.commit()
    else: 
        continue
    
    
cursor.close()
conn.close() 