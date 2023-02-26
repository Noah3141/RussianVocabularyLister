import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
import pickle

# Internet Prep
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# Controller inputs from user
print("\nEnter a starting URL, or press 'Enter' to use default")
url = input("URL:")
maximum_links = int(input("Choose a number of links to collect and scan:"))
if len(url) < 2:
    print("Default link used")
    url = "https://ru.wikipedia.org/wiki/%D0%A8%D1%80%D0%B5%D0%BA_(%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6)"


# Preparing a bunch of variables for later usage
links = []

stop_words = list()
stop_words_txt = open("stop_words.txt", 'r', encoding='UTF-8')
for line in stop_words_txt:
    stop_words.append(line.rstrip())


reference_dictionary = dict()


non_russian_stop_words = ["аз","нея","воно","він","це", "тя", "мене", "па", "з", "від"]



# Seed Initialization
rcv = urllib.request.urlopen(url, context =ctx).read()
print("\nSeed url loaded.\n")
soup = BeautifulSoup(rcv, 'html.parser')



seed_a_tags = str(soup.select('#mw-content-text'))
seed_extensions = re.findall('href="(/wiki/\S+?)"', seed_a_tags)
for ending in seed_extensions:
    links.append(('https://ru.wikipedia.org' + ending))

print("\nEntering crawl for links...\n")


# Link list creation  
while len(links) < maximum_links:
     for link in links:
        print(len(links),"/",maximum_links, "links found.")
        if len(links) > maximum_links: break
        try:
            rcv = urllib.request.urlopen(link, context =ctx).read()
        except: 
            print("\n\n!Something went wrong opening this link:\n", link, "\n\n")
            continue
        soup = BeautifulSoup(rcv, 'html.parser')
        
        
        link_a_tags = str(soup.select('#mw-content-text'))
        extensions = re.findall('href="(/wiki/\S+?)"', link_a_tags)
        for ending in extensions:
            if 'https://ru.wikipedia.org' + ending not in links:
                links.append(('https://ru.wikipedia.org' + ending))





#Dictionary creation from link list   
          
print("Link list has reached minimum depth. Switching to Dictionary Phase.")
print("Resulting length of link list: ", len(links))             
link_index = 0
for link in links:
    old_size = len(reference_dictionary)
    page = ""
    link_index = link_index + 1
    try:
        rcv = urllib.request.urlopen(link, context =ctx).read()
    except: 
        print("\n\n!Something went wrong opening this link:\n", link, "\n\n")
        continue
    soup = BeautifulSoup(rcv, 'html.parser')
    print("================================")
    print('Link', link_index, "soup created.")    
    
    body_paras = soup.find_all("p")
    for p in body_paras:
        page = page + p.text
    
    #Page processing
    #   Page = Page.replace('[править|править код]', ' ')
    #   if X in page: continue
 
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
    
    print("Estimated time remaining: ", round(((len(links) - link_index)*.4/60)   , 1), "m")
    pass 

print("\n\nLink list of ",len(links), " links exhausted.")
print('Final length of dictionary:', len(reference_dictionary))
print("Starting url was: \n", url ,"\n")
print("Depth was set to: ", maximum_links)

with open("reference_dictionary.pkl", "wb") as f:
    pickle.dump(reference_dictionary, f)
