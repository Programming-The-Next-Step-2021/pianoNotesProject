import sys
import os
from PySide6.QtCore import (
    QObject,
    QSize,
    Qt,
    QThread,
    QRunnable,
    Slot,
    QThreadPool,
    Signal,
)
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QBoxLayout,
    QGridLayout,
    QLineEdit,
    QWidget,
)
import pandas as pd
from pygame import midi

from qt_material import apply_stylesheet


class WorkerSignal(QObject):
    """
    Function to get output for midi signal
    """

    result = Signal(tuple)


class Worker(QRunnable):
    """ Class that allows for listening to MIDI input without freezing the GUI

    PySide/PyQT detects input by having a main loop that 'listens' to
    widgets such as buttons. If a long or infinite task is started 
    this main loop freezes as it waits for completion. But in order 
    to detect the midi keys a loop that monitors the midi input is
    needed which would freeze the program/main loop.
    
    Thus this class creates a worker which starts a parallel thread
    that signals the main loop every time a midi key is pressed. 
    
    """

    def __init__(self):
        super(Worker, self).__init__()

        # here we give our worker the ability to send signals back to the frontend GUI
        self.signal = WorkerSignal()

    @Slot()  # QtCore.Slot
    def run(self):
        midi.init()
        self.input = midi.Input(1)
        while True:

            if self.input.poll():

                midi_key = self.input.read(100)
                midi_key = midi_key[0][0]
                status, key_id = midi_key[0], midi_key[1]
                # a status of 144 signals a downpress of a key
                if status == 144:
                    print(midi_key)
                    self.signal.result.emit((key_id))


class MainWindow(QMainWindow):
    """Main class that defines the main loop of the GUI
    
    This class defines the layout of all buttons and inputs as well as how
    the program responds to input. 

    """

    def __init__(self):
        super().__init__()
        # Title for program

        self.setWindowTitle("My App")

        # this dropdown box is used whether one wants to test the whole setup
        self.options_menu = QComboBox()
        self.options_menu.addItems(["midi input", "keyboard"])
        # The start_button launches the reading of the data and adds notes
        self.start_button = QPushButton(text="Start?")
        self.start_button.clicked.connect(self.read_data_and_order)

        # keyboard
        self.keyboard_input = QLineEdit()

        self.keyboard_input.setMaxLength(10)
        self.keyboard_input.setPlaceholderText("Enter the note here")

        # Feedback widget

        self.feedback_widget = QLabel("Have fun practicing!!")
        self.feedback_widget.setAlignment(Qt.AlignCenter)
        # start ability to have multiple threads

        self.threadpool = QThreadPool()

        # create widget that shows the notes
        self.note_widget = QLabel()

        self.note_widget.setAlignment(Qt.AlignCenter)

        layout = QGridLayout()
        layout.addWidget(self.options_menu, 0, 0)
        layout.addWidget(self.start_button, 0, 1)
        layout.addWidget(self.note_widget, 1, 0, 3, 2)
        layout.addWidget(self.feedback_widget, 5, 0, 1, 2)
        layout.addWidget(self.keyboard_input, 6, 0, 1, 2)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.setFixedSize(QSize(500, 650))

    def read_data_and_order(self):
        """This function reads the csv file that contains all of the piano
        names, file names of pictures as well the corresponding midi key id.
        
        The file names and key id are then used to check whether the input is
        correct.
        """
        # read corresponding keys
        self.data = pd.read_csv("./piano_package/piano_config_67k.csv", index_col=0)

        # all keys to be played are stored in self objects and will then accessed via an integer that
        # changes after a note was pressed correctly/wrongly

        self.keys = self.data.key_id
        self.notes = self.data.note_files
        self.note_names = self.data.note_names
        # only clickable once after all
        self.start_button.setEnabled(False)
        self.i = 0
        # start with first picture

        self.note_widget.setPixmap(
            QPixmap("./piano_package/Notes_piano/" + self.notes[0])
        )

        # only start worker loop when no keyboard but midi input is used
        if self.options_menu.currentText() == "keyboard":
            self.keyboard_input.returnPressed.connect(self.test_input)
        else:
            self.keyboard_input.setEnabled(False)
            worker = Worker()
            self.threadpool.start(worker)
            # this takes the output/signal of the worker
            worker.signal.result.connect(self.test_input)

    def test_input(self, input_key=None):
        """Checks whether keyboard/midi input matches displayed note.

        This function checks whether the input from the midi piano or 
        the text input for the note name match the displayed note and provides
        feedback. After that it displayes the next note.
        Args:
            input_key ([str], optional): The midi id of the pressed button. Defaults to None.
        """

        # if a midi keyboard is not available a text box is used tp type in the key name
        if input_key == None:
            input_key = self.keyboard_input.text()

        #
        if input_key == self.keys[self.i] or input_key == self.note_names[self.i]:

            self.feedback_widget.setText(f"RIGHT \n {self.note_names[self.i]}")
            # quickly communicate with main loop so that picture is changed before function ends
            QApplication.processEvents()
            QThread.sleep(1)
            self.feedback_widget.clear()
            res =1
        elif input_key != self.keys[self.i] or input_key != self.note_names[self.i]:
            self.feedback_widget.setText(f"WRONG \n {self.note_names[self.i]}")
            QApplication.processEvents()
            QThread.sleep(1)
            self.feedback_widget.clear()
            res =0

        # reset text input
        self.keyboard_input.clear()

        # increases integer index so next note strored in self.notes can be displayed
        self.i = self.i + 1

        self.note_widget.setPixmap(
            QPixmap("./piano_package/Notes_piano/" + self.notes[self.i])
        )
        return(res)

