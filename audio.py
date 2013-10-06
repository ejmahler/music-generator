import math
import pprint

import matplotlib.pyplot as plt
import numpy
from scipy.io.wavfile import write

import keys
import notes
from notes import natural, sharp, flat

note_map = notes.create_note_map()

sample_freq = 44100
note_duration = 0.5
note_spacing = 0.3

note_linspace = numpy.linspace(0, 1, sample_freq * note_duration)

@numpy.vectorize
def note_fade_function(t):
    return ((1 - t) ** 3) * t

note_fade_vector = note_fade_function(numpy.linspace(0, 1, sample_freq * note_duration))


def write_music(note_list):
    #create the array that will hold all of the audio data from start to end
    audio_data = numpy.zeros(sample_freq * (note_spacing * (len(note_list) - 1) + note_duration))
    
    for i, note in enumerate(note_list):
        
        #create the function which will convert the time input into a value at that time, based on the frequency for this note
        note_freq = note_map[note] * 2 * math.pi
        reference_freq = note_map['C#4'] * 2 * math.pi
        
        @numpy.vectorize
        def sample_function(t):
            
            #notes with a higher frequency should have a smaller amplitude
            amplitude = math.log(reference_freq / note_freq + 1)
            
            
            #i got this by playing around with it - we play the main note, then a weak version of the same note an octave down
            return amplitude * (math.sin(note_freq * t) + 0.1 * math.sin(note_freq * 0.5 * t) + 0.01 * math.sin(note_freq * 0.25 * t))
        
        #apply the sample function to the linear space. this will give a sampled sine wave
        note_data = sample_function(numpy.linspace(0, note_duration, sample_freq * note_duration)) * note_fade_vector
        
        #add this note data to the audio data
        note_begin = note_spacing * sample_freq * i
        audio_data[note_begin:note_begin + len(note_data)] += note_data
        
    scaled = numpy.int16(audio_data/numpy.max(numpy.abs(audio_data)) * 32767)
    write('test.wav', sample_freq, scaled)
    
    
def create_note_fade():
    pass
