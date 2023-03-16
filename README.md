# RussianVocabularyLister


In order to create a web application that automatically generates a (lemmatized) vocabulary list from user-inputted Russian text, a very large amount of natural language processing is necessary, due to the ambiguities in inflectional forms. Prior to this project, no solution was publicly available. Previous linguistic analyses offered lemmatization libraries in Python, but their level of accuracy was designed for search engines, not second language study. 

To complete this task, the Flask app is complete with a large scale language corpus stored in a mySQL database, which is fed cumulatively through 
1) A Russian wikipedia web scraper, capable of quickly compiling multiple hundreds of thousands of unique words
2) A script intended to scrape entire Russian books from public websites. 

Together, these fill a database which is used to triangulate lemma forms of a given Russian word. The site also allows users to browse the database’s verbs in two different grammatical models, and see their inputted text processed into one of these grammatical models, each of which requires another layer of language processing and derivational analysis.

Since the database is inevitably not large enough, the app notices when words are inputted by the user, which aren't in the key. It then searches these words on *kak-pishetsya.com*, and scrubs the page for the dictionary form. The web app learns over time based on user inputted text, and can have entries explicity flagged for this kind of update when the Python lemmatization script offers a faulty output.

Finally, the site includes an anki deck, and the contents of that deck explained and displayed in-page, which proposes an alternative model of Russian verbs as trees, more than pairs. It contains a hand-made list of over 200 verb trees, which, together with the database's tree output, amounts to a fully comprehensive list of Russian verbs.

