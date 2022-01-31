# This script randomly generates a riff.

# Eventually this will be part of a web app that will generate a riff with a 
# given parameter set (e.g., 2 bars in 12/8 time in F Dorian).

# libraries
import random, argparse

# argument parsing
parser = argparse.ArgumentParser(description = "Generate a random riff using a given key/scale")
# parser.parse_args()


parser.add_argument("key", 
	help = "Desired key, capital letter currently required, sharp/flat = s/b. E.g., A, As, Bb...",
	choices = ['C', 'G', 'D', 'A', 'E', 'B', 'Fs', 'Db', 'Ab', 'Eb', 'Bb', 'F'])
parser.add_argument("--time", help = "Time signature of desired riff. Currently script only supports 4/4.", choices = ["4/4"])
parser.add_argument("--mode", 
	help = "Desired mode of the output riff. Default is Ionian.", 
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

#
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
key_list = [['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'],
					['G', 'A', 'B', 'C', 'D', 'E', 'Fs', 'G'],
					['D', 'E', 'Fs', 'G', 'A', 'B', 'Cs', 'D'],
					['A', 'B', 'Cs', 'D', 'E', 'Fs', 'Gs', 'A'],
					['E', 'Fs', 'Gs', 'A', 'B', 'Cs', 'Ds', 'E'],
					['B', 'Cs', 'Ds', 'E', 'Fs', 'Gs', 'As', 'B'],
					['Fs', 'Gs', 'As', 'B', 'Cs', 'Ds', 'Es', 'Fs'],
					['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C', 'Db'],
					['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G', 'Ab'],
					['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D', 'Eb'],
					['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A', 'Bb'],
					['F', 'G', 'A', 'Bb', 'C', 'D', 'E', 'F']]


start_note = range(0, 7) # modes without naming (i.e., if I wanted the scale to start on the second note)
modes = ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrean"]

possible_keys = ['C', 'G', 'D', 'A', 'E', 'B', 'Fs', 'Db', 'Ab', 'Eb', 'Bb', 'F']
key_number = possible_keys.index(args.key)
notes_in_key = key_list[key_number]

starting_position = modes.index(args.mode)

# Also should probably weight the 5th and octave more highly since I'm looking 
	# for basslines specifically.
# There's a better way to do this but I'm going to weight them manually for now:
	# 100 is the most likely a note could be to come up. I'm weighting the root 
		# and octave at 100.
	# 0 means it will never come up
note_weights = [100, 25, 25, 25, 75, 25, 25, 100]

note_list = []

# this is NOT the best way to do this
note_list.append([1]*note_weights[0])
note_list.append([2]*note_weights[1])
note_list.append([3]*note_weights[2])
note_list.append([4]*note_weights[3])
note_list.append([5]*note_weights[4])
note_list.append([6]*note_weights[5])
note_list.append([7]*note_weights[6])
note_list.append([8]*note_weights[7])

note_list = flatten(note_list)

notes = ['r'] * len(beats)


# thanks stack overflow https://stackoverflow.com/questions/6294179/how-to-find-all-occurrences-of-an-element-in-a-list
indices = [i for i, x in enumerate(beats) if x == 1]

for i in range(0, len(indices)):
	note = note_list[random.randrange(0,len(note_list))]
	notes[indices[i]] = notes_in_key[note-1]

# number of notes that continue from a previous 16th slot
continuation_notes = [i for i, x in enumerate(beats) if x == 2]
for i in continuation_notes:
	notes[i] = notes[i-1].lower() # continued notes are lower case





# next steps: 
	# allow for multiple keys (done, but still need to incorporate modes)
	# find a way to get this into notation
	# midi!


print(f"Generating riff in {args.key} ({args.mode})")
print(f"Notes in key of {args.key}: {notes_in_key[0:7]}")
print(f"Starting position: {starting_position}")
print(f"Beats: {beats}")
print(f"Notes: {notes}")

