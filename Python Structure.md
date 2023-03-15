# Python Relationship Structure:
    
## Functions:
    > def update_dictionary(setting:str)
        Defined in: 
            auto_update_dictionary_by_user_input.py
        Inputs: 
            setting: determines how much of morfo_list to process during this call
        Outputs:
            updated_words: a list of words that have been checked
            new_forms: a list of the new forms that were retrieved (these lists should be same length always)
        Called in:
            website_init.py with "soft" when user inputs Create List
            website_init.py with "last" when flags a word
            
    > def rubit(input_text: str, breadth: str, style: str) -> dict:
    
## Scripts
    > py get_reference_russian_key.py
        Running resets for word in database the dictionary_forms (dict) to my script
        
## Variables & Pickles
    > dictionary_forms (dict)
        Utility:
            Stores a connection between a word (key) and its dictionary form (value)
        Utilized in:
            get_reference_russian_key.py creates it, with the database and flaws of the script
            update_dictionary() tries to fix the values for keys, based on online lookup
    
    > morfo_list (list)
        Utility:
            Keeps a list of words that will be checked online for a more accurate dictionary form
        Utilized in:
            rubit() adds words
            update_dictionary() processes and clears words
