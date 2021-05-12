# As a next step I will introduce the images for the notes
# For this I have the folder "Notes" with the C4-C5 note pictures in the correct order
# for piano this needs to be expanded for all 88 keys and notes

# the goal is do add the filenames to the key_bindings.csv file to the corresponding key 
# so that each midi key corresponds to a certain image and note


# let's first read dataframe we just made in last script
import os
import pathlib
os.chdir(os.path.dirname(__file__))




import pandas as pd
key_bindings = pd.read_csv('./key_bindings.csv')

import os
# let's read a list of the the filenames in the Notes folder




note_files = os.listdir('./Notes/')

#print(note_files)
key_bindings.loc[:,"note_files"] = note_files

print(key_bindings)





path = key_bindings.loc[0,"note_files"]

from PIL import Image

img = Image.open("./Notes/" + path)

img.show()


key_bindings= key_bindings.loc[:,["key_number","key_id","note_files"]]
key_bindings.to_csv("key_bindings.csv")