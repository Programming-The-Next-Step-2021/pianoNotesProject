# pianoNotesProject

This project is aimed at teaching people how to read the notes of all 88 piano keys. As learning how to see and play piano notes is one of the first steps in becoming a good piano player, this program will hopefully facilitate this.
One will be presented with a picture of a note and then has to press the corresponding key on they keyboard or - if time allows for an implementation - the key on a digital piano that is connected via MIDI. Then the tone will be played and one will receive feedback of whether it was the correct key or not.

# Structure

This page is set up in such a way that the main magic happens inside the piano_package which can be imported as a python package (See 'Test.py')


The Incremental Scripts folder on the other hand provides insight into the process that went into the creation of the package as each script builds upon the last and introduces a new function. This functionality is then ported into the python package. 