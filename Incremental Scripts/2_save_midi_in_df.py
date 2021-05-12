# Here we will save the key to a dataframe and save  in a csv
# The goal is to have a list of all 88 keys so we can save the corresponding picture note and sound file names in the csv as well
# Before using the whole piano I will work with the launchpad which also has a Midi input
# I will use a single row with 8 keys for this so we can use keys C4-C5

import pandas as pd
# Just the range for the total number of keys
# somewhat redundant as we technically have the natural index but nice because it defines the length of the df
data = {'key_number' :list(range(1,9)) }


key_bindings = pd.DataFrame(data)

from pygame import midi

# initalise reading midi input

midi.init()


input = midi.Input(1)
# if we press a key on the midi input it will receive a certain number corresponding to it's key -> will be denotes key_id
# since this differs depending on input device/number of keys one wants to enable, user is asked to press certain key number until
# range above is filled
# for actual piano we will have to deal with sensitivity/strength of press but here it is just a single number != 0

# TO DO
# fix it in such a way that request to press key only appears on downward press and not release
# -> due to the fact that pressing and releasing a key appear as different input, while we only want the press

key_id = list()
while True:
    # check whether input is detected
    if input.poll():
        # if input is detected print number of key that should be pressed
        print("Please press key number",len(key_id)+1)
        key = input.read(100)
        key = key[0][0]
        # we are interested in key_num for identification and sensitivity because latter changes depending if press/or release
        key_num, sensitivity = key[1],key[2]
        input.read()
        # since we only want downward press
        if sensitivity !=0:
            key_id.append(key_num)
        # if key_id list is full break loop
        if len(key_id) ==len(key_bindings):
            print("Thanks")
            break


# attach the midi id to df from before
key_bindings.loc[:,"key_id"] = key_id

# safe as csv
key_bindings.to_csv("key_bindings.csv")


