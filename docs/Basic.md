# Instructions for Setup


1. *reference_dictionary_web_crawler.py
   * > This feeds a database with the body paragraphs of linked Wikipedia pages along a crawl.

2. *large_book_scraper.py*
   * > This is set up to take two popular Russian book websites, and scrape page by page through entire books.
   * > It is necessary for the triangulation of lemma forms to get words used in other forms that are unlikely to occur in textbook-ish Wikipedia articles.

3. Run both *get_reference_dictionary_key.py* and *get_full_vocab.py*
   * > These process the database into save-state pickle files. These pickle files contain the product of slow language processing, but once made, can be utilized very quickly by the website's pages.

4. Launch the webapp in flask by:
   * > *python website__init.py*

5. Go to 127.0.0.1:5000 in browser
