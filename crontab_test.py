import utils 
from datetime import datetime
import test as main 
import pandas as pd 

def save_current_round(round_number):
    '''
    '''
    DW = main.DP_round()
    
    DP = main.draw_weekend(round_number)

    data = pd.DataFrame({"round_number": [round_number], 'draw_weekend': [DW], "double_points_weekend": [DP]})

    utils.input_into_sql(data, 'round_info', 'append')

    return True 


def get_yesterdays_round(): 
    '''
    '''
    query = 'SELECT round_number FROM round_info order by round_number desc limit 1 '

    yesterday_round = utils.read_from_sql(query)['round_number'][0]

    return yesterday_round
    

current_round = utils.get_current_round()

yesterday_round = get_yesterdays_round()

if str(current_round) == str(yesterday_round): 

    print(datetime.now())

    print('--Still the same round as yesterday--')

    print('--No code called for today--', end = "\n\n")

else:

    print(datetime.now())

    save_current_round(current_round)

    print("--Round changed from {} to {}--".format(yesterday_round, current_round))

    main.main(current_round, yesterday_round)

    print("--main.main() Called--")

    print('--Current round saved--', end = "\n\n")

    