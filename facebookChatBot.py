from fbchat import Client
import pandas as pd
import utils
from datetime import datetime 


def login_to_facebook(username, password): 
    '''
    '''
    client = CustomClient(username, password)
    return client 


class CustomClient(Client):

    def onMessage(self, message_object, author_id, thread_id, thread_type, **kwargs):
        '''
        '''
        relevent = check_message(thread_id)

        round_number = utils.get_current_round()

        if relevent: 

            do_stuff(message_object, round_number, False, author_id, thread_id, thread_type) 


# TODO: Remove check_message and add the relevent check into onMessage.

def check_message(thread_id): 
    '''
    '''
    if thread_id == utils.get_thread_id(): 

        relevent_message = True

    else: 
        relevent_message = False 

    return relevent_message


def do_stuff(msg_obj, round_number, testing = False, author_id = False, thread_id = False, thread_type = False):
    '''
    ''' 
    if testing == True: 

        name = msg_obj.author

    else: 

        name = find_author_name(author_id)

    message_type = evaluate_message(msg_obj.text)

    if message_type == 'Team Submission': 

        valid_submission = check_validity(name, msg_obj, round_number)

        if valid_submission:
            
            submitted = check_if_already_submitted(name, round_number)

            if submitted:

                remove_first_choices(name, round_number)

            input_team(name, msg_obj.text, round_number)

    else:
        valid_submission = True 

    text = find_text(msg_obj, name, message_type, valid_submission, round_number) 

    if text != None and testing == False: 

        send_message(text, thread_id, thread_type, client)

    else: 
        return text


def check_if_already_submitted(name, round_number):
    '''
    '''
    query = 'SELECT COUNT(choice) AS num FROM choices WHERE name = "{}" AND round = {}'.format(name, round_number)

    num = utils.read_from_sql(query)['num'][0]

    if num > 0: 

        return True 

    return False 


def remove_first_choices(name, round_number): 
    '''
    '''
    query = 'DELETE FROM choices WHERE name = "{}" AND round = {}'.format(name, round_number )
    utils.input_sql(query)


def check_validity(name, msg_obj, round_number):
    '''
    '''
    time_valid = check_time_validity(msg_obj, round_number)

    choice_valid = check_choice_validity(name, msg_obj.text)

    if time_valid and choice_valid: 
        valid = True 

    else:
        valid = False 

    return valid


def check_time_validity(msg_obj, round_number): 
    '''
    '''

    kick_off = utils.get_earliest_kickoff(round_number)
    
    time = msg_obj.timestamp / 1000 

    print(kick_off, 'vs', time)

    if kick_off.timestamp() <= time: 
        valid = False 

    else: 
        valid = True 

    return valid


def check_choice_validity(name, message): 
    '''
    '''
    team = utils.clean_string(message.split('=')[1])

    query = "SELECT COUNT(*) AS count FROM choices WHERE name = '{}' and choice = '{}'".format(name, team)

    df = utils.read_from_sql(query)

    times_chosen = df['count'][0]  

    if times_chosen >= 2: 

        validity = False 
        
    else: 

        validity = True

    return validity 


def input_team(name, message, round): 
    '''
    '''
    # round = utils.get_current_round()

    team = utils.find_closest_team(message.split('=')[1])

    query = "INSERT INTO choices (name, choice, round) VALUES ('{}', '{}', '{}')".format(name, team, round)

    return utils.input_sql(query)


def find_author_name(author_id): 
    '''
    '''
    user = client.fetchUserInfo(author_id)[author_id]

    return user.name


def evaluate_message(text):
    '''
    '''
    if utils.clean_string(text).startswith('Team'): 
        message_type = 'Team Submission'

    elif utils.clean_string(text) == 'Help': 
        message_type = 'Help Request'

    elif utils.clean_string(text) == 'Standings':
        message_type = 'Standing Request'

    elif utils.clean_string(text) == 'Winning': 
        message_type = 'Winning Request'

    elif utils.clean_string(text) == 'Loosing': 
        message_type = 'Loosing Request'

    elif utils.clean_string(text) == 'Choices':
        message_type = 'Choices Request'

    elif utils.clean_string(text) == 'Fixtures': 
        message_type = 'Fixture Request'

    elif utils.clean_string(text) == 'Position': 
        message_type = 'Position Request'
    
    elif utils.clean_string(text) == 'Rules':
        message_type = 'Rules Request'

    else: 
        message_type = 'Undefined'

    return message_type


