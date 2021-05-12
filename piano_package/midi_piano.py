import pandas as pd
from psychopy.gui import DlgFromDict
from psychopy.visual import Window, TextStim, ImageStim
from psychopy.core import wait, Clock, quit
from psychopy.hardware.keyboard import Keyboard

# midi functions
from pygame import midi


class midi_piano:
    '''
    This class defines the properties of the midi piano and inicates the location of the note pictures (and maybe sound files).
    This is important as different midi pianos have different key_ids and inidcations of whether a button is pressed.

    Parameters
    ----------
    input_id : int
        The port in which the MIDI devive is plugged in.
    key_total: int
        The total number of keys. Default of 88 for normal piano
    key_num: list  
        A list containing the range of every key. 
    note_files: list
        List containig the path to the corresponding note picture
    key_id: list
        Contains the corresponding output id for the midi device

    --- Not in use yet ---
    mp3_files: list
        List containing the path to corresponding mp3 tone
    model_recall: list
        A list containing tulips with the alpha, beta and half-life for Bayesian scheduling (see https://github.com/fasiha/ebisu)
    last_recall:
        A list containing the last recall.

    '''
    def __init__(self):
        self.input_id = None
        self.key_total = 8
        self.key_num = list(range(self.key_total))
        self.note_files = None
        self.key_id = None
        self.note_order = None
    
    def setup_midi(self,device = 'launchpad',key_total = None ,note_files = None):
        '''
        This function allows to choose from predefined midi setups or to use own setup and needs to be run first
        '''
        # Prompts user to select preconfigured MIDI device or define own properties
        if(device == 'launchpad'):
            df = pd.read_csv("piano_package/launchpad_config.csv",index_col=0)
            # wd needs to be on pianoNoteProject for it to work
            self.input_id = 1
            self.note_files = df.note_files
            self.key_id = df.key_id


    def create_order_df(self,random= False):
        '''
        This function takes the self as input and creates a dataframe that will determine the order of the displayed notes in test_run
        '''
        data = {"key_num": self.key_num,
                "key_id": self.key_id,
                "note_files": self.note_files}

        note_order = pd.DataFrame(data)
        if random:
            note_order = note_order.sample(frac=1)
        self.note_order = note_order



    def test_run(self,random =False):
        '''
        This function launches the graphical interface via psychopy which will present the user with words and gives simple feedback
        '''
        win = Window(fullscr=True,size= (2560,1440))
        win.units = 'pix'

        # initialise clock, key and midi input from psychopy and pygame input 
        clock = Clock()
        kb = Keyboard()
        welcome_txt_stim = TextStim(win,
         text="""Welcome to this experiment!
         You will be presented with piano notes and have to press the corresponding key on the piano. 
         Afterwards you will receive feedback
         (Press enter to start)"""
        )
        welcome_txt_stim.draw()

        win.flip()

        while True:
            keys = kb.getKeys() 
            if "return" in keys:
                break
        
        self.create_order_df(random)
        midi.init()

        input = midi.Input(1)

        trial_clock = Clock()


        for idx,row in self.note_order.iterrows():
            current_note = row['note_files']
            current_id = row['key_id']

            stim_img = ImageStim(win, "piano_package/Notes/" + current_note)

            stim_right = TextStim(win,text='right')
            stim_wrong= TextStim(win,text='wrong')

            #note_order.loc[idx, "response"] = "n/a"
            #note_order.loc[idx, "reaction_time"] = "n/a"

            
            stim_img.draw()
            time_start = midi.time()
            win.flip()
            while True:
                if input.poll():
                    midi_key = input.read(100)[0]
                    key_id, key_sensitivity,time = midi_key[0][1], midi_key[0][2],midi_key[1]
                    if key_id == current_id and key_sensitivity !=0:
                        #condition_df.loc[idx, "reaction_time"] =  time - time_start
                        stim_right.draw()
                        win.flip()
                        wait(1)
                        #condition_df.loc[idx, "response"] = "right"
                        break
                    elif key_id != current_id and key_sensitivity !=0:
                        #condition_df.loc[idx, "reaction_time"] = time_start - time
                        stim_wrong.draw()
                        win.flip()
                        wait(1)
                        #condition_df.loc[idx, "response"] = "wrong"
                        break
        win.close()
        quit()  
        
                    
