import pandas as pd 

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





