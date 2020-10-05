import string, configparser 

def clean_string(text):
    """
    This function will take a string and return the same string 
    but with any white space and punctuation stripped and with 
    the first letter of each word capitalized. 

    PARAMETERS: 

    text (string): this is the text you want to clean 

    RETURNS 

    (string): this is the clean version of the given string
    """
    text = " ".join(text.split())

    text = text.translate(str.maketrans('', '', string.punctuation))

    return text.lower().title().strip() 

def get_details(): 
    """
    This function reads the correct headers from the config.ini 
    file and returns them so we can use them to access the api 

    PARAMETERS: 

    None

    RETURNS: 

    (dictionary) This is a dictionary with the correct details 
    to connect to the api 

    """
    config = configparser.ConfigParser()

    config.read('config.ini') 

    headers = {}

    headers['x-rapidapi-host'] = config['football_API']['host']

    headers['x-rapidapi-key'] = config['football_API']['key']
    
    return headers 