import os
import pusher
from time import sleep
import pysher
import logging
import sys
from dotenv import load_dotenv
import json
from playsound import playsound
from gtts import gTTS


def playVoice(text):
    tts = gTTS(text)
    tts.save('tmp.mp3')
    playsound('tmp.mp3')


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
    'Search Location',
    'question':
    'Where should we search?',
    'choices': [{
        'choice': 'The Table',
        'speech': 'Table chosen, find riddle under table and ponder for 20, then poll for meaning.',
        'index': 1,
        'votes': 0
    }, {
        'choice': 'The Cabinet',
        'speech': 'Cabinet chosen, find a discreet box then poll to open it?.',
        'index': 5,
        'votes': 0
    }]
}, {
    'name':
    'The Riddle\'s Message',
    'question':
    'Where is the riddle telling us to explore?',
    'choices': [{
        'choice': 'Front of the Room',
        'speech': 'Front chosen. Spend 30s being stupid and wasting time then poll whether to continue.',
        'index': 2,
        'votes': 0,
    }, {
        'choice': 'The Cabinet',
        'speech': 'Means to go to the cabinet chosen, find a discreet box then poll to open it?.',
        'index': 5,
        'votes': 0
    }]
}, {
    'name':
    'Descending into Madness',
    'question':
    'Should we keep searching here?',
    'choices': [{
        'choice': 'Yes',
        'speech': 'You are done. Mentally breakdown at the front of the room.',
        'index': 4,
        'votes': 0,
    }, {
        'choice': 'No',
        'speech': 'No, spend 10s wondering where  to search. Then go to a poll on where',
        'index': 3,
        'votes': 0,
    }]
}, {
    'name':
    'Where To Search',
    'question':
    'So where should we search?',
    'choices': [{
        'choice': 'The Painting',
        'speech': 'Take down the piano, try searchign it and then give up and mentally breakdown.',
        'index': 4,
        'votes': 0,
    }, {
        'choice': 'The Cabinet',
        'index': 5,
        'speech': 'Means to go to the cabinet chosen, find a discreet box then poll to open it?.',
        'votes': 0
    }]
}, {
    'name':
    'You Are Done',
    'question':
    'YOU ARE DONE',
    'choices': [{
        'choice': 'This means nothing',
        'index': 4,
        'votes': 0,
    }, {
        'choice': 'This also means nothing',
        'index': 4,
        'votes': 0,
    }]
}, {
    'name':
    'The Box in the Cabinet',
    'question':
    'Should we search the box?',
    'choices': [{
        'choice': 'Yes',
        'speech': 'Choose to search the box. Waste 30s looking for the “key”. Instructions on box.',
        'index': 6,
        'votes': 0,
    }, {
        'choice': 'No',
        'speech': 'Search around for a bit. Then search the book, shake it and a paper will fall out.',
        'index': 6,
        'votes': 0,
    }]
}, {
    'name':
    'The Skies or the floor',
    'question':
    'Should we search the ceiling or the floor?',
    'choices': [{
        'choice': 'The Ceiling',
        'speech': 'Find the piece of paper on the upper section of the wall.',
        'index': 7,
        'votes': 0,
    }, {
        'choice': 'The Floor',
        'speech': 'Search the floor, do nothing. Then the ceiling. Find the piece of paper on the upper section of the wall.',
        'index': 7,
        'votes': 0,
    }]
}, {'name':
    'You Might Win',
    'question':
    'You Might Win',
    'choices': [{
        'choice': 'This means nothing',
        'index': 7,
        'votes': 0,
    }, {
        'choice': 'This also means nothing',
        'index': 7,
        'votes': 0,
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


def voteReceived(data, *args, **kwargs):
    y = json.loads(data)
    print(y)
    theChoices[currentChoice]['choices'][int(y['choice'])]['votes'] += 1


def timeIsUp(data, *args, **kwargs):

    global currentChoice

    choosen = theChoices[currentChoice]['choices'][0]

    notChoosen = theChoices[currentChoice]['choices'][1]

    if theChoices[currentChoice]['choices'][0]['votes'] < theChoices[currentChoice]['choices'][1]['votes']:
        choosen = theChoices[currentChoice]['choices'][1]
        notChoosen = theChoices[currentChoice]['choices'][0]
    currentChoice = choosen['index']
    playVoice(choosen['speech'])
    pusher_client.trigger(
        u'drama', u'results', {
            'choosen': choosen,
            'notChoosen': notChoosen
        })


pusher = pysher.Pusher(os.getenv("PUSHER_KEY"), 'ap1')

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able


def connect_handler(data):
    channel = pusher.subscribe('drama')
    channel.bind('readyForChoice', readyForChoice)
    channel.bind('voteReceived', voteReceived)
    channel.bind('timeIsUp', timeIsUp)


pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

while True:
    sleep(1)
