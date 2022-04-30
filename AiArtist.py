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
import pickle
import torch
from torch_utils import *
from dnnlib import *

import sys


#users -- using a dictionary to simplify workload, under real project restraints this would be a sql server of somekind
users = {
    "johnsmith": "1234abc" #bad password i know, but used only for debugging and prototyping
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

        self.genBttn.clicked.connect(self.generateImage)

        #show the UI
        self.show()


    def generateImage(self):
        
        #!!Button disapear
        #!!loading/progress bar
        
        
        #self.label.setText(f'Hello there {self.textedit.toPlainText()}') 

        seed = self.textedit.toPlainText()
        
        #put seed usage here
        print(seed)
        
        self.textedit.setPlainText("")


        #put img gen code here
        pkl = "network-snapshot-000400.pkl"
        pkl = f"./data/{pkl}"
        with open(pkl, 'rb') as f:
            G = pickle.load(f)['G_ema'].cuda()  # torch.nn.Module
        z = torch.randn([1, G.z_dim]).cuda()    # latent codes
        c = None                                # class labels (not used in this example)
        img = G(z, c)                           # NCHW, float32, dynamic range [-1, +1]
        
        w = G.mapping(z, c, truncation_psi=0.5, truncation_cutoff=8)
        img = G.synthesis(w, noise_mode='const', force_fp32=True)


        #display to label_2 code here
        self.im = QPixmap(img)
        #self.im = QPixmap("./uiref/icon.jpg")
        self.label.setPixmap(self.im)

        #!!button becomes active

    #select pickle


#initalize app
app = QApplication(sys.argv)
UIWindow  = UI()

app.exec()