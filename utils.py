import string, configparser, json, requests
from sqlalchemy import create_engine 
import mysql.connector as con 


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

def get_api_details(): 
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

def get_facebook_details():
    """
    This Function reads the correct details to log into facebook 
    which will allow python to send messages on your behalf. 

    PARAMETERS: 

    None 

    RETURNS: 

    username(string): the username for the facebook account 
    password(string): the password for the facebook account
    """
    config = configparser.ConfigParser()

    config.read('config.ini') 

    username = config['facebook']['username']

    password = config['facebook']['password']

    return username, password


def get_sql_details(): 
    """
    """

    config = configparser.ConfigParser()

    config.read('config.ini')

    username = config['mysql']['username']

    password = config['mysql']['password']

    port = config['mysql']['port']

    database = config['mysql']['database']
    host = config['mysql']['host']

    conn_string  = f'mysql+mysqlconnector://{username}:\
{password}@{host}:{port}/{database}'

    print(conn_string)
    return create_engine(conn_string)

def input_sql(query): 
    """
    """
    connection = con.connect(host = 'localhost', database = 'FPG',
                             user = 'root', password = '2002Fish')
    cursor = connection.cursor()  

    cursor.execute(query) 

    connection.commit() 

    cursor.close()

    return '--query inputted--'


def get_current_round(): 
    """
    """
    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/rounds/2790/current"

    data = pull(url)

    round = data['api']['fixtures'][0][-1]

    return round 


def pull(url):

    """
    This function will pull the data down from
    the football API it automatically pulls the 
    correct headers for the connection to work
    
    PARAMETERS: 

    url(string): This is the URL for the endpoint 
    of the API you want the data from 

    RETURNS: 

    (dictionary) This is the data from the API you requested 

    """
    headers = get_api_details() 

    response = requests.request("GET", url, headers=headers)

    data = json.loads(response.text) 

    return data 