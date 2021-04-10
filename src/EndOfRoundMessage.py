import FPGLogic as logic 
import ReadFromSql as read 
import utils 
import facebookChatBot as fbcb 


def send_weekly_message(next_round_number, round_number, thread_id, testing = False): 
    '''
    '''
    text = get_weekly_message_text(next_round_number, round_number) 

    if testing == False: 

        uname, pword = utils.get_facebook_details()

        client = fbcb.login_to_facebook(uname, pword)
        
        thread_type = client.fetchThreadInfo(thread_id)[thread_id].type

        fbcb.send_message(text, thread_id, thread_type, client)
    
    return text


def get_weekly_message_text(next_round_number, round_number):
    '''
    '''
    with open('weekly_message.txt') as file: 
        text = file.read() 
    
    scores = get_points_text(round_number)

    standings = get_standings_text()

    fixtures = get_fixtures_text(next_round_number)

    added_info = get_added_info_text(next_round_number)

    return text.format( next_round_number, 
                        round_number, 
                        scores, 
                        round_number, 
                        standings, 
                        next_round_number, 
                        fixtures, 
                        next_round_number, 
                        added_info) 


def get_fixtures_text(round_number):
    '''
    '''
    raw_data = logic.get_raw_data(round_number)

    text = 'Fixtures:\n\n'

    for i in raw_data: 

        text += '{} vs {}\n'.format(i['homeTeam']['team_name'],
                                    i['awayTeam']['team_name']) 

    return text


def get_standings_text(): 
    '''
    '''
    standings = read.read_scores()

    text = "Standings: \n\n"

    for row in standings.iterrows():

        text = text + "{}: {} \n".format(row[1]['name'], int(row[1]['scores']))

    return text


def get_points_text(round_number): 
    '''
    '''
    points = read.read_points(round_number)

    text = "Points: \n\n"

    for row in points.iterrows():

        text = text + "{}: {} \n".format(row[1]['name'], int(row[1]['points']))

    return text 


def get_added_info_text(round_number):
    '''
    '''
    DW, DP = read.read_added_info(round_number)

    text =  """Draw Weekend = {} 
Double Points Weekend = {}""".format(DW, DP)
     
    return text 