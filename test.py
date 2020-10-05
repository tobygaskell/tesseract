import pandas as pd 
import requests
import json 
import utils


class Players: 

    def __init__(self, name, choice, points_gained, overall_score): 
        self.name = name 
        self.choice = choice
        self.points_gained = points_gained
        self.overall_score = overall_score


class Rounds: 

    def __init__(self, number, fixtures):
        self.number = number 
        self.fixtures = fixtures 


class Fixtures:

    def __init__(self, score, result):
        self.score = score
        self.result = result 


def save_points(df, round_number):
    """
    This function is used to save the csv containing
    the points per round for each player. 

    PARAMETERS: 

    df (DataFrame): This is the DataFrame of points 
    you want to save

    round_number (int): This is the round number for 
    the given round you want to save the points for

    RETURNS: 

    (string): a string indicating that the save has 
    worked.
    """
    df.to_csv(f'points/points_for_round_{round_number}.csv')
    return '-- Points Saved --'


def save_scores(df):
    """
    This function is used to save the csv containing
    the overall scores for each player. 

    PARAMETERS: 

    df (DataFrame): this is the DataFrame of scores 
    you want to save

    RETURNS: 

    (string): a string indicating that the save has 
    worked.
    """
    df.to_csv('overall_scores.csv')

    return '-- Scores Saved -- '


def read_choices():
    """
    This Function will read the choices of teams for
    each player. The choices will be in a text file 
    called team_choices.txt 

    PARAMETERS: 

    None 

    RETURNS: 

    (Dictionary) a dictionary of the team choices with 
    player names as keys and the team choice as the value
    """
    with open('team_choices.txt', 'r') as file_:
        choices = file_.readlines() 

    choices = {i.split('=')[0].strip() : i.split('=')[1].strip() for i in choices}
    
    return choices 


def initilize_scores(choices): 
    """
    This function is used to create an initial csv for 
    the scores. it will have an index with the names and 
    a score column filled with values of 0 

    PARAMETERS: 

    choices (Dict): The dictionary that contains the team choices 

    RETURNS: 

    (string) a string indicating that the Scores have been initialized  
    """
    df = {k:0 for k in choices.keys()}

    scores = pd.DataFrame(df, index = ['Scores']).T

    scores.to_csv('overall_scores.csv')

    return '-- Scores Initialized --'


def update_overall_scores(round_number): 
    """
    This Function will update the overall scores with the 
    scores for the week. 

    PARAMETERS: 

    round_number (int):  This is the round number for 
    the given round for the points you want to update 
    the score with. 

    RETURNS 
    
    (Dictionary) This is the updated scores 
    """

    points = pd.read_csv(f'points/points_for_round_{round_number}.csv', index_col = 0)

    scores = pd.read_csv('overall_scores.csv', index_col = 0)

    for i in points.index: 
        scores['Scores'][i] += points['Points'][i]

    return scores 


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
    headers = utils.get_details() 

    response = requests.request("GET", url, headers=headers)

    data = json.loads(response.text) 

    return data 

def display_data(dict):
    print(json.dumps(dict, indent = 1))


def print_results(raw_data):

    for i in raw_data: 
        print(i['homeTeam']['team_name'], end = ' ') 
        print(i['goalsHomeTeam'], 'vs', i['goalsAwayTeam'], end = ' ' ) 
        print(i['awayTeam']['team_name'])


def find_teams_that_played(raw_data): 
    played  = [i for i in raw_data if i['status'] == 'Match Finished']
    not_played = []
    for i in raw_data: 
        if i['status'] != 'Match Finished':
            not_played.append(i['homeTeam']['team_name'])
            not_played.append(i['awayTeam']['team_name'])
    return played, not_played 
        

def remove_draws(played, draws): 
    for i in played: 
        if i['homeTeam']['team_name'] in draws: 
            played.remove(i)

    return played


def find_winners_and_loosers(wins_and_loss): 
    winners = [i['homeTeam']['team_name'] if i['goalsHomeTeam'] > i['goalsAwayTeam'] else i['awayTeam']['team_name'] for i in wins_and_loss]
    loosers = [i['homeTeam']['team_name'] if i['goalsHomeTeam'] < i['goalsAwayTeam'] else i['awayTeam']['team_name'] for i in wins_and_loss]
    return winners, loosers


def find_draws(played): 
    draws = []
    for i in played: 

        if i['goalsHomeTeam'] == i['goalsAwayTeam']: 
            draws.append(i['homeTeam']['team_name'])
            draws.append(i['awayTeam']['team_name'])
    return draws 


def find_points(round_number, choices): 
    points = {}
    winners, loosers, draws, not_played = get_team_lists(round_number)
    for name, choice in choices.items(): 
        if choice in winners: 
            value = winners_round_worth()
        elif choice in loosers: 
            value = loosers_round_worth()
        elif choice in draws: 
            value = draws_round_worth()
        elif choice in not_played: 
            value = 0 
        else: 
            value = 0

        points[name] = value
    return points

def winners_round_worth(): 
    return 1 

def loosers_round_worth():
    return -1 

def draws_round_worth(): 
    return 0 

def get_team_lists(round_number): 
    round = f'Regular_Season_-_{round_number}'
    data = pull(f"https://api-football-v1.p.rapidapi.com/v2/fixtures/league/2790/{round}")
    played, not_played = find_teams_that_played(data['api']['fixtures'])
    draws = find_draws(played)
    wins_and_loss = remove_draws(played, draws)
    wins, loss = find_winners_and_loosers(wins_and_loss)
    return wins, loss, draws, not_played


def main(round__number): 
    choices = read_choices()
    #initilize_scores(choices)
    points = find_points(round_number, choices)
    points = pd.DataFrame(points, index = ['Points']).T
    save_points(points, round_number)
    scores = update_overall_scores(round_number)
    save_scores(scores)


if __name__ == "__main__": 
    round_number = input('round? ')
    main(round_number)