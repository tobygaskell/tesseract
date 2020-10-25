import pandas as pd 
import utils
import random 


# def save_points(df, round_number):
#     """
#     This function is used to save the csv containing
#     the points per round for each player. 

#     PARAMETERS: 

#     df (DataFrame): This is the DataFrame of points 
#     you want to save

#     round_number (int): This is the round number for 
#     the given round you want to save the points for

#     RETURNS: 

#     (string): a string indicating that the save has 
#     worked.
#     """
#     df.to_sql('points', conn,  if_exists = 'append')

#     return '-- Points Saved --'


# def save_scores(df):
#     """
#     This function is used to save the csv containing
#     the overall scores for each player. 

#     PARAMETERS: 

#     df (DataFrame): this is the DataFrame of scores 
#     you want to save

#     RETURNS: 

#     (string): a string indicating that the save has 
#     worked.
#     """
#     df.to_sql('scores', conn, if_exists = 'replace')

#     return '-- Scores Saved -- '


def read_choices(round_number):
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
    query = 'select name, choice from choices where round = {}'.format(round_number)

    choices_df = utils.read_from_sql(query, 'name')

    choices = choices_df.to_dict(orient='index')    

    choices = {k:v['choice'] for k,v in choices.items()}

    return choices 

def read_points(round_number): 
    '''
    '''
    query = 'SELECT name, points FROM points WHERE round = {}'.format(round_number)

    points = utils.read_from_sql(query, 'name')

    return points 



def read_scores(round_number): 
    '''
    '''
    query = 'SELECT name, score FROM scores WHERE round = {} ORDER BY score'.format(round_number)

    scores = utils.read_from_sql(query, 'name')

    return scores


def read_results(round_number): 
    '''
    '''
    query = 'SELECT * FROM results WHERE round = {}'.format(round_number)

    results = utils.read_from_sql(query)

    return results


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
    points = read_points(round_number)

    scores = read_scores('1')

    for i in points.index: 

        scores['score'][i] += points['points'][i]

    return scores 


def find_teams_that_played(raw_data): 
    """
    """
    played  = [i for i in raw_data if i['status'] == 'Match Finished']

    not_played = []

    for i in raw_data: 

        if i['status'] != 'Match Finished':

            not_played.append(i['homeTeam']['team_name'])

            not_played.append(i['awayTeam']['team_name'])
 
    return played, not_played 


def save_results(round_number): 
    """
    """
    played = get_team_lists(round_number)[4]

    data = {'team':[],'apponent': [],'result': [],'scores': []} 

    for i in played: 

        data['team'].append(i['homeTeam']['team_name'])

        data['apponent'].append(i['awayTeam']['team_name'])

        data['result'].append(get_result(i['homeTeam']['team_name'], round_number))

        data['scores'].append('{} - {}'.format(i['goalsHomeTeam'],i['goalsAwayTeam']))

        data['team'].append(i['awayTeam']['team_name'])

        data['apponent'].append(i['homeTeam']['team_name'])

        data['result'].append(get_result(i['awayTeam']['team_name'], round_number))

        data['scores'].append('{} - {}'.format(i['goalsAwayTeam'],i['goalsHomeTeam']))

    data['round'] = utils.get_current_round() 

    df = pd.DataFrame(data)

    return utils.input_into_sql(df, 'results', 'append')


def get_result(team_name, round_number):
    """
    """
    winners, loosers, draws = get_team_lists(round_number)[:3]

    if team_name in winners: 
        result = 'winner'

    elif team_name in loosers: 
        result = 'looser'

    elif team_name in draws: 
        result = 'draw'

    else: 
        result = 'N/A'

    return result 


def remove_draws(played, draws): 
    """
    """
    played_ = []

    for i in played: 

        if i['homeTeam']['team_name'] not in draws: 
            played_.append(i)

    return played_


def find_winners_and_loosers(wins_and_loss):
    """
    """ 
    winners = [i['homeTeam']['team_name'] if i['goalsHomeTeam'] > i['goalsAwayTeam'] 
                                          else i['awayTeam']['team_name'] for i in wins_and_loss]

    loosers = [i['homeTeam']['team_name'] if i['goalsHomeTeam'] < i['goalsAwayTeam'] 
                                          else i['awayTeam']['team_name'] for i in wins_and_loss]
    return winners, loosers


def find_draws(played): 
    """
    """
    draws = []
    for i in played: 

        if i['goalsHomeTeam'] == i['goalsAwayTeam']: 

            draws.append(i['homeTeam']['team_name'])

            draws.append(i['awayTeam']['team_name'])
    return draws 


