
# Import pygame midi module
from pygame import midi

# initalise reading midi input

midi.init()

# give list of all MIDI devices
for i in range(midi.get_count()):
    r = midi.get_device_info(i)
    print(i,r)

# select appropriate midi device
input = midi.Input(1)

# loop that prints out the input of a key if it is pressed


while True:
    if input.poll():

        key = input.read(100)
        #key = key[0][0]
        
        print(key)
        #key_num, sensitivity = key[1],key[2]
        #print(key_num,sensitivity)



#while True:
#    if input.poll():
#        time = input.read(100)[0][1]
#        print(time)
#        
#        #print(key)
#        #key_num, sensitivity = key[1],key[2]
#        #print(key_num,sensitivity)


midi.quit()

