import utils 
import pandas as pd 
import test as main 
import random, string


teams = []

for i in main.get_team_lists('12')[:4]:
    
    teams = teams + i

def add_dummy_choices(num_of_players):

    players = [''.join(random.choice(string.ascii_uppercase)for _ in range(10)) for i in range(num_of_players)]
    
    for i in range(int(utils.get_current_round())): 

        for name in players:

            choice = random.choice(teams)

            data = pd.DataFrame({'name':[name], 'choice': [choice], 'round': [(i+1)]})

            utils.input_into_sql(data, 'choices', 'append')


def add_dummy_added_info():

    for i in range(int(utils.get_current_round())): 

        round = i+1

        DW = main.DP_round() 

        DP = main.draw_weekend(round)

        data = pd.DataFrame({'round_number': [round], 'draw_weekend': [DW], 'double_points_weekend':[DP]})

        utils.input_into_sql(data, 'round_info', 'append') 