def find_points(round_number, choices): 
    """
    """
    points = {}

    DP = DP_round()

    DW = draw_weekend(round_number)

    winners, loosers, draws, not_played = get_team_lists(round_number)[:4]

    for name, choice in choices.items(): 

        if choice in winners: 
            value = round_worth(1, choice, choices, round_number, DP) 

        elif choice in loosers: 
            value = round_worth(-1, choice, choices, round_number, DP)

        elif choice in draws: 
            value = draws_round_worth(0, choice, round_number, DW)

        elif choice in not_played: 
            value = 0 

        else: 
            value = 0

        points[name] = value

    points = pd.DataFrame(points, index = ['points']).T

    points = points.reset_index()

    points['round'] = round_number

    points.columns = ['name', 'points', 'round']

    return points, DP, DW


def DP_round(): 
    """
    """
    return random.randrange(10) > 8  


def draw_weekend(round_number): 
    """
    """
    return random.randrange(100) > 80



def round_worth(value, choice, choices, round_number, double_points): 
    """
    """
    derby = played_in_a_derby(choice, round_number) 

    head_to_head = played_head_to_head(choice, choices, round_number) 

    if double_points == True: 
        value *= 2 

    if head_to_head == True: 
        value *= 2

    if derby == True: 
        value *= 2

    return value  


def draws_round_worth(value, choice, round_number, draw_weekend):
    """
    """
    derby = played_in_a_derby(choice, round_number)

    if derby == True: 
        value = -1 

    if draw_weekend == True:

        if value == 0: 

            value = 1 

        value *= 3 

    return value


def played_in_a_derby(choice, round_number): 
    """
    """
    derby = False

    results = read_results(round_number)

    derbys = [('Manchester United', 'Manchester City'), ('Liverpool' , 'Everton'),
              ('Arsenal' , 'Tottenham'), ('Chelsea', 'Fulham'),
              ('Manchester City' , 'Liverpool'), ('Leeds ', 'Manchester United'),
              ('Sheffield' , 'Leeds Utd'), ('Man Utd ', 'Liverpool'), 
              ('West Brom' , 'Aston Villa'), ('Wolves' , 'West Brom'), 
              ('Wolves' , 'Aston Villa')]

    for i in derbys: 

        if choice == i[0] and i[1] == results[results['team'] == choice]['apponent'].values[0]: 
            derby =  True 

        elif choice == i[1] and i[0] == results[results['team'] == choice]['apponent'].values[0]:  
            derby =  True 

    return derby 


def played_head_to_head(choice, choices, round_number):
    """
    """
    results = read_results(round_number)

    if results[results['team'] == choice]['apponent'].values[0] in choices.values(): 

        head_to_head = True

    else: 

        head_to_head = False

    return head_to_head


def initilize_choice_tracker(choices): 
    """
    """
    teams = get_all_teams()

    dic = {k:[0 for i in range(len(teams))] for k in choices.keys()}

    pd.DataFrame(dic, index = teams).to_csv('choice_tracker.csv')

    return '-- choice tracker initialized --'


def get_all_teams(): 
    """
    """
    data = utils.pull('https://api-football-v1.p.rapidapi.com/v2/teams/league/2790') 

    teams = [i['name'] for i in data['api']['teams']]

    return teams 


def update_choice_tracker(choices):

    tracker = pd.read_csv('choice_tracker.csv', index_col = 0)

    for k,v in choices.items():

        tracker[k][v] += 1

    tracker.to_csv('choice_tracker.csv')

    return '-- Updated choice tracker --'


def get_team_lists(round_number): 
    """
    """
    round = f'Regular_Season_-_{round_number}'

    data = utils.pull(f"https://api-football-v1.p.rapidapi.com/v2/fixtures/league/2790/{round}")

    played, not_played = find_teams_that_played(data['api']['fixtures'])

    draws = find_draws(played)

    wins_and_loss = remove_draws(played, draws)

    wins, loss = find_winners_and_loosers(wins_and_loss)

    return wins, loss, draws, not_played, played 

def initialize_scores(choices):
    '''
    '''
    df = {k:0 for k in choices.keys()}

    scores = pd.DataFrame(df, index = ['scores']).T

    scores = scores.reset_index()

    scores['round'] = '1'

    scores.columns = ['name', 'score', 'round']
    
    utils.input_into_sql(scores, 'scores', 'append')


def main(): 
    """
    """
    round_number = utils.get_current_round()

    choices = read_choices(round_number)

    save_results(round_number)

    points, double_weekend, draw_weekend = find_points(round_number, choices)

    utils.input_into_sql(points, 'points', 'append')

    initialize_scores(choices) 

    scores = update_overall_scores(round_number)

    utils.input_into_sql(scores, 'scores', 'append')

    print('Draw Weekend = ', draw_weekend)

    print('Double Weekend = ', double_weekend)


if __name__ == "__main__": 
   main()  

