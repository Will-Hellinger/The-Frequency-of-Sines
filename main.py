import pyaudio
import numpy as np
import sys, csv, time
import urllib.request
import os
name = os.path.basename(__file__)

if os.name == 'nt':
    subDirectory = '\\'
    pip = 'pip'
    clear = 'cls'
else:
    subDirectory = '/'
    pip = 'pip3'
    clear = 'clear'

def clearConsole():
	os.system(clear)

def delayPrint(string):
	for a in string:
		sys.stdout.write(a)
		sys.stdout.flush()
		time.sleep(0.025)

p = pyaudio.PyAudio()
clearConsole()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 10.0  # in seconds, may be float
f = 256.0        # sine frequency, Hz, may be float

environments = {"water" : 1480,
                "air" : 345,
                "steel" : 5960,
                "rock" : 4470.4,
                "vacuum" : 0}

c = "water" # Current environment

mode = 'menu'
modes = ['menu', 'play_sound', 'song_player', 'environment_changer']

def menu():
    global c, mode, modes, environments

    delayPrint('The Frequency of Sines - A Physics Interpretation on Music\n\nBy Will Hellinger & John Bieberich:\n\n')
    try:
        delayPrint(f'1. Play a specific frequency\n2. Play a song(csv file)\n3. Change Medium - (Current Medium - {c})\n\n')
    except:
        delayPrint('1. Play a specific frequency\n2. Play a song(csv file)\n3. Change Medium - (Current Medium - unknown)\n\n')

    while True:
        delayPrint('Please select a choice: ')
        userInput = int(input(''))
        if userInput <= len(modes) - 1 and userInput >= 1:
            mode = modes[userInput]
            break
        else:
            delayPrint('Not a valid selection.\n')
    clearConsole()

def play_sound():
    global c, fs, volume, duration, environments, mode, modes

    delayPrint('Sound Player\n("back" to go back)\n')
    while True:
        try:
            stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs,output=True)

            delayPrint('frequency: ')
            userInput = input('')

            if userInput != 'back':
                f = float(int(userInput))
                samples = (np.cos(2*np.pi*np.arange(fs*(duration/(environments[c]/345)))*f/fs)).astype(np.float32)
                stream.write(volume*samples)

            stream.stop_stream()
            stream.close()

            if userInput == 'back':
                mode = 'menu'
                clearConsole()
                break
        except:
            delayPrint('please input a valid number\n')

def song_player():
    global fs, c, volume, environments, mode, modes

    while True:
        delayPrint('Song Player\n("back" to go back)\n')
        delayPrint('song: ')

        try:
            stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs,output=True)

            song = str(input(''))
            song = song.replace('.csv', '')

            if song == 'back':
                mode = 'menu'
                stream.stop_stream()
                stream.close()
                clearConsole()
                break

            rows = []

            if os.path.exists(f'.{subDirectory}{song}.csv'):
                with open(f'.{subDirectory}{song}.csv', 'r') as file:
                    csvreader = csv.reader(file)
                    header = next(csvreader)
                    for row in csvreader:
                        rows.append(row)
            
                try:
                    for s in range(len(rows)):
                        samples = (np.cos((2*np.pi*np.arange(fs*(float(rows[s][1])/(environments[c]/345)))*float(rows[s][0])/fs))).astype(np.float32)
                        stream.write(volume*samples)
                except:
                    continue
        except:
            delayPrint('please input a valid file\n')
        stream.stop_stream()
        stream.close()

def environment_changer():
    global c, environments, mode, modes

    try:
        delayPrint(f'Current Medium - {c}\n')
    except:
        delayPrint('Current Medium - unknown\n')
    
    delayPrint('Available Mediums: \n')

    for item in environments:
        delayPrint(f'{item}\n')
    
    while True:
        delayPrint('\nPlease enter a new medium ("back" to go back): ')
        userInput = str(input(''))

        if userInput == 'back':
            mode = 'menu'
            clearConsole()
            break
            
        if environments.get(userInput) != None:
            c = userInput
        else:
            delayPrint('please input a valid medium')

while True:
    if mode == 'menu':
        menu()
    elif mode == 'play_sound':
        play_sound()
    elif mode == 'song_player':
        song_player()
    elif mode == 'environment_changer':
        environment_changer()