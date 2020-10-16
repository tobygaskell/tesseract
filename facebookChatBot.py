from fbchat import Client
import utils


def login_to_facebook(username, password): 
    client = CustomClient(username, password)
    return client 


class CustomClient(Client):

    def onMessage(self, message_object, author_id, thread_id, thread_type, **kwargs):
        print('in onMessage')
        relevent = check_message(thread_id)
        if relevent ==  True: 
            do_stuff(message_object, author_id, thread_id, thread_type) 
        else: 
            pass

def check_message(thread_id): 
    if thread_id == '3365583033489198': 
        relevent_message = True
    else: 
        relevent_message = False 
    return relevent_message

def do_stuff(msg_obj, author_id, thread_id, thread_type):
    name = find_author_name(author_id)
    message_type = evaluate_message(msg_obj.text)
    if message_type == 'Team Submission': 
        pass
        #input_team(name, msg.obj.text)
    respond(msg_obj.text, name, message_type, thread_id, thread_type)



def find_author_name(author_id): 
    user = client.fetchUserInfo(author_id)[author_id]
    return user.name

def evaluate_message(text):
    print(text.lower())
    if text.startswith('Team ='): 
        message_type = 'Team Submission'
    elif text.lower() == 'help': 
        message_type = 'Help Request'
    elif text.lower() == 'standings':
        message_type = 'Standing Request'
    elif text.lower() == 'winning': 
        message_type = 'Winning Request'
    elif text.lower() == 'loosing': 
        message_type = 'Loosing Request'
    elif text.lower() == 'choices':
        message_type = 'Choices Request'
    elif text.lower() == 'fixtures': 
        message_type = 'Fixture Request'
    else: 
        message_type = 'Undefined'
    return message_type

def respond(text, name, message_type, thread_id, thread_type): 
    if message_type == "Help Request": 
        text = help_request_text(name)
        send_message(text, thread_id, thread_type, client)
        
    elif message_type == 'Team Submission': 
        text = team_submission_text(name, text)
        send_message(text, thread_id, thread_type, client)

def team_submission_text(name, text): 
    return '''Hi {}, you have submitted {} as your team for this week!

If this is incorrect please redo your submission before the cutoff'''.format(name, text.split('=')[1])

def help_request_text(name): 
    return f''' Hi {name} Here is the Help for the facebook chat bot...

## Commands: 

- 'help' - This will print the help document.
- 'winning' - This will give you the name of the player currently at the top of the leaderboard.
- 'loosing' - This will give you the name of the player currently at the bottom of the leaderboard.
- 'standings' - This will give you the position of each of the players.
- 'position' - This will give you your current position in the leaderboard.
- 'choices' - This will give you your eligable choices for the upcomming round.
- 'fixtures' - This will give you the upcoming fixtures for that round

## Inputs

- 'Team = <team_name>' - This will input your team choice for the upcoming week.

## Rules of the chat 

- Please try to use the chat one at a time 
- Please don't spam the chat 
- Please when giving team choices don't use abriviations
                '''


def send_message(text, thread_id, thread_type, client): 
    client.sendMessage(text, thread_id, thread_type)
    return '--Message Sent--'



if __name__ == "__main__": 
    client = CustomClient('toby96@sky.com', '2002Fish')
    client.listen()

