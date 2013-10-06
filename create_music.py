
import keys
import audio
import notes


def fibonacci_mod_iter(num, modulus):
    
    prev2 = 0
    prev1 = 1
    current = (prev1 + prev2)%modulus
    
    if(num >= 1):
        yield prev2%modulus
    if(num >= 2):
        yield prev1%modulus
        
    for i in xrange(2, num):
        yield current
        
        prev1 = prev2
        prev2 = current
        current = (prev1 + prev2)%modulus


if(__name__ == '__main__'):
    '''
    key = keys.get_key('C#','minor')
    
    part1 = [
        key[7 * 4 + 4], key[7 * 5 + 0], key[7 * 5 + 2],
        key[7 * 4 + 4], key[7 * 5 + 0], key[7 * 5 + 2],
        key[7 * 4 + 4], key[7 * 5 + 0], key[7 * 5 + 2],
        key[7 * 4 + 4], key[7 * 5 + 0], key[7 * 5 + 2],
        
        key[7 * 4 + 5], key[7 * 5 + 0], key[7 * 5 + 2],
        key[7 * 4 + 5], key[7 * 5 + 0], key[7 * 5 + 2],
        
        key[7 * 4 + 5], natural(key[7 * 5 + 1]), key[7 * 5 + 3],
        key[7 * 4 + 5], natural(key[7 * 5 + 1]), key[7 * 5 + 3],
        
        key[7 * 4 + 4], sharp(key[7 * 4 + 6]), key[7 * 5 + 3],
        key[7 * 4 + 4], key[7 * 5 + 0], key[7 * 5 + 2],
        key[7 * 4 + 4], key[7 * 5 + 0], key[7 * 5 + 1],
        key[7 * 4 + 3], sharp(key[7 * 4 + 6]), key[7 * 5 + 1],
        ]
    
    write_music(part1)
    '''
    key = keys.get_key('C','major')
    
    notes = list(fibonacci_mod_iter(100, 25))[5:]
    audio.write_music([key[20 + n] for n in notes])
    
    
    
 
