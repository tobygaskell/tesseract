import utils
import pandas as pd 
import ReadFromSql as read 

def get_raw_data(round_number): 
    '''
    This Function will read down the raw data for the fixtures 
    for the given round. This data includes the final score after 
    the game has been played. 

    PARAMETERS: 

    round_number (string): This is the round number for which you 
    want to pull down the fixtures data. 

    RETURNS: 

    (raw_data) This is a list of fixture objects which in turn are in 
    Json/Dict format.  
    '''
    data = utils.pull("https://api-football-v1.p.rapidapi.com/v2/fixtures/league/2790/Regular_Season_-_{}".format(round_number))

    raw_data = data['api']['fixtures']
    
    return raw_data


def find_teams_that_played(raw_data): 
    '''
    This Function will filter out the teams into two lists,
    One containing the teams that finished the game, the 
    other the teams who play didn't finish. 

    PARAMETERS: 

    raw_data (json): This is the output for the get raw_data function 
    which in turn outputs the raw data from the football API when we
    ask for the results after the round has finished.

    RETURNS 

    (played) A list containing the fixture objects for the 
    teams who finished there game. 
    # (not_played) A list containing the names of the teams who 
    # didn't finish the game.
    '''
    played  = [i for i in raw_data if i['status'] == 'Match Finished']
 
    return played


def find_draws(played): 
    '''
    This Function will identify any fixture from then given round which 
    ended in a draw. 

    PARAMETERS:

    played (List): This is the output of the find_teams_that_played 
    function which in turn returns a list of the fixture objects for teams 
    that ended there game.

    RETURNS: 

    (draws) This is a list of team names for the teams whos fixture ended in 
    a draw.
    '''
    draws = []

    for i in played: 

        if i['goalsHomeTeam'] == i['goalsAwayTeam']: 

            draws.append(i['homeTeam']['team_name'])

            draws.append(i['awayTeam']['team_name'])

    return draws 


def remove_draws(played, draws): 
    '''
    This Function will remove the fixture objects from the list of teams 
    that played for each team that drew. This will just leave the fixtures 
    whos result ended in a win for either the home or away team. 

    PARAMETERS: 

    played (List): This is the output of the find_teams_that played 
    function which in turn returns a list of the fixture objects for 
    teams that ended the game 

    draws (List): This is the output of the find_draws function which inturn 
    returns a list of the team names for each team whos game ended in a draw 

    RETURNS: 

    no_draws (list): This is a list of the fixtures objects which ended in a 
    win for either the home or away team.   
    '''
    no_draws = []

    for i in played: 

        if i['homeTeam']['team_name'] not in draws: 

            no_draws.append(i)

    return no_draws


def find_winners_and_loosers(wins_and_loss):
    '''
    This Functoin will split the list of fixture objects for fixtures that ended 
    in a win for either the home or away team into two lists one containing the 
    names of the teams that won and the other containing the list that lost 

    PARAMETERS: 

    wins_and_loss (List): This is a list of fixture objects conatining only the 
    fixtures that ended in a win for either the home or away team 

    RETURNS: 

    (winners) This is the list of team names for the teams that have won in this 
    round 
    (loosers) This is the list of the team names for the teams that have lost 
    in this round. 
    '''
    winners = [i['homeTeam']['team_name'] if i['goalsHomeTeam'] > i['goalsAwayTeam'] 
                                          else i['awayTeam']['team_name'] for i in wins_and_loss]

    loosers = [i['homeTeam']['team_name'] if i['goalsHomeTeam'] < i['goalsAwayTeam'] 
                                          else i['awayTeam']['team_name'] for i in wins_and_loss]
    return winners, loosers