def find_text(msg_obj, name, message_type, valid_submission, round_number): 
    '''
    '''
    if message_type == "Help Request": 
        text = help_request_text(name)
        
    elif message_type == 'Team Submission':
        text = get_team_submission_text(name, msg_obj, valid_submission, round_number)

    elif message_type == 'Standing Request': 
        text = standing_request_text(name)
    
    elif message_type == 'Winning Request': 
        text = winning_request_text(name) 
    
    elif message_type == 'Loosing Request': 
        text = loosing_request_text(name)
    
    elif message_type == 'Position Request': 
        text = position_request_text(name)

    elif message_type == 'Choices Request': 
        text = choice_request_text(name)
    
    elif message_type == 'Fixture Request': 
        text = fixture_request_text(name, round_number)
    
    elif message_type == 'Rules Request':
        text = rules_request_text(name)

    else: 
        text = None 

    return text 


def get_team_submission_text(name, msg_obj, valid_submission, round_number): 
    '''
    '''

    if  valid_submission: 
        text = team_submission_text(name, msg_obj.text)

    else:
        time_valid = check_time_validity(msg_obj, round_number)

        choice_valid = check_choice_validity(name, msg_obj.text)

        if time_valid == False: 
            text = time_not_valid_text(name)

        elif choice_valid == False: 
            text = choice_not_valid_text(name, msg_obj.text)

    return text 


def time_not_valid_text(name): 
    '''
    '''
    return "Hi {}, you have missed the deadline for this weeks submission, you will be scores as though the team you picked had lost.".format(name)


def rules_request_text(name): 
    '''
    '''
    with open('documentation/Rules.md') as file: 
        
        text = file.read() 

    return 'Hi {}, {}'.format(name, text)


def choice_not_valid_text(name, text): 
    '''
    '''
    return "Hi {}, you have chosen {} too many times. Please make a new submission".format(name, utils.find_closest_team(text.split('=')[1]))


def team_submission_text(name, text): 
    '''
    '''
    return '''Hi {}, you have submitted {} as your team for this week!

If this is incorrect please redo your submission'''.format(name, utils.find_closest_team(text.split('=')[1]) )


def standing_request_text(name): 
    '''
    '''
    standings = find_standings()[0]

    text =  "Hi {}, The current standings are: \n\n {}".format(name, standings)


    return text 


def position_request_text(name): 
    '''
    '''
    standings_list = find_standings()[1]

    for i in standings_list: 

        if name == i: 
            
            pos = standings_list.index(i) + 1

    if pos == 1: 
        pos = '1st'

    elif pos == 2: 
        pos = '2nd'

    elif pos == 3:
        pos = '3rd'

    elif pos in [4,5,6]:

        pos = str(pos) + 'th'

    return 'Hi {}, you are currently {} in the standings'.format(name, pos)


def choice_request_text(name): 
    '''
    '''
    return 'Hi {}, Sorry this Function is currently not working!!'.format(name)


def winning_request_text(name): 
    '''
    '''
    standings_list = find_standings()[1]

    winning = standings_list[0]

    return 'Hi {}, {} is currently top of the standings.'.format(name, winning)


def loosing_request_text(name): 
    '''
    '''
    standings_list = find_standings()[1]

    loosing = standings_list[len(standings_list)-1]

    return 'Hi {}, {} is currently bottom of the standings.'.format(name, loosing)


def find_standings(): 
    '''
    '''
    query = 'SELECT name, sum(score) as points FROM scores GROUP BY name ORDER BY points DESC'

    standings = utils.read_from_sql(query)

    standings_list  = list(standings['name'])

    standings = str(standings)

    print(standings, standings_list )

    return standings, standings_list 


def fixture_request_text(name, round_number):
    '''
    '''

    round = 'Regular_Season_-_{}'.format(round_number)

    text = 'Hi {}, the fixtures for Round {} are: \n\n'.format(name, round_number)

    data = utils.pull("https://api-football-v1.p.rapidapi.com/v2/fixtures/league/2790/{}".format(round))

    raw_data = data['api']['fixtures']

    for i in raw_data: 

        text += '{} vs {}\n'.format(i['homeTeam']['team_name'],i['awayTeam']['team_name']) 

    return text


def help_request_text(name): 
    '''
    '''
    with open('help.txt','r') as file: 

        help_string = file.read()

    return "Hi, {}".format(name) + help_string 


def send_message(text, thread_id, thread_type, client): 
    '''
    '''
    client.sendMessage(text, thread_id, thread_type)

    return '--Message Sent--'


if __name__ == "__main__": 

    uname, pword = utils.get_facebook_details() 

    client = CustomClient(uname, pword) 

    client.listen()