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

args = parser.parse_args()

# functions
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
L = 1/8 # standard note length is the 16th note

# Generate rhythm:
# each measure is 4 beats (man this really restricts us to 4/4)
# each beat is 4 16th-note slots

# TODO: figure out a way to get these probs into the arguments
beat_note_probs = [.75, .25, .5, .25] # prob of note (vs rest) in quarter slots
sixteenth_probs = [.8, .1, .4, .2] # prob of a note for each 16th

beats = []
for i in range(0, 4):
	beats.append([0,0])

	for j in range(0, len(beats[i])):
		if random.uniform(0,1) <= sixteenth_probs[j]:
			beats[i][j] = 1

beats = flatten(beats)


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
beats_string = [str(x) for x in beats]
beats_string = ''.join(beats_string)
print(f"beats string: {beats_string}")


# generate notes:
mode_position = modes.index(args.mode)

# notes to choose from:
for i in key_list:
	try:
		if i.index(args.key) == mode_position:
			ionian_key = i[0]
			double_list = i + i
			notes_in_key = double_list[mode_position:mode_position+8]
			print(f"Pulling notes from the key of {ionian_key}: {double_list[0:8]}")
			break
	except ValueError: 
		# if the note we're looking for isn't in the key, move on to the next one
		pass 

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

notes = ['z'] * len(beats)


# approach 1: get all beats with notes ahead of time, determine notes, place them.
# thanks stack overflow https://stackoverflow.com/questions/6294179/how-to-find-all-occurrences-of-an-element-in-a-list
# indices of all occurrences of 1 in the beats list:
indices = [i for i, x in enumerate(beats) if x == 1]

for i in range(0, len(indices)):	
	note = note_list[random.randrange(0,len(note_list))]
	notes[indices[i]] = notes_in_key[note-1]

# notes that continue from a previous 16th slot
continuation_notes = [i for i, x in enumerate(beats) if x == 2]
for i in continuation_notes:
	notes[i] = notes[i-1].lower() # continued notes are lower case


# approach 2: iterate through beats:
	# if 0, z
	# if 1, generate note
	# if 2, modify previous note to be longer

notes = []
# YOU ARE HERE 2/2/22
for i in range(0, len(beats)):
	if beats[i] == 1:
		note = note_list[random.randrange(0, len(note_list))]
		notes.append(notes_in_key[note-1])
	elif beats[i] == 2:
		# get appended number on the end of the prev note. Multiply it by 2.
		# list
		try:
			list_note = list(notes[len(notes)-1]) 
			print(f"list note: {list_note}")
			n = 2*int(list_note[len(list_note)])
			list_note[len(list_note)] = n
			notes[len(notes)] = ''.join(list_note)
		
		except IndexError:
			n = notes[len(notes)-1]+'2'
			notes[len(notes)-1] = n
	else:
		notes.append('z')



# convert to abc:
# we want this eventually to be a text file that we can export. 

# metadata at the top of the abc file
tune = 'X:1'
title = 'T:Your Randomly Generated Riff'
composer = 'C:RandomRiff'
length = 'L:1/8'
time_sig = 'M:4/4' # for now it's all 4/4
key_sig = 'K:' + ionian_key
notes = '|'+''.join(notes)+'|'


# export file:
abc_txt = [tune, title, composer, length, time_sig, key_sig, notes]
with open('exported_abc.txt', 'w') as f:
	f.write('\n'.join(abc_txt))





# next steps: 
	# find a way to get this into notation 
		# Oh this is cool as hell: https://www.abcjs.net/
		# 1. Change RandomRiff to use abc notation because it's great
		# 2. Embed this script in an index file, send the riff script to the front end to get picked up by abcjs.
		# 3. Write the html/js for the front end
			# Features:
			# Generate a new riff
			# Copy abc for the current riff to the clipboard
			# Send midi
			# Send image of sheet music
	# midi!

# print(f"Notes in {args.key} {args.mode}: {notes_in_key}")
# print(f"Starting position: {mode_position+1}")
# print(f"Generating riff in {args.key} {args.mode}")
# print(f"Beats: {beats}")
# print(f"Notes: {notes}")

print('\n'.join(abc_txt))

# notes:

# 2/3 looks like Bb doesn't work in the key signature later on, am I exporting it wrong?
# Next step is to get it working on github pages! Added html to a folder called html, but it's not working yet
