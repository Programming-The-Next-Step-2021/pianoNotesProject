from PySide6 import QtTest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
import unittest
import piano_package as pp


class TestDataLoading(unittest.TestCase):
    def setup(self):
        self.app = pp.QApplication(pp.sys.argv)
        window = pp.MainWindow()
        