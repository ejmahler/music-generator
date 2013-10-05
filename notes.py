#each note goes by multiple names, this structure keeps track of the different names, in the correct order
note_sequence = [
    ('c',       'c-natural', 'b-sharp'),
    ('c-sharp', 'd-flat'),
    ('d',       'd-natural'),
    ('d-sharp', 'e-flat'),
    ('e',       'e-natural','f-flat'),
    ('f',       'f-natural','e-sharp'),
    ('f-sharp', 'g-flat'),
    ('g',       'g-natural'),
    ('g-sharp', 'a-flat'),
    ('a',       'a-natural'),
    ('a-sharp', 'b-flat'),
    ('b',       'b-natural', 'c-flat'),
    ]

def create_note_map():
    middle_a = 440
    note_ratio = 2 ** (float(1) / float(12))
    
    #compute the frequencies for each note
    note_map = {}
    for n in xrange(12*9):
        octave_num = n / 12
        note_num = n % 12
        
        for note_name in note_sequence[note_num]:
            #compute the frequency of this note relative to middle A (ie 440)
            note_map["%s-%d"%(note_name,octave_num)] = middle_a * (note_ratio ** (n - 57))
            
    return note_map 

def get_key(key_name, key_type):
    
    #set up the major key indexes
    note_index_map = {}
    
    for i, name_list in enumerate(note_sequence):
        for note_name in name_list:
            note_index_map[note_name] = i
    
    #first we need to find the index of this note
    note_index = note_index_map[key_name]
    
    wheel_position = get_wheel_position(note_index, key_name, key_type)
    
    modified_notes = get_modified_notes(wheel_position)
    
    key_notes = get_key_notes(note_index, key_type)
    
    
    #key_notes now contains the indexes of the notes that will be used in this key, with the base note at key_notes[0]
    return key_notes

def get_wheel_position(note_index, key_name, key_type):
    
    #the key index is different from the base note index if we're in a minor key
    if(key_type == 'minor'):
        key_index = (note_index + 3)%12
    else:
        key_index = note_index
        
    
     #find this key's position on the circle of fifths
    #keys progress up and down from C using a circle of fifths. so the "base" key is at C, 
    #then we go up one perfect fifth to G, thne up one perfect fifth to D. this is equivalent to solving 
    #"key_index congruent to perfect_fith_interval * wheel_position (mod 12)" for wheel_position
    
    #the solution to that formula is simply "key_index * perfect_fifth_interval (mod 12)"
    wheel_position = (key_index * 7) % 12
    
    #for the keys that involve flat notes, we will represent this with negative numbers
    if(wheel_position >= 8):
        wheel_position -= 12
    
    #the keys with index 5 6 and 7 can be both flat or sharp - only make it flay if the key name has "flat" in it
    elif(wheel_position >= 5 and 'flat' in key_name):
        wheel_position -= 12
        
    return wheel_position
        
def get_key_notes(note_index, key_type):
    #set up the initial note configuration assuming a key of c major or a minor
    if(key_type == 'major'):
        key_notes = [
            note_index, #c
            (note_index + 2)%12,#d
            (note_index + 4)%12,#e
            (note_index + 5)%12,#f
            (note_index + 7)%12,#g
            (note_index + 9)%12,#a
            (note_index + 11)%12,#b
        ]
    elif(key_type == 'minor'):
        key_notes = [
            note_index, #a
            (note_index + 2)%12,#b
            (note_index + 3)%12,#c
            (note_index + 5)%12,#d
            (note_index + 7)%12,#e
            (note_index + 8)%12,#f
            (note_index + 10)%12,#g
        ]
    return key_notes

def get_modified_notes(wheel_position):
    #if the wheel position is positive we will be raising notes by one half tone, 
    #and if its negative we'll be decreasting notes by one half tone
    if(wheel_position > 0):
        tone_modifier = 1
    elif(wheel_position < 0):
        tone_modifier = -1
    else:
        tone_modifier = 0
        
    #loop from 1 to wheel_position, inclusive
    modified_notes = set()
    for i in xrange(1, abs(wheel_position) + 1):
        current_note = (7 * i * tone_modifier) % 12
        
        #if this is a sharp key, go 2 semitones back from current_key, and increase that by one semitone
        if(tone_modifier > 0):
            modified_note = (current_note - 2 + tone_modifier) % 12
        
        #if this is a sharp key, go 6 semitones back from current_key, and increase that by one semitone
        elif(tone_modifier < 0):
            modified_note = (current_note - 6 + tone_modifier) % 12
            
        modified_notes.add(modified_note)
        
    return modified_notes
        
        
