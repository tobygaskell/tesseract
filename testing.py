import utils 
import pandas as pd 
import test as main 
import random, string


teams = []

for i in main.get_team_lists('12')[:4]:
    
    teams = teams + i

print(len(teams)) 

def add_dummy_choices(num_of_players):
    '''
    '''
    query = 'truncate table choices'

    utils.input_sql(query)

    players = [''.join(random.choice(string.ascii_uppercase)for _ in range(10)) for i in range(num_of_players)]
    
    for i in range(int(utils.get_current_round())): 

        for name in players:

            choice = random.choice(teams)

            data = pd.DataFrame({'name':[name], 'choice': [choice], 'round': [(i+1)]})

            utils.input_into_sql(data, 'choices', 'append')


def add_dummy_added_info():
    '''
    '''

    query = 'truncate table round_info'

    utils.input_sql(query)

    for i in range(int(utils.get_current_round())): 

        round = i+1

        DW = main.DP_round() 

        DP = main.draw_weekend(round)
        kickoff = utils.find_earliest_kickoff(str(round)) 
    
        data = pd.DataFrame({'round_number': [round], 'draw_weekend': [DW], 'double_points_weekend':[DP], 'earliest_kickoff':[kickoff]})

        utils.input_into_sql(data, 'round_info', 'append') 


def clear_choices(): 
    '''
    '''
    query = 'truncate table choices'

    return utils.input_sql(query)


def clear_all_tables(): 
    '''
    '''
    for i in ['choices', 'points', 'round_info', 'results']: 

        query = 'truncate table {}'.format(i)

        utils.input_sql(query)

    

