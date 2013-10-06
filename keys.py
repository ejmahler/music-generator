
import notes 





def get_key(key_name, key_type):
    
    #first we need to find the index of this note
    base_note_index = notes.note_index_map[key_name]
    
    #find the position on the wheel of fifths, relative to c major/a minor
    wheel_position = get_wheel_position(base_note_index, key_name, key_type)
    
    #find the set of notes that get sharpened or flattened
    modified_notes = get_modified_notes(wheel_position)
    
    #find the ordered list of notes in this key, starting with the base note for the key
    key_notes = get_key_notes(base_note_index, key_type)
    
    #all we have are indexes, and only for a single octave - compute note names for all the octaves
    return get_full_note_list(key_notes, modified_notes, wheel_position)






    

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
    
    #the keys with index 5 6 and 7 can be both flat or sharp - only make it flat if the key name has the flat symbol in it
    elif(wheel_position >= 5 and key_name.endswith('b')):
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
        
    
    #key_notes now contains something similar to [8, 10, 11, 1, 3, 4, 6]. we want to convert this to [-4, -2, -1, 1, 3, 4, 6]
    #we do this by subtracting 12 from each element until we find one that is smaller than the previous
    previous = -13
    for i in xrange(len(key_notes)):
        modified = key_notes[i] - 12
        if(modified < previous):
            break
        previous = key_notes[i] = modified
    
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

    
def get_full_note_list(key_notes, modified_notes, wheel_position):
    
    if(wheel_position < 0):
        target_alias = "flat"
    else:
        target_alias = "sharp"
    
    #loop through octaves 0 to 9 and build the full list of notes, including their names and octaves
    #for c major, all the note indexes will be negative, meaning octave 9 won't be represented at all
    #but in general we're creating 9 full octaves
    note_name_list = []
    for octave_num in xrange(0, 10):
        
        for note_num in key_notes:
            
            #if the note number is negative we actually want to put this note in the previous octave
            if(note_num < 0):
                current_octave = octave_num - 1
            else:
                current_octave = octave_num
                
            current_note_index = note_num % 12
            
            #find out the name for this note
            
            #if this note was modified, we want to use its "special" name like a-sharp or w/e
            if(current_note_index in modified_notes):
                note_name = notes.note_aliases[current_note_index][target_alias]
            else:
                note_name = notes.note_aliases[current_note_index]["natural"]
                
            #we have the note name and octave name! add this note to the note_name_list
            note_name_list.append('%s%d'%(note_name, current_octave))
            
    return note_name_list
