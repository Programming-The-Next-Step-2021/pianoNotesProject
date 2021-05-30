import piano_package as pp

app = pp.QApplication(pp.sys.argv)
window = pp.MainWindow()

# setup stylesheet
pp.apply_stylesheet(app, theme="dark_red.xml")

# run
window.show()

app.exec_()
