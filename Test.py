# This python file serves as a test for the package as it imports it and can be used to launch the progran

from piano_package import midi_piano

piano = midi_piano()

piano.setup_midi()

help(midi_piano)

piano.test_run()

        