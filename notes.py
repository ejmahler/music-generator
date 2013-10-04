#create the 'generic' names for each note. each note goes by multiple names, this structure keeps track of the different names
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

def get_key(note_name, key_type):
    
    #set up the major key indexes
    note_index_map = {'major':{}}
    
    for i, name_list in note_sequence:
        for note_name in name_list:
            note_index_map['major'][note_name] = i
            
    #set up the minor key indexes. c is 0 for major and a is 0 for minor, so add 3 semitones to every major index
    note_index_map['minor'] = {name:index + 3 for name, index in note_index_map['major'].iteritems()}
    
    #first we need to find the index of this note
    note_index = note_index_map[key_type][note_name]
    
    #find this key's position on the circle of fifths
    #keys progress up and down from C using a circle of fifths. so the "base" key is at C, 
    #then we go up one perfect fifth to G, thne up one perfect fifth to D. this is equivalent to solving 
    #"note_index congruent to perfect_fith_interval * wheel_position (mod 12)" for wheel_position
    
    #the solution to that formula is simply "note_index * perfect_fifth_interval (mod 12)"
    wheel_position = (note_index * 7) % 12
    
    #for the keys that involve flat notes, we will represent this with negative numbers
    if(wheel_position >= 8):
        wheel_position -= 12
    
    #the keys with index 5 6 and 7 can be both flat or sharp - only make it flay if the key name has "flat" in it
    elif(wheel_position >= 5 and 'flat' in note_name):
        wheel_position -= 12
        
    #wheel_position now contains an integer from -7 to +7 representing its position on the wheel of fifths
    
    
    