def get_team_lists(played): 
    '''
    This function will split the teams who played in the given round 
    into three lists 1 for the teams that won, one for the ones that drew 
    and one for the ones that lost. 

    PARAMETERS: 

    played (List): This is the output of the find_teams_that_played 
    function which in turn returns a list of the fixture objects for 
    teams that ended the game 

    RETURNS: 

    (wins) This is the list of teams who won that round. 
    (loss) This is the list of teams who lost that round. 
    (draws) This is the list of team who drew that round. 
    '''
    draws = find_draws(played)

    wins_and_loss = remove_draws(played, draws)

    wins, loss = find_winners_and_loosers(wins_and_loss)

    return wins, loss, draws


# TODO: get it so that this function also saves the results for teams who havent played. 

def save_results(round_number, played, winners, loosers, draws): 
    '''
    This Function will take the cleaned data from the API and 
    save it into tabular form in our SQL database. The table has 
    5 Columns team which is the team in question, apponent which 
    is the team who the team in question was playing for that round 
    results is if the team won, lost or drew. Finally score is the 
    final score of the round. 

    PARAMETERS: 

    round_number (string): The round number in which you are saving the 
    results from. 
    played (list): The list of fixture objects, for which the game finnished. 
    winners (list):The list of the team names for the teams who won that round.
    loosers (list): The list of the team names for the teams who lost that round.
    draws (list): The list of the team names for the teams that drew that round. 

    RETURNS 

    inputted (boolean) True if the data was inputted successfully and False if the 
    data input didn't work.
    '''
    data = {'team':[],'apponent': [],'result': [],'scores': []} 

    for i in played: 

        data['team'].append(i['homeTeam']['team_name'])

        data['apponent'].append(i['awayTeam']['team_name'])

        data['result'].append(get_result(i['homeTeam']['team_name'], winners, loosers, draws))

        data['scores'].append('{} - {}'.format(i['goalsHomeTeam'],i['goalsAwayTeam']))

        data['team'].append(i['awayTeam']['team_name'])

        data['apponent'].append(i['homeTeam']['team_name'])

        data['result'].append(get_result(i['awayTeam']['team_name'],  winners, loosers, draws))

        data['scores'].append('{} - {}'.format(i['goalsAwayTeam'],i['goalsHomeTeam']))

    data['round'] = round_number

    df = pd.DataFrame(data)

    inputted = utils.input_into_sql(df, 'results', 'append')

    return inputted  


def get_result(team_name, winners, loosers, draws):
    '''
    This Function will check to see what the result was for 
    any given team. 

    PARAMETERS: 

    team_name (string): This is the name of the team you want 
    to find out the result for.
    winners (list): This is the list of teams that have won 
    that round.
    loosers (list): This is the list of teams that have lost 
    that round.
    draws (list): This is the list of teams that drew that round.

    RETURNS: 

    result (string) this is whether the given team won lost or 
    drew. Will return winner, looser, draw respectectively if 
    the result cant be found will return N/A.
    '''
    if team_name in winners: 
        result = 'winner'

    elif team_name in loosers: 
        result = 'looser'

    elif team_name in draws: 
        result = 'draw'

    else: 
        result = 'N/A'

    return result 


def find_points(round_number, choices, winners, loosers, draws): 
    '''
    This Function will find the points that each player has gained 
    for that round given the choices they made. 

    PARAMETERS: 

    round_number (string): This is the round for which you want to 
    find the points for. 
    choices (dict): this is the output of the read_choices function 
    which in turn outputs a dictionary with the key as the players  
    and the choice as the value 
    winners (list): This is the list of teams that have won that round.
    loosers (list): This is the list of teams that have lost that round.
    draws (list): This is the list of teams that drew that round.

    RETRUNS: 

    points (DataFrame): This table will have 3 columns, name which is 
    the name of the player, points which is the number of points that 
    player has gained this round and round which is the round number.
    '''
    points = {}

    DW, DP = read.read_added_info(round_number)

    for name, choice in choices.items(): 

        if choice in winners: 
            value = round_worth(1, choice, choices, round_number, DP) 

        elif choice in loosers: 
            value = round_worth(-1, choice, choices, round_number, DP)

        elif choice in draws: 
            value = draws_round_worth(0, choice, round_number, DW)

        else: 
            value = 0

        points[name] = value

    points = pd.DataFrame(points, index = ['points']).T

    points = points.reset_index()

    points['round'] = round_number

    points.columns = ['name', 'points', 'round']

    return points


