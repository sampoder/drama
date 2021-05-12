from playsound import playsound
import os
import pusher
from time import sleep
import pysher
import logging
import sys
import rtmidi
from dotenv import load_dotenv

load_dotenv()

root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

print(os.getenv("PUSHER_KEY"))

pusher = pysher.Pusher(os.getenv("PUSHER_KEY"), 'ap1')

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able
def playTheSounds(data, *args, **kwargs):
  print(data)
  if data.sound == "padlock":
    playsound('/Users/sam/Documents/GitHub/drama/mouth/padlock.flac')
  if data.sound == "siren":
    playsound('/Users/sam/Documents/GitHub/drama/mouth/siren.flac')
  if data.sound == "pressure":
    note_off = [0x90, 100, 100]
    midiout.send_message(note_off)
  if data.sound == "quote":
    note_off = [0x90, 0, 0]
    midiout.send_message(note_off)
    playsound('/Users/sam/Documents/GitHub/drama/mouth/quote.mp3')
  if data.sound == "drop":
    note_off = [0x90, 0, 0]
    midiout.send_message(note_off)
    playsound('/Users/sam/Documents/GitHub/drama/mouth/siren.flac')
    sleep(1)
    note_off = [0x90, 100, 0]
    midiout.send_message(note_off)
  if data.sound == "rattle":
    playsound('/Users/sam/Documents/GitHub/drama/mouth/rattle.mp3')

def connect_handler(data):
    channel = pusher.subscribe('drama')
    channel.bind('playTheSounds', playTheSounds)

pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

while True:
    sleep(1)