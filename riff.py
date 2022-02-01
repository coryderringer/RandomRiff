# Cory Derringer
# 2/1/22
# This script randomly generates a riff using a given key and mode.

# Eventually this will be part of a web app that will generate a riff with a 
# given parameter set (e.g., 2 bars in 12/8 time in F Dorian).

# First version generates one bar of 4/4 with a given key and mode.

# libraries
import random, argparse

# argument parsing
parser = argparse.ArgumentParser(description = "Generate a random riff using a given key/scale")

parser.add_argument("key", 
	help = "Desired key, capital letter currently required, sharp/flat = s/b. E.g., A, As, Bb...",
	choices = ['C', 'G', 'D', 'A', 'E', 'B', 'Fs', 'Db', 'Ab', 'Eb', 'Bb', 'F'])
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
					['G', 'A', 'B', 'C', 'D', 'E', 'Fs'],
					['D', 'E', 'Fs', 'G', 'A', 'B', 'Cs'],
					['A', 'B', 'Cs', 'D', 'E', 'Fs', 'Gs'],
					['E', 'Fs', 'Gs', 'A', 'B', 'Cs', 'Ds'],
					['B', 'Cs', 'Ds', 'E', 'Fs', 'Gs', 'As'],
					['Fs', 'Gs', 'As', 'B', 'Cs', 'Ds', 'Es',],
					['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C',],
					['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G',],
					['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D',],
					['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A',],
					['F', 'G', 'A', 'Bb', 'C', 'D', 'E']]


# Generate rhythm:
# each measure is 4 beats (man this really restricts us to 4/4)
# each beat is 4 16th-note slots

# TODO: figure out a way to get these probs into the arguments
beat_note_probs = [.75, .25, .5, .25] # prob of note (vs rest) in quarter slots
sixteenth_probs = [.8, .1, .4, .2] # prob of a note for each 16th

beats = []
for i in range(0, 4):
	beats.append([0,0,0,0])

	for j in range(0, len(beats[i])):
		if random.uniform(0,1) <= sixteenth_probs[j]:
			beats[i][j] = 1
 
beats = flatten(beats)

for i in range(0, len(beats)):
	if(i < 15 and beats[i] == 1):
		a = 0

		while a == 0:
			if random.uniform(0,1) <= .75: # hardcoded .75, not sure what to call this, prob of extending note?
				# print("slot " + str(i) + " extended!")
				beats[i+1] = 2 # 2 means it's the same note as before, so we only need pitches for the ones
			else:
				a = 1

# generate notes:
mode_position = modes.index(args.mode)

for i in key_list:
	try:
		if i.index(args.key) == mode_position:
			double_list = i + i
			notes_in_key = double_list[mode_position:mode_position+8]
			print(f"Pulling notes from the key of {i[0]}: {double_list[0:8]}")
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

notes = ['r'] * len(beats)

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


# next steps: 
	# find a way to get this into notation (https://abjad.github.io/)
	# midi!

print(f"Notes in {args.key} {args.mode}: {notes_in_key}")
print(f"Starting position: {mode_position+1}")
print(f"Generating riff in {args.key} {args.mode}")
print(f"Beats: {beats}")
print(f"Notes: {notes}")