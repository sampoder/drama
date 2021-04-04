import os
import pusher
from time import sleep
import pysher
import logging
import sys
from dotenv import load_dotenv
import json

load_dotenv()

root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

pusherPysher = pysher.Pusher("92c64299da2189a14546")

pusher.app_id = "1182764"
pusher.key = os.getenv("PUSHER_KEY")
pusher_client = pusher.Pusher("1182764",
                              os.getenv("PUSHER_KEY"),
                              os.getenv("PUSHER_SECRET"), cluster='ap1')

print('We await for the first choice.')

currentChoice = 0

theChoices = [{
    'name':
    'The Cereal',
    'question':
    'What cereal should Sam eat?',
    'choices': [{
        'choice': 'KoKoKrunch',
        'index': 1,
        'votes': 0
    }, {
        'choice': 'Cornflakes',
        'index': 1,
        'votes': 0
    }]
}, {
    'name':
    'The Candy',
    'question':
    'What candy should Sam eat?',
    'choices': [{
        'choice': 'Skittles',
        'index': 1,
        'votes': 0
    }, {
        'choice': 'Cornflakes',
        'index': 1,
        'votes': 0
    }]
}]


def readyForChoice(data, *args, **kwargs):
    print('New Choice')
    print('We are currently at X, we can either go to Y or Z')

    # sending that we have a choice to the window and the options to the users

    pusher_client.trigger(
        u'drama', u'newChoice', {
            u'choices': [
                theChoices[currentChoice]['choices'][0],
                theChoices[currentChoice]['choices'][1]
            ],
            u'question':
            theChoices[currentChoice]['question']
        })


def voteRecieved(data, *args, **kwargs):
    y = json.loads(data)
    print(y)
    theChoices[currentChoice]['choices'][y['choice']]['votes'] += 1


def timeIsUp(data, *args, **kwargs):

    global currentChoice

    choosen = theChoices[currentChoice]['choices'][0]

    if theChoices[currentChoice]['choices'][0]['votes'] < theChoices[currentChoice]['choices'][1]['votes']:
        choosen = theChoices[currentChoice]['choices'][1]
    print(choosen)
    currentChoice = choosen['index']
    print('Tallying up the responses')
    print('The Winner is: !')
    print('Sending the winner to the window!')


pusher = pysher.Pusher(os.getenv("PUSHER_KEY"), 'ap1')

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able


def connect_handler(data):
    channel = pusher.subscribe('drama')
    channel.bind('readyForChoice', readyForChoice)
    channel.bind('voteRecieved', voteRecieved)
    channel.bind('timeIsUp', timeIsUp)

pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

while True:
    # Do other things in the meantime here...
    sleep(1)
