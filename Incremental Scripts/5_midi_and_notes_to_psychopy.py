# This script will port the previous script number 4 into psychopy.
# psychopy functions
from psychopy.gui import DlgFromDict
from psychopy.visual import Window, TextStim, ImageStim
from psychopy.core import wait, Clock, quit
from psychopy.hardware.keyboard import Keyboard
from pandas import read_csv

# midi functions
from pygame import midi


# exp_info = {'participant_nr': ''}  # no default!
# dlg = DlgFromDict(exp_info)

win = Window(fullscr=True, size=(2560, 1440))
win.units = "pix"

# initialise clock, key and midi input from psychopy and pygame input

clock = Clock()

kb = Keyboard()

welcome_txt_stim = TextStim(
    win,
    text="""Welcome to this experiment!
 You will be presented with piano notes and have to press the corresponding key on the piano. 
 Afterwards you will receive feedback
 (Press enter to start)""",
)

welcome_txt_stim.draw()

win.flip()

while True:
    keys = kb.getKeys()
    if "return" in keys:
        break


# Now I will create two dataframes: The first one 'key_bindings' has the note files and the corresponding key_id that we implemented earlier
# The second "condition_df" dataframe will include the order in which the notes will be shown (random for now) and store the reaction time

key_bindings = read_csv("./key_bindings.csv", index_col=0)


# condition_df = key_bindings.sample(frac=1)
condition_df = key_bindings
midi.init()

input = midi.Input(1)

trial_clock = Clock()
for idx, row in condition_df.iterrows():
    current_note = row["note_files"]
    current_id = row["key_id"]

    stim_img = ImageStim(win, "./Notes/" + current_note)

    stim_right = TextStim(win, text="right")
    stim_wrong = TextStim(win, text="wrong")

    condition_df.loc[idx, "response"] = "n/a"
    condition_df.loc[idx, "reaction_time"] = "n/a"

    stim_img.draw()
    time_start = midi.time()
    win.flip()
    while True:
        if input.poll():
            midi_key = input.read(100)[0]
            key_id, key_sensitivity, time = midi_key[0][1], midi_key[0][2], midi_key[1]
            if key_id == current_id and key_sensitivity != 0:
                condition_df.loc[idx, "reaction_time"] = time - time_start
                stim_right.draw()
                win.flip()
                wait(1)
                condition_df.loc[idx, "response"] = "right"
                break
            elif key_id != current_id and key_sensitivity != 0:
                condition_df.loc[idx, "reaction_time"] = time_start - time
                stim_wrong.draw()
                win.flip()
                wait(1)
                condition_df.loc[idx, "response"] = "wrong"
                break

condition_df.to_csv("results.csv")


# Finish experiment
win.close()
quit()
