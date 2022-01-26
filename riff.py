# This script randomly generates a riff.

# Eventually this will be part of a web app that will generate a riff with a 
# given parameter set (e.g., 2 bars in 12/8 time in F Dorian).

# libraries
import random

# functions
def flatten(t):
    return [item for sublist in t for item in sublist]

# next big step: determine the number of notes and the rhythm!
	# use the set of rhythyms from the Wooten camp: each one is worth one beat
	# in 4/4 (I think). Randomly pick them.
	# Rythyms are basically duple or triple. For now we're sticking to duple:

# for each beat we have to determine: 
	# how many notes will be in the beat (for 4/4 going down to 16ths it could be 0-4)
	# the placement of those notes (if it's one 8th note, where does the rest go?)

# I'm going to have to come up with my own shorthand for notes and rests at the sixteenth-note level
	# QQQQ = quarter note 
	# the beat could be a string of characters. Upper case are notes, lower case are rests, default is 16th.
	# one bar of three quarter notes, an eighth rest, then an 8th note: 'QQQQQQQQQQQQeeEE'
	# one bar of sixteen sixteenth notes: 'SSSSSSSSSSSSSSSS'

one_note_patterns = []

# That means I'll also have to write code to interpret those strings so I can put notes in there.






# parameters
number_notes = 8 # first random riff will be two measures of quarter notes

# Might be a better way to do this: for now it's just randomly determined for 
# each note and we can tweak the overall probability
rest_prob = 0.25  
accidental_prob = 0 # I'll incorporate this later

# Also should probably weight the 5th and octave more highly since I'm looking for basslines specifically.
# There's a better way to do this but I'm going to weight them manually for now:
	# 100 is the most likely a note could be to come up. I'm weighting the root and octave at 100.
	# 0 means it will never come up
note_weights = [100, 25, 25, 25, 75, 25, 25, 100]

note_list = []

# this is NOT the best way to do this
note_list.append([0]*note_weights[0])
note_list.append([1]*note_weights[1])
note_list.append([2]*note_weights[2])
note_list.append([3]*note_weights[3])
note_list.append([4]*note_weights[4])
note_list.append([5]*note_weights[5])
note_list.append([6]*note_weights[6])
note_list.append([7]*note_weights[7])

note_list = flatten(note_list)

# print(note_list)

# Add different keys (and modes) later. For now everything is in C. 
key = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']

# easy but inefficient: just loop through the number of notes.
# For my purposes I might not need to change this.
# I can't imagine it will ever loop more than a dozen times or so.
for i in range(0, 8):
	if random.uniform(0,1) < rest_prob:
		print("quarter rest")

	else:
		note_ind = random.randrange(0,len(note_list))
		note = note_list[note_ind] 
		print(key[note])

print("HELLO!!!")