def round_worth(value, choice, choices, round_number, double_points): 
    '''
    The Function will work out the value for the point each player
    has gained. This will change if the choice was playing in a derby 
    in a head to head or if it was a draw_weekend. 

    PARAMETERS: 

    value (int): This is the points before we calculate the added rules 
    1 for a win, 0 for a draw and -1 for a draw. 
    choice (string): this is the name of the team that the player has picked.
    choices (dict): this is the output of the read_choices function 
    which in turn outputs a dictionary with the key as the players  
    and the choice as the value.
    round_number (string): This is the round for which you are figuring 
    out the points worth for. 
    double_points (bool): 

    RETURNS: 

    value (int) This is the new value for the points gained in this round 
    for the given choice.
    '''
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
    ''' 
    This Function will work out the points value for the 
    weeks when there is a draw_weekend. if you played in a 
    derby you get -1 if it is a draw weekend then you get your
    score multipled by 3.

    PARAMETERS: 

    value (int): This is the points value already calculated 
    choice (string): This is the team name for the team the 
    player chose 
    round_number (string): This is the current round number 
    draw_weekend (bool): This is whether or not the round is
    a draw_weekend or not 

    RETURNS: 

    value (int) This is the new points value for when it is a 
    draw_weekend.
    '''
    derby = played_in_a_derby(choice, round_number)

    if derby: 
        value = -1 

    if draw_weekend:

        if value == 0: 

            value = 1 

        value *= 3 

    return value

# TODO: Figure out a better way to do the derbies. I do not like the hard coded list.

def played_in_a_derby(choice, round_number): 
    '''
    This Function will figure out if the choice made 
    was playing in a derby or not. The derbys are a 
    hardcoded predefined list of fixtures. 

    PARAMETERS: 

    choice (string): This is the choice you wish to check 
    to see if it played in a derby 
    round_number (string): This is the round number for which 
    you want to check and see if the team chosen was playing in 
    a derby. 

    RETURNS: 

    derby (bool) True if the choice played in a derby False
    if it did not. 
    '''
    results = read.read_results(round_number)

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

        else: 
            derby = False 

    return derby 


def played_head_to_head(choice, choices, round_number):
    '''
    This Function will figure out if the choice made 
    was playing in a head_to_head or not. 

    PARAMETERS: 

    choice (string): This is the choice you wish to check 
    to see if it played in a derby.
    choices (dict): This is the output for the read_choices 
    function. Which in turn returns a dict whith the names as 
    the keys and the choices for a given round as the values.
    round_number (string): This is the round number for which 
    you want to check and see if the team chosen was playing in 
    a derby. 

    RETURNS: 

    derby (bool) True if the choice played in a derby False
    if it did not. 
    '''
    results = read.read_results(round_number)

    if results[results['team'] == choice]['apponent'].values[0] in choices.values(): 

        head_to_head = True

    else: 

        head_to_head = False

    return head_to_head


def run_game_logic(round_number, testing = False): 
    '''
    This Function is the main command function for this script. 
    it will run all the required functions in order to read the 
    choices from sql and output the points gained for the given 
    round. 

    PARAMETERS: 

    round_number (string): This is the round you want to run the
    game logic for.
    testing (bool): if you want to test the script or no.

    RETURNS:

    inputted (bool) True if the points data is inputted successfully 
    False if the data isn't saved correctly.  
    '''
    choices = read.read_choices(round_number)

    raw_data = get_raw_data(round_number)

    played = find_teams_that_played(raw_data)

    winners, loosers, draws = get_team_lists(played)

    save_results(round_number, played, winners, loosers, draws )

    points = find_points(round_number, choices, winners, loosers, draws)

    inputted = utils.input_into_sql(points, 'points', 'append')

    return inputted 