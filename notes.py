
import re

note_regex = re.compile(r'(?P<note_name>[A-G][#b]?)(?P<octave_number>-?\d+)')

#each note goes by multiple names, this structure keeps track of the different names, in the correct order
note_aliases = [
    {'natural':'C', 'sharp':'B#'                },
    {               'sharp':'C#',   'flat':'Db' },
    {'natural':'D'                              },
    {               'sharp':'D#',   'flat':'Eb' },
    {'natural':'E',                 'flat':'Fb' },
    {'natural':'F', 'sharp':'E#'                },
    {               'sharp':'F#',   'flat':'Gb' },
    {'natural':'G'                              },
    {               'sharp':'G#',   'flat':'Ab' },
    {'natural':'A'                              },
    {               'sharp':'A#',   'flat':'Bb' },
    {'natural':'B',                 'flat':'Cb' },
    ]

note_index_map = {}
for i, name_dict in enumerate(note_aliases):
    for note_name in name_dict.itervalues():
        note_index_map[note_name] = i
        
        
def create_note_map():
    middle_a = 440
    note_ratio = 2 ** (float(1) / float(12))
    
    #compute the frequencies for each note
    note_map = {}
    for n in xrange(-11,12*9):
        octave_num = n / 12
        note_num = n % 12
        
        for note_name in note_aliases[note_num].itervalues():
            
            formatted_note = format_note(note_name,octave_num)
            
            #compute the frequency of this note relative to middle A (ie 440)
            note_map[formatted_note] = middle_a * (note_ratio ** (n - 57))
            
    return note_map


def flat(note_name):
    new_alias, new_octave = _make_flat(*_parse_note(note_name))
    return format_note(new_alias,new_octave)
    
    
def sharp(note_name):
    new_alias, new_octave = _make_sharp(*_parse_note(note_name))
    return format_note(new_alias,new_octave)


def natural(note_name):
    note_index, note_alias, octave_num = _parse_note(note_name)
    
    if('#' in note_alias):
        new_alias, new_octave = _make_flat(note_index, note_alias, octave_num)
    elif('b' in note_alias):
        new_alias, new_octave = _make_sharp(note_index, note_alias, octave_num)
    else:
        new_alias, new_octave = note_alias, octave_num
        
    return format_note(new_alias,new_octave)
    
    
def format_note(note_alias, octave_num):
    return "%s%d"%(note_alias,octave_num)



#takes in a note with an octave, and returns the note's alias index, its alias, and its octave number
def _parse_note(note_name):
    match = note_regex.match(note_name)
    if(match is None):
        raise ValueError("Invalid note name")
    
    note_alias = match.group('note_name')
    octave_num = int(match.group('octave_number'))
    
    return note_index_map[note_alias], note_alias, octave_num



def _make_flat(note_index, note_alias, octave_num):
    new_note_index = note_index - 1
    new_octave_num = octave_num
        
    #check if we've dropped into the next octave
    if(new_note_index < 0):
        new_note_index += 12
        new_octave_num -= 1
    
    #i'm not fancy enough for double flats and shit like that, so here are the rules:
    
    #if it's a sharp, just go one semitone down and use the natural alias
    #if it's natural or flat, then go one semitone down, and if that note has a 'flat' alias, use it, otherwise just use the natural alias
    if(note_alias.endswith('#')):
        new_note_alias = note_aliases[new_note_index]['natural']
    else:
        if('flat' in note_aliases[new_note_index]):
            new_note_alias = note_aliases[new_note_index]['flat']
        else:
            new_note_alias = note_aliases[new_note_index]['natural']
            
    return new_note_alias, new_octave_num



def _make_sharp(note_index, note_alias, octave_num):
    new_note_index = note_index + 1
    new_octave_num = octave_num
        
    #check if we've risen into the next octave
    if(new_note_index >= 12):
        new_note_index -= 12
        new_octave_num += 1
    
    #i'm not fancy enough for double sharps and shit like that, so here are the rules:
    
    #if it's a flat, just go one semitone down and use the natural alias
    #if it's natural or sharp, then go one semitone down, and if that note has a 'sharp' alias, use it, otherwise just use the natural alias
    if(note_alias.endswith('b')):
        new_note_alias = note_aliases[new_note_index]['natural']
    else:
        if('sharp' in note_aliases[new_note_index]):
            new_note_alias = note_aliases[new_note_index]['sharp']
        else:
            new_note_alias = note_aliases[new_note_index]['natural']
            
    return new_note_alias, new_octave_num



