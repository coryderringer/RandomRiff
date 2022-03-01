# Cory Derringer
# 2/1/22
# This script randomly generates a riff in abc notation using a given key and mode.

# Eventually this will be part of a web app that will generate a riff with a 
# given parameter set (e.g., 2 bars in 12/8 time in F Dorian).

# First version generates one bar of 4/4 with a given key and mode.

# libraries
import random, argparse

# argument parsing
parser = argparse.ArgumentParser(description = "Generate a random riff using a given key/scale")

parser.add_argument("key", 
	help = "Desired key, capital letter currently required, sharp/flat = s/b. E.g., A, ^A, _B...",
	choices = ['C', 'G', 'D', 'A', 'E', 'B', '^F', '_D', '_A', '_E', '_B', 'F'])
parser.add_argument("--time", help = "Time signature of desired riff. Currently script only supports 4/4.", choices = ["4/4"])
parser.add_argument("--mode", 
	help = "Desired mode of the output riff. Default is Ionian. (Minor is Aeolian.)", 
	default = "Ionian",
	choices = ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", 
	"Locrean"])
parser.add_argument("--numericMode", 
	help = "Desired mode of the output riff, numeric input (e.g., 1 is Ionian, 2 is Dorian, etc).",
	type = int,
	choices = range(1,8))
parser.add_argument("--numberMeasures",
	help = "Number of measures of music to generate",
	type = int,
	default = 1)

args = parser.parse_args()

# helper functions
def flatten(t):
    return [item for sublist in t for item in sublist]

# important global variables/lists
modes = ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrean"]
key_list = [['C', 'D', 'E', 'F', 'G', 'A', 'B'],
					['G', 'A', 'B', 'C', 'D', 'E', '^F'],
					['D', 'E', '^F', 'G', 'A', 'B', '^C'],
					['A', 'B', '^C', 'D', 'E', '^F', '^G'],
					['E', '^F', '^G', 'A', 'B', '^C', '^D'],
					['B', '^C', '^D', 'E', '^F', '^G', '^A'],
					['^F', '^G', '^A', 'B', '^C', '^D', '^E',],
					['_D', '_E', 'F', '_G', '_A', '_B', 'C',],
					['_A', '_B', 'C', '_D', '_E', 'F', 'G',],
					['_E', 'F', 'G', '_A', '_B', 'C', 'D',],
					['_B', 'C', 'D', '_E', 'F', 'G', 'A',],
					['F', 'G', 'A', '_B', 'C', 'D', 'E']]
L = 1/8 # standard note length is the 8th note


# Same-note bias: if we have two 1s in a row, it should be more likely that they're the same note.
# Call it 60/40 for now, eventually we'll want to put this in the optional arguments.
same_note_bias = .6


# Generate rhythm: which 8th-note "slots" will have notes in them?
	# each measure is 4 beats (man this really restricts us to 4/4)
	# each beat is 2 8th-note slots

# TODO: figure out a way to get these probs into the arguments
beat_note_probs = [.8, .6, .7, .6] # prob of note (vs rest) in quarter slots
subdivision_probs = [.75, .5] # prob of a note for each 16th

# main functions
def get_beats(): 

	beats = []
	for i in range(0, len(beat_note_probs)):
		# beats.append([0,0])
		beats.append([0]*len(subdivision_probs))

		if random.uniform(0,1) <= beat_note_probs[i]: # there is at least one note in this beat

			for j in range(0, len(beats[i])):
				if random.uniform(0,1) <= subdivision_probs[j]:
					beats[i][j] = 1

	beats = flatten(beats)

	return beats

def convert_beats_to_string(beats): # function isn't really named properly, and maybe should just be a part of beats
	for i in range(0, len(beats)):
		if(i < 7 and beats[i] == 1):
			a = 0

			while a == 0:
				if random.uniform(0,1) <= .75: # hardcoded .75, not sure what to call this, prob of extending note?
					# print("slot " + str(i) + " extended!")
					beats[i+1] = 2 # 2 means it's the same note as before, so we only need pitches for the ones
				else:
					a = 1

	# convert to a string (maybe we should switch so that it GENERATES as a string)
	# beats_string = [str(x) for x in beats]
	# beats_string = ''.join(beats_string)
	# print(f"beats string: {beats_string}")
	return beats


