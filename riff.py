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
	# how many notes will be in the beat (for 4/4 going down to 16ths it could 
		# be 0-4)



# Eventually this will take a "time" argument but assuming 4/4 for now
# Time should be in the following format: "4/4", "3/4", etc.
def get_notes():   
	# beat_value = time.split('/')[1] 

	# Just to get it working I think we need to assume 4/4. This will be 
	# adjusted later
	slots = 16 # there is probably a better descriptive term for this

	# method 1:
			# number_notes = 0

			# for i in range(0, slots):
			# 	if random.uniform(0,1) > rest_prob:
			# 		number_notes += 1

	# method 2: gamma distribution (requires numpy, pita to set up but possible)
	# random.gamma(2, 1, None)

	# method 3: beat orientation
		# Assuming 4/4, we can say that there are 4 quarter notes and assign 
		# probabilities that there will be a note on that downbeat.
		# We can also assign probabilities to pickup notes (maybe like a 
		# busy-ness scale, where busier = more pickup notes) and whether those 
		# pickup notes will be 8th or 16th notes.

	beat_notes = [0,0,0,0] # notes on the beat, default as 4 rests
	beat_note_probs = [.75, .25, .5, .25]

	note_values = [0,0,0,0]
	
	a = [4]*50 # 4th
	b = [8]*100 # 8th
	c = [16]*25 # 16th

	value_weights = a + b + c
	
	for i in range(0, len(beat_notes)):
		
		if random.uniform(0,1) <= beat_note_probs[i]:
			beat_notes[i] = 1
			note_values[i] = value_weights[random.randrange(0, len(value_weights))]
		else:
			pass


	# pickup_probs = 
	# trailer_probs =
	# pitches = # once we have all notes in a measure we can assign pitches
		# Pitch idea: if we generate them randomly independent of each other it 
		# could sound jumpy. That's sometimes good but sometimes we might want a 
		# more melodic line, so we could put in a parameter to weight closer 
		# notes more heavily in that case.

	return beat_notes, note_values

notes = get_notes()

beat_notes = notes[0]
note_lengths = notes[1]

print("Beat Notes: " + str(beat_notes))
print("Note Lengths: " + str(note_lengths))


# we need to determine notes in the measure before notes in the beat, will make
# it a lot easier; could avoid thinking about beats for the most part (aside 
# from weighting the downbeat more heavily in a later version).

def measure(number_notes, note_lengths):

	pass



	# how long will each note last (if we want one note in a 4/4 beat, is it a 
		# 1/4 note, 1/8 note and 1/8 rest, etc)
	# the placement of those notes (if it's one 8th note, where does the rest 
		# go?)

# I'm going to have to come up with my own shorthand for notes and rests at the 
	# One option: sixteenth-note level
	
	# QQQQ = quarter note 
	# the beat could be a string of characters. Upper case are notes, lower 
		# case are rests, default is 16th.
	# one bar of three quarter notes, an eighth rest, then an 8th note: 
		# 'QQQQQQQQQQQQeeEE'
	# one bar of sixteen sixteenth notes: 'SSSSSSSSSSSSSSSS'

one_note_patterns = [

	'QQQQ',
	'EEee',
	'eeEE',
	'Ssee',
	'sSee',
	'eeSs',
	'eesS',
	'sEEE', # dotted eighth note
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',



	'qqqq'


]

# That means I'll also have to write code to interpret those strings so I can 
	# put notes in there.






# parameters
# number_notes = 8 # first random riff will be two measures of quarter notes

# Might be a better way to do this: for now it's just randomly determined for 
# each note and we can tweak the overall probability. Could also sample number 
# of notes in a measure from a distribution with a given mean and sd (e.g., 3, 
# 0.5).

# Weird concept: this is currently the probability that another note won't be 
# added to the measure, or that the next slot won't contain a note.
rest_prob = 0.75 
accidental_prob = 0 # I'll incorporate this later


# number_notes = get_number_notes()
# print(str(number_notes) + ' notes in this measure')


# Also should probably weight the 5th and octave more highly since I'm looking 
	# for basslines specifically.
# There's a better way to do this but I'm going to weight them manually for now:
	# 100 is the most likely a note could be to come up. I'm weighting the root 
		# and octave at 100.
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
		# print("quarter rest")
		pass

	else:
		note_ind = random.randrange(0,len(note_list))
		note = note_list[note_ind] 
		# print(key[note])
		pass

# print("HELLO!!!")