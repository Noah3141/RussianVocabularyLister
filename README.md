# http://www.RussianVocabularyListMaker.com/rubit


In order to create a web application that automatically generates a (lemmatized) vocabulary list from user-inputted Russian text, a very large amount of natural language processing is necessary, due to the ambiguities in inflectional forms. Prior to this project, no solution was publicly available. Previous linguistic analyses offered lemmatization libraries in Python, but their level of accuracy was designed for search engines, not second language study. 

To complete this task, the Flask app is complete with a large scale language corpus stored in a mySQL database, which is fed cumulatively through 
1) A Russian wikipedia web scraper, capable of quickly compiling multiple hundreds of thousands of unique words
2) A script intended to scrape entire Russian books from public websites.
3) User input on the site
4) User flagged words on the site

Together, these fill a database which is used to triangulate lemma forms of a given Russian word. This is done by taking each individual word, and probing the presence of sufficient numbers of proposed alternative forms for a given lexical category, until a score passes the relevant threshold, whereupon the word is processed for subtypes within that lexical category (e.g. -ивать ending verb of subtype that contains an 'o' to 'a' stem change), and its true dictionary form is reverse-engineered.

The site also allows users to browse the database’s verbs in two different grammatical models, and see their inputted text processed into one of these grammatical models, each of which requires another layer of language processing and derivational analysis.

Since the database is inevitably not large enough to find every word in a sufficient variety of forms to triangulate its dictionary form, the app notices when words are inputted by the user, which aren't in the key. It then searches these words on *kak-pishetsya.com*, and scrubs the page for the dictionary form. The web app learns over time based on user inputted text, and can have entries explicity flagged for this kind of update when the Python lemmatization script offers a faulty output.

Upon list creation, one thread is sent to collect any words that the key did not recognize, which can take many minutes. Simultaneously, a user may use the flag word button, which sends an AJAX request to the server to initiate another worker onto that same update script. Because of this, a locking mechanism and multiple checks are in place to allow the flag button to work even during longer-term background update scrubbing, without causing an "unpickling" data corruption error from simultaneous reading and editing. For instance, the updater is designed with a for loop that announces the beginning of an update, sets up all the tools, runs the http request, scrubs the page, updates the resources, and then puts down all the tools and announces into a log file that the updater is open. When another call is made to the function, it checks the status of the updater and waits until any other calls are *in between for loop iterations*. Because the longer calls are time-delayed (partly just to blunt the load on *kak-pishetsya.com*) by a short period between loops, this allows a falg word call to slip its work between the iterations of the longer background updating process.

Finally, the site includes an anki deck, and the contents of that deck explained and displayed in-page, which proposes an alternative model of Russian verbs as trees, more than pairs. It contains a hand-made list of over 200 verb trees, which, together with the database's tree output, amounts to a fully comprehensive list of Russian verbs for the purposes of second language acquisition.

Excluding the verb pairs and verb trees, the app's data flow is as follows:

![Data_Flow (1)](https://user-images.githubusercontent.com/66894106/227043315-80e0e30d-bc85-4ac8-9a01-998083d5c3d3.png)

Okay, but what does it do that wasn't already available?

1) Offers vocabulary list generation based on user input for Russian text
2) Also allows these lists to be generated in verb pairs (the standard model of and mimimum necessary way of learning Russian verbs)
3) Even allows these lists to be generated in a novel verbal model, which approximates the languages base lexemes - verb tree. That's a novel, revolutionary grammatical model, and a novel list generator that uses that model!
4) Complete, single page, total lexicon verb lists in both pair and tree. While it is possible to find "Top 500 Russian Verbs", nowhere else is it possible to find a comprehensive, total-lexicon list of nearly all the Russian verbs on a _single page_ (even Wiktionary splits up the pages), not to mention the entire language's list of verb trees. Verb trees approximate lexemes close enough that learning the entire Russian verb tree page is akin to learning most of the words in the language (not just the verbs!). This means that the Russian verb tree page is the first available resource which completely obliterates the entire intermediate stage of Russian language learning, extending well into advanced levels.

For Russian learners and Russian teachers - this web app changes the game.

For deployment instruction on an AWS EC2 Ubuntu server, using Nginx and Gunicorn:
![Flask_Gunicorn_Nginx_Deployment_Roadmap](https://user-images.githubusercontent.com/66894106/228661711-772f8989-32f8-485c-b015-fd66cf3d7ebe.png)
