# This file creates csv with the files and the input for 76 piano notes

import os
import pandas as pd
piano_notes = os.listdir("./piano_package/Notes_piano/")
piano_df = pd.DataFrame({"note_files" : piano_notes})
piano_df["key_id"] = piano_df.note_files.str[:2]

piano_df.key_id = pd.to_numeric(piano_df.key_id)

piano_df.key_id = piano_df.key_id + 20

piano_df.to_csv("./piano_package/piano_config_67k.csv")