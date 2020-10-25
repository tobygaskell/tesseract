import utils 
from datetime import date

print('running the job')


def save_current_round(current_round):
    round_txt =  open('round.txt', 'w') 
    round_txt.write(current_round)
    round_txt.close()
    return('--round number saved--')


def get_yesterdays_round(): 
    round_txt = open('round.txt', 'r')
    yesterday_round = round_txt.read()
    return yesterday_round


current_round = utils.get_current_round()
yesterday_round = get_yesterdays_round()

if current_round == yesterday_round: 

    print(date.today())
    print('--Still the same round as yesterday--')

else:

    save_current_round(current_round)
    print(date.today())
    print("--Round Changed from {} to {}--".format(yesterday_round, current_round))
