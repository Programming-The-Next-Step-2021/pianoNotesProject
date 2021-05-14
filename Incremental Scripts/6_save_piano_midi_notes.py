# Now that the basic feedback version is working it is time to repeat the steps for the actual 88 piano keys

# In comparison to the launchpad the midi output has changed
# the Input.read() function gives is this output
# [[status,data1,data2,data3],timestamp],...]

# If I run 1_connect_midi.py I see that I am interested in status and data1
# status == 144 we have a downpress
# status == 128 we have release
# data1 indicates the key

import pandas as pd



from pygame import midi

# initalise reading midi input

midi.init()


input = midi.Input(1)

key_id = list()
while True:
    # check whether input is detected
    if input.poll():
        # if input is detected print number of key that should be pressed
        print("Please press key number",len(key_id)+1)
        key = input.read(100)
        key = key[0][0]
        # we are interested in key_num for identification and sensitivity because latter changes depending if press/or release
        status,key_num = key[0],key[1]
        
        # since we only want downward press I use status == 144
        if status ==144:
            key_id.append(key_num)
        # if key_id list is full break loop
        if len(key_id) ==67:
            print("Thanks")
            break


data = {'key_number' :list(range(1,66)) }

key_bindings2 = pd.DataFrame(data)
key_bindings2 = pd.DataFrame(data)
key_bindings2.loc[:,"key_id"] = key_id

# safe as csv
key_bindings2.to_csv("key_bindings2.csv")