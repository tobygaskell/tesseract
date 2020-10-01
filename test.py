class Players: 

    def __init__(self, name, choice, points_gained, overall_score): 
        self.name = name 
        self.choice = choice
        self.points_gained = points_gained
        self.overall_score = overall_score


class Rounds: 

    def __init__(self, number, fixtures):
        self.number = number 
        self.fixtures = fixtures 


class Fixtures:

    def __init__(self, score, result):
        self.score = score
        self.result = result 


def save_points(df):
    """
    This function is used to save the csv containing
    the points per round for each player. 

    PARAMETERS: 

    df (DataFrame): this is the DataFrame of points 
    you want to save

    RETURNS: 

    (string): a string indicating that the save has 
    worked.
    """
    df.to_csv(f'points/points_for_round_{number}.csv')
    return '-- Points Saved --'


def save_scores(df):
    """
    This function is used to save the csv containing
    the overall scores for each player. 

    PARAMETERS: 

    df (DataFrame): this is the DataFrame of scores 
    you want to save

    RETURNS: 

    (string): a string indicating that the save has 
    worked.
    """
    df.to_csv('overall_scores.csv')
    return '-- Scores Saved -- '

def read_choices():
    """
    This Function read 
    """
    with open('team_choices.txt', 'r') as file_: 
        choices = file_.readlines() 
    choices = {i.split('=')[0].strip() : i.split('=')[1].strip() for i in choices}
    return choices 


def initilize_scores(choices): 
    df = {k:0 for k in choices.keys()}
    scores = pd.DataFrame(df, index = ['Scores']).T
    scores.to_csv('overall_scores.csv')
    return '-- Scores Initialized --'

    





