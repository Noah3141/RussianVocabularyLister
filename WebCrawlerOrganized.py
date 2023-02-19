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
url = input("\nStarting url: ")
maximum_links = int(input("Choose a number of links to collect and scan:"))
if len(url) < 2:
    url = "https://ru.wikipedia.org/wiki/%D0%A8%D1%80%D0%B5%D0%BA_(%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6)"


# Preparing a bunch of variables for later usage
links = []
stop_words = ["в","на","с","от","к","из","по", "и","для", "а",
              "что", "не","это", "при", "как", "чтобы", "об",
              "также", "то","когда", "но", "о", "где","он","или"]
Words = dict()



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
        rcv = urllib.request.urlopen(link, context =ctx).read()
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
    old_size = len(Words)
    page = ""
    link_index = link_index + 1
    rcv = urllib.request.urlopen(link, context =ctx).read()
    soup = BeautifulSoup(rcv, 'html.parser')
    print('Link', link_index, "soup created.")    
    
    body_paras = soup.find_all("p")
    for p in body_paras:
        page = page + p.text
    
    #Page processing
    #   Page = Page.replace('[править|править код]', ' ')
    #Word processing
    page_words = re.findall('\s([А-Я]*[а-я]+?)\s', page)
    page_words = [word.lower() for word in page_words if word not in stop_words]
    for item in page_words:
        Words[item] = Words.get(item,0)+1
    print('New length of dictionary:', len(Words))
    new_size = len(Words)
    print("Number of new words:", new_size-old_size)
    pass 

print("\n\nLink list of ",len(links), " links exhausted.")
print('Final length of dictionary:', len(Words))
print("Starting url was: \n", url ,"\n")
print("Depth was set to: ", maximum_links)

with open('Words.pkl', 'wb') as f:
    pickle.dump(Words, f)
 
