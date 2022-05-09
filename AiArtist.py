#############################################
# Author: Sean Gregor
#
#   Project: AI Artist
#
#   
#
#############################################

from ast import If
from asyncio.windows_events import NULL
from distutils.log import info
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import numpy as np
import PIL.Image
import pickle
import torch
import time

from torch_utils import *
from dnnlib import *

import sys


#users -- using a dictionary to simplify workload, under real project restraints this would be a sql server of somekind
users = {
    "johnsmith": "1234abc" #bad password i know, but used only for debugging and prototyping
}

outdir = "./images/"

device = torch.device('cuda')


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ai Artist")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Please Select a Pkl file.")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

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
        self.loadin = self.findChild(QProgressBar, "progressBar")
        self.loadin = QProgressBar(self)
        self.loadin.setGeometry(840,640, 251, 41)
        self.loadin.setHidden(True)



        self.genBttn.clicked.connect(self.buttonClick)
        self.info.clicked.connect(self.infoButton)

        #show the UI
        self.show()

    #infoBttn
    def infoButton(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Info")
        width_i = 800
        height_i = 300
        dlg.setFixedSize(width_i,height_i)
        uic.loadUi("uiref/info_gen.ui",dlg)
        
        dlg.exec()

    def buttonClick(self): 

        seeds = self.textedit.toPlainText()
        #put seed usage here
        if seeds is not None:
            self.textedit.setPlainText("")

            dlg = CustomDialog(self)
            if dlg.exec():
                print("Success!")
                fname = QFileDialog.getOpenFileName(self, "Open Pkl file", "","Pickle File (*.pkl)")
                if fname[0] != '':
                    
                    #!!loading/progress bar
                    self.loadin.setHidden(False)
                    self.loadin.setValue(10)


                    #load pkl file
                    pkl = fname
                    print('Loading networks from "%s"...' % pkl)
                    device = torch.device('cuda')
                    self.loadin.setValue(25)
                    with dnnlib.util.open_url(pkl) as f:
                        G = legacy.load_network_pkl(f)['G_ema'].to(device) 
                    

                    #generate image
                    print('Generating image for seed %d ...' % (seeds))
                    self.loadin.setValue(35)
                    z = torch.from_numpy(np.random.RandomState(seeds).randn(1, G.z_dim)).to(device)

                    self.loadin.setValue(45)
                    img = G(z, None, truncation_psi=1, noise_mode="none")
                    self.loadin.setValue(55)

                    img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
                    self.loadin.setValue(75)
                    PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB').save(f'{outdir}/seed{seeds:04d}.png')
                    self.loadin.setValue(90)
                    
                    #loading bar progress
                    for i in range(11):
            
                        # slowing down the loop
                        time.sleep(0.05)
            
                        # setting value to progress bar
                        self.loadin.setValue(90+i)        


                    self.loadin.setHidden(True)
                    

                    #display to label_2 code here
                    self.im = QPixmap(f'{outdir}/seed{seed:04d}.png')
                    #self.im = QPixmap("./images/image_512.jpg") #test code, displays an image to label_2 *ignores generate method
                    
                    self.label.setPixmap(self.im)
                    
                else:
                    print("Cancel3")           
            else:
                print("Cancel2")
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Oops!")
            dlg.setText("Please enter a seed")
            button = dlg.exec()

            if button == QMessageBox.Ok:
                print("Cancel1")


#initalize app
app = QApplication(sys.argv)
UIWindow  = UI()

app.exec()