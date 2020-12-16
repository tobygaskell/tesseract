import pandas as pd 
import utils 


def read_choices(round_number):
    '''
    This Function will read the choices of teams for
    each player. The choices will be stored in an SQL 
    table called choices. 

    PARAMETERS: 

    round_number (string): This is the round number you want
    to read the choices for. 

    RETURNS: 

    (choices) A Dictionary of the team choices with 
    player names as keys and the team choice as the value
    '''
    query = 'SELECT name, choice FROM choices WHERE round = {}'.format(round_number)

    choices_df = utils.read_from_sql(query, 'name')

    choices = choices_df.to_dict(orient='index')    

    choices = {k:v['choice'] for k,v in choices.items()}

    return choices 


def read_added_info(round_number): 
    '''
    This Function will read the weekly added info (Whether 
    or nor the round is a double point round or a draw weekend)
    for the given round. 

    PARAMETERS: 

    round_number (string): This is the round number you want 
    to read the added info for 

    RETURNS 

    (Dw) A Bool indicating if the round is a draw weekend or not. 
    (DP) A Bool indicating if the round is a double points weekend or not 
    '''
    query = 'SELECT draw_weekend, double_points_weekend FROM round_info WHERE round_number = {}'.format(round_number)

    added_info = utils.read_from_sql(query)

    DW = bool(added_info['draw_weekend'][0])

    DP = bool(added_info['double_points_weekend'][0])

    return DW, DP


def read_scores(): 
    '''
    This Function will read the overall scores for each player up 
    until the point in which the function is called. 

    PARAMETERS: 

    NONE 

    RETURNS: 

    (scores) A DataFrame with two columns called name and 
    scores containing the scores data for each player.
    '''
    query = 'SELECT name, SUM(points) AS scores FROM points GROUP BY name ORDER BY scores'

    scores = utils.read_from_sql(query, 'name')

    return scores 


def read_points(round_number): 
    '''
    This Function will read the points gained for each player 
    in a specified round. 

    PARAMETERS: 

    round_number (string): This is the round number in which you 
    want to find out what points everyone got.

    RETURNS: 

    (points) A DataFrame with two columns called name and 
    points which will contain the points data for each player
    for that round.
    '''
    query = 'SELECT name, points FROM points WHERE round = {} ORDER BY points'.format(round_number)

    points = utils.read_from_sql(query, 'name')

    return points


def read_results(round_number): 
    '''
    This Function will read the results for a specified round 
    from the SQL table called results. 

    PARAMETERS: 

    round_number (string): This is the round number in which 
    you want to find the results. 

    RETURNS: 

    (results) A DataFrame with 4 columns team, apponent, result, score.
    Team contains the team names, the apponent is the name of the team they 
    played in that round, results whether the won lost or drew. 
    '''
    query = 'SELECT name, apponent, result, score FROM results WHERE round = {}'.format(round_number)

    results = utils.read_from_sql(query)

    return results