def get_notes_in_key(mode): # plug in args.mode when you call the function
	# generate notes:
	mode_position = modes.index(mode)

	# notes to choose from:
	for i in key_list:
		try:
			if i.index(args.key) == mode_position:
				ionian_key = i[0]
				double_list = i + i
				notes_in_key = double_list[mode_position:mode_position+8]
				# print(f"Pulling notes from the key of {ionian_key}: {double_list[0:8]}")
				break
		except ValueError: 
			# if the note we're looking for isn't in the key, move on to the next one
			pass 

	return [ionian_key, notes_in_key]

def measure(beats, notes_in_key): # call with 1st position of output of notes_in_key function

	# Also should probably weight the 5th and octave more highly since I'm looking 
		# for basslines specifically.
	# There's a better way to do this but I'm going to weight them manually for now:
		# 100 is the most likely a note could be to come up. I'm weighting the root 
			# and octave at 100.
		# 0 means it will never come up
	note_weights = [100, 25, 25, 25, 75, 25, 25, 100]
	note_list = []

	for i in note_weights:
		for j in range(0, i):
			note_list.append(note_weights.index(i)+1)

	# iterate through beats to generate notes. For each beat:
		# if 0, z (rest)
		# if 1, generate note
		# if 2, modify previous note to be longer

	notes = []
	for i in range(0, len(beats)):
		if beats[i] == 1:
			
			if (len(notes) > 0) & (beats[i-1] == 1) & (random.uniform(0,1) <= same_note_bias):
				pass # note stays the same as it was
			else:
				note = note_list[random.randrange(0, len(note_list))]
		
			notes.append(notes_in_key[note-1])
		elif beats[i] == 2:
			# get appended number on the end of the prev note. Multiply it by 2.
			# list
			try:
				list_note = list(notes[len(notes)-1]) 
				# print(f"list note: {list_note}")
				n = 2*int(list_note[len(list_note)])
				list_note[len(list_note)] = n
				notes[len(notes)] = ''.join(list_note)
			
			except IndexError:
				n = notes[len(notes)-1]+'2'
				notes[len(notes)-1] = n
		else:
			notes.append('z')
	
	return ''.join(notes)

def measure_loop(numberMeasures, notes_in_key): # feed in 1st position of output from get_notes_in_key()
	abc_string = '|'
	for i in range(0, numberMeasures):
		beats = get_beats()
		beats_string = convert_beats_to_string(beats)
		abc_string = abc_string + measure(beats_string, notes_in_key) + '|'

	return abc_string

def abc_notation(ionian_key, notes): # call with 0th position of notes_in_key output, as well as output of measure

	# convert to abc:
	# we want this eventually to be a text file that we can export. 

	# metadata at the top of the abc file
	tune = 'X:1'
	title = 'T:Your Randomly Generated Riff'
	composer = 'C:RandomRiff'
	length = 'L:1/8'
	time_sig = 'M:4/4' # for now it's all 4/4
	key_sig = 'K:' + ionian_key

	return [tune, title, composer, length, time_sig, key_sig, notes]

def export_file(abc): # output of abc_notation

	# export file:
	with open('exported_abc.txt', 'w') as f:
		f.write('\n'.join(abc))


# main block:
beats = get_beats()
beats_string = convert_beats_to_string(beats)
notes_in_key = get_notes_in_key(args.mode)
# m = measure(beats_string, notes_in_key[1])
m = measure_loop(args.numberMeasures, notes_in_key[1])
abc = abc_notation(notes_in_key[0], m)
export_file(abc)

# show output in console
print('\n'.join(abc))

# next steps: 
	# find a way to get this into notation 
		# 1. Embed this script in an index file, send the riff script to the front end to get picked up by abcjs.
			# (This will require something like a google or aws webapp)
		# 2. Write the html/js for the front end
			# Features:
			# Generate a new riff
			# Copy abc for the current riff to the clipboard
			# Send midi
			# Send image of sheet music
	# midi!


# notes:

# 2/3 looks like Bb doesn't work in the key signature later on, am I exporting it wrong?
