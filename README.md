# russianvocabularylistmaker.com/rubit


In order to create a web application that automatically generates a (lemmatized) vocabulary list from user-inputted Russian text, a very large amount of natural language processing is necessary, due to the ambiguities in inflectional forms. Prior to this project, no solution was publicly available. Previous linguistic analyses offered lemmatization libraries in Python, but their level of accuracy was designed for search engines, not second language study. 

To complete this task, the Flask app is complete with a large scale language corpus stored in a mySQL database, which is fed cumulatively through 
1) A Russian wikipedia web scraper, capable of quickly compiling multiple hundreds of thousands of unique words
2) A script intended to scrape entire Russian books from public websites.
3) User input on the site
4) User flagged words on the site

Together, these fill a database which is used to triangulate lemma forms of a given Russian word. The site also allows users to browse the database’s verbs in two different grammatical models, and see their inputted text processed into one of these grammatical models, each of which requires another layer of language processing and derivational analysis.

Since the database is inevitably not large enough, the app notices when words are inputted by the user, which aren't in the key. It then searches these words on *kak-pishetsya.com*, and scrubs the page for the dictionary form. The web app learns over time based on user inputted text, and can have entries explicity flagged for this kind of update when the Python lemmatization script offers a faulty output.

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
