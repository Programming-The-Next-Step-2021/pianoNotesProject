# This script will take the csv we produced last time and show a picture when a key is pressed down

from PIL import Image
#import os
#import pathlib
#os.chdir(os.path.dirname(__file__))


import pandas as pd
key_bindings = pd.read_csv("./key_bindings.csv",index_col=0)
print(key_bindings)



from pygame import midi

midi.init()

input = midi.Input(1)

while True:
    if input.poll():
        midi_key = input.read(100)[0][0]
        key_id, key_sensitivity = midi_key[1], midi_key[2]

        if key_sensitivity != 0:
            print(key_id)
            
            
            path = key_bindings.loc[key_bindings.loc[:,"key_id"] == key_id,"note_files"].item()
            print(type(path))
            img = Image.open("./Notes/" + path)
            img.show()


