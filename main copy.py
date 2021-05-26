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
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
import pandas as pd
from pygame import midi

from qt_material import apply_stylesheet


class WorkerSignal(QObject):
    """[summary]

    Args:
        QObject ([type]): [description]
    """

    result = Signal(tuple)


class Worker(QRunnable):
    """
    This worker is necessary to enable the continous reading of the midi input

    This is due to the fact that the GUI normally runs a loop that reacts to user input (e.g. buttons)
    But if we start a while loop to catch the MIDI input it blocks and freezes the main loop of the gui
    -> thus manipulating the note pictures and giving feedback becomes inpossible
    So this function creates a worker that we will pass as another thread to monitors the midi loop and gives and indication of which key is pressed
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
                # midi_key = self.input.read(100)[0]
                midi_key = self.input.read(100)
                midi_key = midi_key[0][0]
                # key_id, status = midi_key[0][1], midi_key[0][2]
                status, key_id = midi_key[0], midi_key[1]
                # if status != 0:
                if status == 144:
                    print(midi_key)
                    self.signal.result.emit((key_id))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Title for program

        self.setWindowTitle("My App")

        # Let's load necessary dataframe for launchpad

        # this dropdown box is used whether one wants to test the whole setup

        # The start_button launches the reading of the data and adds notes
        self.start_button = QPushButton(text="Start?")
        self.start_button.clicked.connect(self.read_data_and_order)
        # start ability to have multiple threads

        self.threadpool = QThreadPool()

        # create widget that does the notes
        self.note_widget = QLabel()

        self.note_widget.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.note_widget)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.setFixedSize(QSize(1000, 600))

    def read_data_and_order(self):
        """
        This function reads 
        """
        # read corresponding keys
        self.data = pd.read_csv("./piano_package/piano_config_67k.csv", index_col=0)
        # self.data = pd.read_csv("./piano_package/launchpad_config.csv", index_col=0)
        # TODO: implement that one can randomise order
        # TODO: option for actual piano keys
        # all keys to be played are stored in self objects and will then accessed via an integer that changes after a note was pressed correctly/wrongly

        self.keys = self.data.key_id
        self.notes = self.data.note_files
        # only clickable once after all
        self.start_button.setEnabled(False)
        self.i = 0
        # start with first picture
        self.note_widget.setPixmap(
            QPixmap("./piano_package/Notes_piano/" + self.notes[0])
        )

        worker = Worker()
        self.threadpool.start(worker)
        # this takes the output/signal of the worker
        worker.signal.result.connect(self.test_input)

    def test_input(self, s):
        """
        This function does something with the signal from our
        """
        key = s

        # since the integer was
        if key == self.keys[self.i]:
            # right or wrong
            self.note_widget.setText("RIGHT")
            # quickly communicate with main loop so that picture is changed without having to implement with another worker
            QApplication.processEvents()
            QThread.sleep(1)
        elif key != self.keys[self.i]:
            self.note_widget.setText("WRONG")
            QApplication.processEvents()
            QThread.sleep(1)

        # increases integer index so next note strored in self.notes can be displayed
        self.i = self.i + 1

        self.note_widget.setPixmap(
            QPixmap("./piano_package/Notes_piano/" + self.notes[self.i])
        )
        # self.start_button.setText(s)

    def midi_beta(self):
        key_binding = pd.read_csv("piano_package/launchpad_config.csv", index_col=0)
        for idx, row in key_binding.iterrows():
            self.widget.setPixmap(QPixmap("piano_package/Notes/" + row["note_files"]))
            QApplication.processEvents()
            QThread.sleep(2)
        print("end")


# create the application and the main window
app = QApplication(sys.argv)
window = MainWindow()

# setup stylesheet
apply_stylesheet(app, theme="dark_red.xml")

# run
window.show()
app.exec_()
