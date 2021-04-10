import pandas as pd 
import utils 
from datetime import datetime


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
    try: 
        query = 'SELECT name, choice FROM choices WHERE round = {}'.format(round_number)

        choices_df = utils.read_from_sql(query, 'name')
        
        if len(choices_df) == 0:

            raise NoDataError
    
    except NoDataError:
        
        print('There were no choices for round {} in the data base'.format(round_number))

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
    query = 'SELECT name, SUM(points) AS scores FROM points GROUP BY name ORDER BY scores DESC'

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
    query = 'SELECT team, apponent, result, scores FROM results WHERE round = {}'.format(round_number)

    results = utils.read_from_sql(query)

    return results

def read_kickoffs(round_number): 
    '''
    This Function will read the earliest and latest kickoffs for 
    a given round from the round_info table in SQL.

    PARAMETERS: 

    round_number (string): This is the round number in which 
    you want to find the kickoffs for. 

    RETRURNS: 

    (earliest_kickoff) A DateTime object for the time of the earliest 
    kickoff for the given round.
    (latest_kickoff) A DateTime object for the time of the latest kickoff 
    for the given round.

    '''
    query = 'SELECT earliest_kickoff, latest_kickoff FROM round_info WHERE round_number = {}'.format(round_number)
    
    kickoffs_df = utils.read_from_sql(query)

    early = kickoffs_df['earliest_kickoff'][0]

    late = kickoffs_df['latest_kickoff'][0]

    earliest_kickoff = datetime.strptime(early, '%Y-%m-%d %H:%M:%S')

    latest_kickoff = datetime.strptime(late, '%Y-%m-%d %H:%M:%S')
    
    return earliest_kickoff, latest_kickoff


def read_last_round_number(): 
    '''
    This Function will read the largest round_number stored in the 
    round_info SQL table

    PARAMETERS: 

    NONE

    RETURS: 

    last_round_number (string) a sting of the biggest round number stored 
    in the round_info SQL table (used as the round_number for the last round)
    '''
    query = 'SELECT round_number FROM round_info ORDER BY round_number DESC LIMIT 1'
    
    last_round_df = utils.read_from_sql(query)

    last_round_number = str(last_round_df['round_number'][0])

    return last_round_number


class NoDataError(Exception):
    pass 