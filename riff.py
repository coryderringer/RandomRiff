# This script randomly generates a riff.

# Eventually this will be part of a web app that will generate a riff with a 
# given parameter set (e.g., 2 bars in 12/8 time in F Dorian).

# libraries
import random 


# functions
def flatten(t):
    return [item for sublist in t for item in sublist]

# each measure is 4 beats (man this really restricts us to 4/4)
# each beat is 4 16th-note slots

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
key = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']

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

notes = [0] * len(beats)


# thanks stack overflow https://stackoverflow.com/questions/6294179/how-to-find-all-occurrences-of-an-element-in-a-list
indices = [i for i, x in enumerate(beats) if x == 1]

for i in range(0, len(indices)):
	note = note_list[random.randrange(0,len(note_list))]
	notes[indices[i]] = note

# number of notes that continue from a previous 16th slot
continuation_notes = [i for i, x in enumerate(beats) if x == 2]
for i in continuation_notes:
	notes[i] = notes[i-1]
	

print(beats)
print(notes)

