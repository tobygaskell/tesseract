import pandas as pd 
import test as main 
import facebookChatBot as FB
import random, string, time, utils 
from datetime import datetime, timedelta
from crontab_test import save_current_round


def add_dummy_choices(num_of_players):
    '''
    '''
    query = 'truncate table choices'

    utils.input_sql(query)

    players = [''.join(random.choice(string.ascii_uppercase)for _ in range(10)) for i in range(num_of_players)]
    
    for i in range(int(utils.get_current_round())): 

        for name in players:

            choice = random.choice(utils.get_all_teams())

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

        DP = main.draw_weekend()
        
        earliest_kickoff, latest_kickoff = utils.find_kickoffs(str(round)) 
    
        data = pd.DataFrame({'round_number': [round],
                         'draw_weekend': [DW], 
                         'double_points_weekend': [DP], 
                         'earliest_kickoff': [earliest_kickoff],
                         'latest_kickoff': [latest_kickoff],
                         'start_of_round': [latest_kickoff]})

        utils.input_into_sql(data, 'round_info', 'append') 

def add_dummy_choices2(num): 
    '''
    '''
    players = ['Toby', 'Val', 'Dylan']

    # teams = utils.get_all_teams() 

    while num > 0: 

        if num in [1,2]:

            choices = pd.DataFrame({'name': players, 'choice':['Manchester United' for  i in players], 'round':[1 for i in players]})

            utils.input_into_sql(choices, 'choices', 'replace')

        num -= 1 
    return 'Added'


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

    
class Player: 

    def __init__(self, name): 
        '''
        '''
        self.name = name 

    def make_a_choice(self, manual = False): 
        '''
        '''
        if manual == False: 

            team = random.choice(utils.get_all_teams())

        else: 

            team = manual 

        return FBmessage('Team = {}'.format(team), self.name)
    
    def ask_for_standings(self): 
        '''
        '''
        return FBmessage('Standings', self.name) 

    def ask_for_help(self): 
        '''
        '''
        return FBmessage('Help', self.name) 

    def ask_whos_winning(self): 
        '''
        '''
        return FBmessage('Winning', self.name) 

    def ask_whos_loosing(self): 
        '''
        '''
        return FBmessage('Loosing', self.name) 

    def ask_for_position(self):
        '''
        '''
        return FBmessage('Position', self.name) 
    
    def ask_for_choices(self): 
        '''
        '''
        return FBmessage('Choices', self.name) 
    
    def ask_for_fixtures(self): 
        '''
        '''
        return FBmessage('Fixtures', self.name) 
    
    def ask_for_rules(self): 
        '''
        '''
        return FBmessage('Rules', self.name) 


class FBmessage: 

    def __init__(self, text, author):
        '''
        '''
        self.text = text 

        self.author = author
        
        self.timestamp = datetime.now().timestamp() 


class Round:

    def __init__(self, round_number = False):
        '''
        '''
        if round_number == False: 

            self.round_number =  utils.get_current_round()  

        else:
             self.round_number = round_number 
            
        self.draw_weekend = main.draw_weekend() 

        self.double_points_weekend = main.DP_round() 
        
        self.start_of_round = datetime.now()

        self.earliest_kickoff = datetime.now() + timedelta(minutes = 1)

        self.end_of_round = datetime.now() + timedelta(minutes = 2)

    def save_round_details(self): 
        '''
        '''
        save_current_round(self.round_number,
                           True,    
                           self.draw_weekend, 
                           self.double_points_weekend, 
                           str(self.earliest_kickoff)[:-7],
                           str(self.start_of_round)[:-7],
                           str(self.end_of_round)[:-7])




def test(): 
    '''
    '''
    clear_all_tables() 

    old_round = Round('1')

    old_round.save_round_details() 

    players = ['Toby', 'Val', 'Dylan']

    for i in players: 

        player = Player(i)

        msg_obj = player.make_a_choice()

        print(FB.do_stuff(msg_obj, old_round.round_number, True))

    time.sleep(65)

    for i in players: 

        player = Player(i)

        msg_obj = player.make_a_choice()

        print(FB.do_stuff(msg_obj,old_round.round_number, True))

    time.sleep(55)

    new_round = Round('2')

    new_round.save_round_details() 

    return main.main('2', '1', True)