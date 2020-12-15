import pandas as pd 
import utils
import random 
import facebookChatBot as fbcb 

def read_choices(round_number):
    '''
    This Function will read the choices of teams for
    each player. The choices will be stored in an SQL 
    table called choices. 

    PARAMETERS: 

    round_number (string): This is the round number you want
    to read the choices for. 

    RETURNS: 

    (Dictionary) A dictionary of the team choices with 
    player names as keys and the team choice as the value
    '''
    query = 'select name, choice from choices where round = {}'.format(round_number)

    choices_df = utils.read_from_sql(query, 'name')

    choices = choices_df.to_dict(orient='index')    

    choices = {k:v['choice'] for k,v in choices.items()}

    return choices 
    

def read_scores(round_number): 
    '''
    This Function will read the points gained for each 
    player from a specified round. 

    PARAMETERS: 

    round_number (string): This is the round number you want
    to read the choices for. 

    RETURNS: 

    (DataFrame) A DataFrame with two columns called name and 
    points containing the points data for each player for a 
    specific round
    '''
    query = 'SELECT name, sum(points) as scores FROM points WHERE round = {} GROUP BY name ORDER BY scores'.format(round_number)

    points = utils.read_from_sql(query, 'name')

    return points 

def read_added_info(round_number): 
    '''
    '''
    query = 'SELECT draw_weekend, double_points_weekend FROM round_info WHERE round_number = {}'.format(round_number)

    added_info = utils.read_from_sql(query)

    DW = bool(added_info['draw_weekend'][0])

    DP = bool(added_info['double_points_weekend'][0])

    return DW, DP

def read_points(round_number): 
    '''
    '''
    query = 'SELECT name, points FROM points WHERE round = {} ORDER BY points'.format(round_number)

    points = utils.read_from_sql(query, 'name')

    return points


def read_results(round_number): 
    '''
    '''
    query = 'SELECT * FROM results WHERE round = {}'.format(round_number)

    results = utils.read_from_sql(query)

    return results


def update_overall_scores(round_number): 
    '''
    This Function will update the overall scores with the 
    scores for the week. 

    PARAMETERS: 

    round_number (int):  This is the round number for 
    the given round for the points you want to update 
    the score with. 

    RETURNS 
    
    (Dictionary) This is the updated scores 
    '''
    points = read_points(round_number)

    scores = read_scores(round_number)

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

    data['round'] = round_number

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

    DW, DP = read_added_info(round_number)

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

    return points


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
    round = 'Regular_Season_-_{}'.format(round_number)

    data = utils.pull("https://api-football-v1.p.rapidapi.com/v2/fixtures/league/2790/{}".format(round))

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


def send_weekly_message(new_round, round_number, thread_id): 
    '''
    '''
    uname, pword = utils.get_facebook_details()

    client = fbcb.login_to_facebook(uname, pword)

    thread_type = client.fetchThreadInfo(thread_id)[thread_id].type

    text = get_weekly_message_text(new_round, round_number) 

    fbcb.send_message(text, thread_id, thread_type, client)


def get_weekly_message_text(new_round, round_number):
    '''
    '''
    with open('weekly_message.txt') as file: 
        text = file.read() 

    scores = get_scores_text(round_number)

    standings = get_standings_text()

    fixtures = get_fixtures_text(new_round)

    added_info = get_added_info_text(new_round)

    return text.format(new_round, round_number, scores, round_number, standings, new_round, fixtures, new_round, added_info) 


def get_fixtures_text(round_number):
    '''
    '''
    round = 'Regular_Season_-_{}'.format(round_number)

    text = 'Fixtures:\n\n'

    data = utils.pull("https://api-football-v1.p.rapidapi.com/v2/fixtures/league/2790/{}".format(round))

    raw_data = data['api']['fixtures']

    for i in raw_data: 

        text += '{} vs {}\n'.format(i['homeTeam']['team_name'],i['awayTeam']['team_name']) 

    return text

def get_standings_text(): 
    '''
    '''
    query = 'SELECT name, sum(points) as points FROM points GROUP BY name ORDER BY points DESC'

    standings = utils.read_from_sql(query)

    text = "Standings: \n\n"

    for row in standings.iterrows():

        text = text + "{}: {} \n".format(row[1]['name'], int(row[1]['points']))

    return text


def get_scores_text(round_number): 
    '''
    '''
    query = "SELECT name, sum(points) AS scores FROM points WHERE round = {} GROUP BY name ORDER BY scores DESC".format(round_number)

    scores = utils.read_from_sql(query)

    text = "Scores: \n\n"

    for row in scores.iterrows():

        text = text + "{}: {} \n".format(row[1]['name'], int(row[1]['scores']))

    return text 

def get_added_info_text(round_number):
    '''
    '''
    DW , DP = read_added_info(round_number)

    text =  """Draw Weekend = {} 
Double Points Weekend = {}""".format(DW, DP)
     
    return text 
    

def main(new_round, round_number): 
    """
    """
    choices = read_choices(round_number)

    print(len(choices))

    if len(choices) == 0: 

        with open('intro.txt') as file:

            text = file.read() 

            text = text.format(get_fixtures_text(new_round))

        uname, pword = utils.get_facebook_details()

        client = fbcb.login_to_facebook(uname, pword)

        thread_type = client.fetchThreadInfo('3365583033489198')['3365583033489198'].type

        fbcb.send_message(text, '3365583033489198', thread_type, client)

        return True  

    save_results(round_number)

    points = find_points(round_number, choices)

    utils.input_into_sql(points, 'points', 'append')

    send_weekly_message(new_round, round_number,'3365583033489198')

# if __name__ == '__main__':
#     main('12','11')

hello this is an insertion 