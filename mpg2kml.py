import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUiType

form_class = loadUiType("mpg2kml.ui")[0]

class MyWindowClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent )
        self.setupUi(self)
        self.mpg2kml.clicked.connect(self.mpg2kml_clicked)
        self.kml2mpg.clicked.connect(self.kml2mpg_clicked)
    def mpg2kml_clicked(self):
        try : 
            mpg=float(self.inputValue.toPlainText())
            kml=mpg*1.60934/3.78541
            self.output.setText(f"{kml:.2f}")
        except ValueError:
            self.output.setText("Invalid Input")
            
    def kml2mpg_clicked(self):
        try:
            kml=float(self.inputValue.toPlainText())
            mpg = kml*3.78541 / 1.60934
            self.output.setText(f"{mpg:.2f}")
        except ValueError:
            self.output.setText("Invalid Input") 
            
app=QApplication(sys.argv)
myWindow=MyWindowClass(None)
myWindow.show()
app.exec_()


