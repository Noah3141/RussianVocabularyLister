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
URL = input("Starting URL for URL scrounge: ")
Max = int(input("Choose a number of links to collect and scan:"))
if len(URL) < 2:
    URL = "https://ru.wikipedia.org/wiki/%D0%A8%D1%80%D0%B5%D0%BA_(%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6)"


# Preparing a bunch of variables for later usage
Links = []
stop_words = ["в","на","с","от","к","из","по", "и","для", "а",
              "что", "не","это", "при", "как", "чтобы", "об",
              "также", "то","когда"]
Words = dict()



# Seed Initialization
rcv = urllib.request.urlopen(URL, context =ctx).read()
print("Seed URL loaded.")
soup = BeautifulSoup(rcv, 'html.parser')
Seeds_A_tags = str(soup.find_all('a'))
SeedsExtensions = re.findall('href="(/wiki/\S+?)"', Seeds_A_tags)
for ending in SeedsExtensions:
    Links.append(('https://ru.wikipedia.org' + ending))

print("Entering crawl for links...")

# Link list creation  
while len(Links) < Max:
     for Link in Links:
        print(len(Links),"/",Max, "links found.")
        if len(Links) > Max: break
        rcv = urllib.request.urlopen(Link, context =ctx).read()
        soup = BeautifulSoup(rcv, 'html.parser')
        Link_A_tags = str(soup.select('#mw-content-text'))
        Extensions = re.findall('href="(/wiki/\S+?)"', Link_A_tags)
        for ending in Extensions:
            if 'https://ru.wikipedia.org' + ending not in Links:
                Links.append(('https://ru.wikipedia.org' + ending))


#Dictionary creation from link list             
print("Link list has reached minimum depth. Switching to Dictionary Phase.")                
Counter = 0
for Link in Links:
    Counter = Counter + 1
    rcv = urllib.request.urlopen(Link, context =ctx).read()
    soup = BeautifulSoup(rcv, 'html.parser')
    print('Link', Counter,"soup created.")    
    Page = soup.get_text(strip= True) # Extract the main readable text
    
    #Page processing
    Page = Page.replace('[править|править код]', ' ')
    #Word processing
    PageWords = re.findall('\s([А-Я]*[а-я]+?)\s', Page)
    
    PageWords = [word.lower() for word in PageWords if word not in stop_words]
    
    
    for item in PageWords:
        Words[item] = Words.get(item,0)+1 
    print('New length of dictionary:', len(Words))
print("Link list of ",len(Links)," links exhausted.")
print('Final length of dictionary:', len(Words))
print("Starting URL was: \n", URL,"\n")
print("Depth was set to: ", Max)

with open('Words.pkl', 'wb') as f:
    pickle.dump(Words, f)
 
