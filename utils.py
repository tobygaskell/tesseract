import string, configparser, json, requests
from sqlalchemy import create_engine 
import mysql.connector as con 
import pandas as pd 


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

    # TODO: change the doc stings so they match the new functionality 

    """
    This function will read the SQL connection details for 
    the SQL server being used to store the game data on and 
    allow you to read from the SQL database 

    PARAMETERS: 

    NONE

    RETURNS: 

    (ConnectionEngine) This is the connection engine for the 
    SQL database names conn 
    """
    config = configparser.ConfigParser()

    config.read('config.ini')

    username = config['mysql']['username']

    password = config['mysql']['password']

    port = config['mysql']['port']

    database = config['mysql']['database']

    host = config['mysql']['host']

    return username, password, host, port, database 


def read_from_sql(query, index = False) : 
    """
    """
    username, password, host, port, database = get_sql_details() 

    conn_string  = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(username, password, host, port, database)

    conn = create_engine(conn_string)
    if index: 
        df = pd.read_sql(query, conn, index_col = index)

    else: 
        df = pd.read_sql(query, conn) 

    return df 


def input_into_sql(df, table, how):
    '''
    '''
    username, password, host, port, database = get_sql_details() 

    conn_string  = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(username, password, host, port, database)

    conn = create_engine(conn_string)

    df.to_sql(table, conn, index = False,  if_exists = how)

    return '--table updated--'



def input_sql(query): 
    """
    This function will let you input data into the SQL database
    used for this game. 

    PARAMETERS: 

    query (string): This is the SQL query you wish to use to input the
                    data into the data lake. 

    RETURNS: 
    (string) indicating that the query was successfully carried out.
    """
    username, password, host, port, database = get_sql_details() 


    connection = con.connect(host = host, database = database,
                             user = username, password = password)

    cursor = connection.cursor()  

    cursor.execute(query) 

    connection.commit() 

    cursor.close()

    return '--query inputted--'


def get_current_round(): 
    """
    This function will read the current round for the 
    premier league this will be determined by the API. 

    PARAMETERS: 

    NONE 

    RETURNS: 

    (int) the current number for the permier league  
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