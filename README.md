# RussianVocabularyLister


In order to create a web application that automatically generates a (lemmatized) vocabulary list from user-inputted Russian text, a very large amount of natural language processing is necessary, due to the ambiguities in inflectional forms. Prior to this project, no solution was publicly available. Previous linguistic analyses offered lemmatization libraries in Python, but their level of accuracy was designed for search engines, not second language study. 

To complete this task, the Flask app is complete with a large scale language corpus stored in a mySQL database, which is fed cumulatively through 
1) a Russian wikipedia web scraper, capable of quickly compiling multiple hundreds of thousands of unique words
2) a script intended to scrape entire Russian books from public websites. 

Together, these fill a database which is used to triangulate lemma forms of a given Russian word. The site also allows users to browse the database’s verbs in two different grammatical models, and see their inputted text processed into one of these grammatical models, each of which requires another layer of language processing and derivational analysis.

