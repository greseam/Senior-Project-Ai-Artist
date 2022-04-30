#############################################
# Author: Sean Gregor
#
#   Project: AI Artist
#
#   
#
#############################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys

#users -- using a dictionary to simplify workload, under real project restraints this would be a sql server of somekind
users = {
    "johnsmith": "1234abc" #bad password is bad i know, but used only for debugging and prototyping
}

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        #load the ui
        uic.loadUi("uiref/gen.ui",self)

        #define window parameters
        width = 1200
        height = 800
        self.setFixedSize(width,height)
        title = "Ai Artist"
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("uiref/icon.jpg"))
        
        #define Widgets
        self.label = self.findChild(QLabel, "label_2")
        self.textedit = self.findChild(QTextEdit, "seed")
        self.genBttn = self.findChild(QPushButton, "pushButton")
        self.info = self.findChild(QPushButton, "info_bttn")

        self.genBttn.clicked.connect(self.clicker)

        #show the UI
        self.show()


    def clicker(self):
        #self.label.setText(f'Hello there {self.textedit.toPlainText()}') 
        seed = self.textedit.toPlainText()
        print(seed)
        self.textedit.setPlainText("")




#initalize app
app = QApplication(sys.argv)
UIWindow  = UI()

app.exec()