import utils 
from datetime import datetime
import test as main 
import pandas as pd 
import ReadFromSql as read

def save_current_round(round_number, testing = False, DW = False, DP = False, earliest_kickoff = False, start_of_round = False, latest_kickoff = False):
    '''
    '''
    if testing == False:

        DW = main.DP_round()
        
        DP = main.draw_weekend()

        earliest_kickoff, latest_kickoff = utils.find_kickoffs(round_number)

        start_of_round = datetime.now()

    data = pd.DataFrame({'round_number': [round_number],
                         'draw_weekend': [DW], 
                         'double_points_weekend': [DP], 
                         'earliest_kickoff': [earliest_kickoff],
                         'latest_kickoff': [latest_kickoff],
                         'start_of_round': [start_of_round]})

    utils.input_into_sql(data, 'round_info', 'append')

    return True 

# # MOVED 
# def get_yesterdays_round(): 
#     '''
#     '''
#     query = 'SELECT round_number FROM round_info ORDER BY round_number DESC LIMIT 1 '

#     yesterday_round = utils.read_from_sql(query)['round_number'][0]

#     return yesterday_round
    
if __name__ == '__main__': 
    current_round = utils.get_current_round()

    yesterday_round = read.read_last_round_number()

    if str(current_round) == str(yesterday_round): 

        print(datetime.now())

        print('--Still the same round as yesterday--')

        print('--No code called for today--', end = "\n\n")

    else:

        print(datetime.now())

        save_current_round(current_round)

        # create_crontab()

        print("--Round changed from {} to {}--".format(yesterday_round, current_round))

        main.main(current_round, yesterday_round)

        print("--main.main() Called--")

        print('--Current round saved--', end = "\n\n")

    