# This file is basically just a clone of midi_piano but instead of a class it uses functions to increase readability.
import pandas as pd

from psychopy.gui import DlgFromDict
from psychopy.visual import Window, TextStim, ImageStim
from psychopy.core import wait, Clock, quit
from psychopy.hardware.keyboard import Keyboard

# midi functions
from pygame import midi


def setup_midi(input_id=1, device=None):
    """[summary]

    Args:
        input_id (int, optional): [description]. Defaults to 1.
        device ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """

    if device == None:
        print(
            """Please select your device number: \n
        1: Launchpad
        2: Piano (67 keys)
        3: keyboard (doesn't work yet)
        """
        )
        while True:
            try:
                num = int(input())
                if num == 1 or num == 2:  # not 3 since this function not included yet
                    break
            except:
                print("That is not an option")

    if device == "piano1" or num == 2:
        config_file_df = pd.read_csv("piano_package/piano_config_67k.csv", index_col=0)
        path = "piano_package/Notes_piano/"

    elif device == "lauchpad" or num == 1:
        config_file_df = pd.read_csv("piano_package/launchpad_config.csv", index_col=0)
        path = "/piano_package/Notes/"
    return (device, config_file_df, path)


def test_run(device=None):

    """
    This function can be used for testing purposes to display a couple of notes and give feedback
    Mostly just to test functionality - and not to train.
    """
    device, config_file_df, path = setup_midi(device=device)

    win = Window(fullscr=True, size=(2560, 1440), monitor="my")
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

    # condition_df = key_bindings.sample(frac=1).head(10)
    condition_df = config_file_df.head(10)
    midi.init()

    input = midi.Input(1)

    trial_clock = Clock()
    for idx, row in condition_df.iterrows():
        current_note = row["note_files"]
        current_id = row["key_id"]

        stim_img = ImageStim(win, path + current_note)

        stim_right = TextStim(win, text="right")
        stim_wrong = TextStim(win, text="wrong")

        # condition_df.loc[idx, "response"] = "n/a"
        # condition_df.loc[idx, "reaction_time"] = "n/a"

        stim_img.draw()
        time_start = midi.time()
        win.flip()
        while True:
            if input.poll():
                key = input.read(100)
                key = key[0][0]

                # we are interested in key_num for identification and sensitivity because latter changes depending if press/or release
                if device == "piano1":
                    status, key_id = key[0], key[1]

                if key_id == current_id and status == 144:
                    # condition_df.loc[idx, "reaction_time"] =  time - time_start
                    stim_right.draw()
                    win.flip()
                    wait(1)
                    # condition_df.loc[idx, "response"] = "right"
                    break
                elif key_id != current_id and status == 144:
                    # condition_df.loc[idx, "reaction_time"] = time_start - time
                    stim_wrong.draw()
                    win.flip()
                    wait(1)
                    # condition_df.loc[idx, "response"] = "wrong"
                    break

    # Finish experiment
    win.close()
    quit()
