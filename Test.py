# This python file serves as a test for the package as it imports it and can be used to launch the progran


import unittest
import piano_package as pp

unittest discover 
# pp.test_run(device="piano1")

device, config_file_df, path = pp.setup_midi(device="launchpad")



# piano.test_run()
