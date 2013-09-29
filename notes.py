
def create_note_map():
    middle_a = 440
    note_ratio = 2 ** (float(1) / float(12))
    
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
    
    #compute the frequencies for each note
    note_map = {}
    for n in xrange(12*9):
        octave_num = n / 12
        note_num = n % 12
        
        for note_name in note_sequence[note_num]:
            #compute the frequency of this note relative to middle A (ie 440)
            note_map["%s-%d"%(note_name,octave_num)] = middle_a * (note_ratio ** (n - 57))
            
    return note_map 
