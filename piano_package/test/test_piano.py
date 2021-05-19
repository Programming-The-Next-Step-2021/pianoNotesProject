import unittest


import piano_package as pp


class TestNotes(unittest.TestCase):
    """
    This test function checks whether the correct notes are loaded with the initialisation function
    Because if the wrong notes are loaded, the whole programm doesn't work.
    """

    def test_read_launchpad(self):
        device, config_file_df, path = pp.setup_midi(device="launchpad")

        test_list = [
            "1_Treble_C4_Natural.png",
            "2_Treble_D4_Natural.png",
            "3_Treble_E4_Natural.png",
            "4_Treble_F4_Natural.png",
            "5_Treble_G4_Natural.png",
            "6_Treble_A4_Natural.png",
            "7_Treble_B4_Natural.png",
            "8_Treble_C5_Natural.png",
        ]
        self.assertEqual(first=config_file_df.note_files.tolist(), second=test_list)

    def test_read_piano(self):
        device, config_file_df, path = pp.setup_midi(device="piano1")
        test_list = [
            "16_Note-Bass-C2.png",
            "17_Note-Bass-C2s.png",
            "17_Note-Bass-D2b.png",
            "18_Note-Bass-D2.png",
            "19_Note-Bass-D2s.png",
            "19_Note-Bass-E2b.png",
            "20_Note-Bass-E2.png",
            "21_Note-Bass-F2.png",
            "22_Note-Bass-F2s.png",
            "22_Note-Bass-G2b.png",
            "23_Note-Bass-G2.png",
            "24_Note-Bass-A2b.png",
            "24_Note-Bass-G2s.png",
            "25_Note-Bass-A2.png",
            "26_Note-Bass-A2s.png",
            "26_Note-Bass-B2b.png",
            "27_Note-Bass-B2.png",
            "28_Note-Bass-C3.png",
            "29_Note-Bass-C3s.png",
            "29_Note-Bass-D3b.png",
            "30_Note-Bass-D3.png",
            "31_Note-Bass-D3s.png",
            "31_Note-Bass-E3b.png",
            "32_Note-Bass-E3.png",
            "33_Note-Bass-F3.png",
            "34_Note-Bass-F3s.png",
            "34_Note-Bass-G3b.png",
            "35_Note-Bass-G3.png",
            "36_Note-Bass-A3b.png",
            "36_Note-Bass-G3s.png",
            "36_Note-Treble-A3b.png",
            "37_Note-Bass-A3.png",
            "37_Note-Treble-A3.png",
            "38_Note-Bass-A3s.png",
            "38_Note-Bass-B3b.png",
            "38_Note-Treble-A3s.png",
            "38_Note-Treble-B3b.png",
            "39_Note-Bass-B3.png",
            "39_Note-Treble-B3.png",
            "40_Note-Bass-C4.png",
            "40_Note-Treble-C4.png",
            "41_Note-Bass-C4s.png",
            "41_Note-Bass-D4b.png",
            "41_Note-Treble-C4s.png",
            "41_Note-Treble-D4b.png",
            "42_Note-Bass-D4.png",
            "42_Note-Treble-D4.png",
            "43_Note-Bass-D4s.png",
            "43_Note-Bass-E4b.png",
            "43_Note-Treble-D4s.png",
            "43_Note-Treble-E4b.png",
            "44_Note-Bass-E4.png",
            "44_Note-Treble-E4.png",
            "45_Note-Treble-F4.png",
            "46_Note-Treble-F4s.png",
            "46_Note-Treble-G4b.png",
            "47_Note-Treble-G4.png",
            "48_Note-Treble-A4b.png",
            "48_Note-Treble-G4s.png",
            "49_Note-Treble-A4.png",
            "50_Note-Treble-A4s.png",
            "50_Note-Treble-B4b.png",
            "51_Note-Treble-B4.png",
            "52_Note-Treble-C5.png",
            "53_Note-Treble-C5s.png",
            "53_Note-Treble-D5b.png",
            "54_Note-Treble-D5.png",
            "55_Note-Treble-D5s.png",
            "55_Note-Treble-E5b.png",
            "56_Note-Treble-E5.png",
            "57_Note-Treble-F5.png",
            "58_Note-Treble-F5s.png",
            "58_Note-Treble-G5b.png",
            "59_Note-Treble-G5.png",
            "60_Note-Treble-A5b.png",
            "60_Note-Treble-G5s.png",
            "61_Note-Treble-A5.png",
            "62_Note-Treble-A5s.png",
            "62_Note-Treble-B5b.png",
            "63_Note-Treble-B5.png",
        ]
        self.assertEqual(first=config_file_df.note_files.tolist(), second=test_list)


if __name__ == "__main__":
    unittest.main()
