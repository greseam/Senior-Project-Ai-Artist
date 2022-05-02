#############################################
# Author: Sean Gregor
#
#   Project: AI Artist
#
#   
#
#############################################

from ast import If
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
        self.infoText = QLabel("label", self)
        self.infoText.setGeometry(130,620, 181,151)
        self.infoText.setText("i: This is a tab for generating images based on a numerical seed. It generates images trained from Nvidias StyleGan2 ada-Pytorch architecure.")
        self.infoText.setHidden(False)
        self.infoText.setAlignment(Qt.AlignLeft)
        self.infoText.setStyleSheet("border :2px solid black; font-size: 10pt;color: rgb(226, 228, 246);background-color: rgb(111, 104, 109);")
        self.infoText.setWordWrap(True)


        self.genBttn.clicked.connect(self.generateImage)
        self.info.clicked.connect(self.infoButton)

        #show the UI
        self.show()

    #infoBttn
    def infoButton(self):
        print(str(self.infoText.isVisible))
        if self.infoText.isVisible == False:
            self.infoText.setHidden(True)
        elif self.infoText.isVisible == True:
            self.infoText.setHidden(False)

    def generateImage(self):
        
        #!!loading/progress bar
        self.loadin.setHidden(False)
        
        #self.label.setText(f'Hello there {self.textedit.toPlainText()}') 

        seed = self.textedit.toPlainText()
        
        #put seed usage here
        print(seed)
        
        self.textedit.setPlainText("")
        self.loadin.setValue(10)

        #put img gen code here
        pkl = "network-snapshot-000400.pkl"
        pkl = f"./data/{pkl}"
        #with open(pkl, 'rb') as f:
        #    G = pickle.load(f)['G_ema'].cuda()  # torch.nn.Module
        #z = torch.randn([1, G.z_dim]).cuda()    # latent codes
        self.loadin.setValue(25)

        #c = None                                # class labels (not used in this example)
        #img = G(z, c)                           # NCHW, float32, dynamic range [-1, +1]
        self.loadin.setValue(35)

        #w = G.mapping(z, c, truncation_psi=0.5, truncation_cutoff=8)
        #img = G.synthesis(w, noise_mode='const', force_fp32=True)
        self.loadin.setValue(45)


        # Generate images.
        print(f'Generating image for seed {seed} ...')
        #z = torch.from_numpy(np.random.RandomState(seed).randn(1, G.z_dim)).to(device)
        self.loadin.setValue(55)
        #img = G(z, label, truncation_psi=truncation_psi, noise_mode=noise_mode)
        self.loadin.setValue(70)
        #img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
        self.loadin.setValue(80)
        #PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB').save(f'{outdir}/seed{seed:04d}.png')
        self.loadin.setValue(90)
        for i in range(11):
  
            # slowing down the loop
            time.sleep(0.05)
  
            # setting value to progress bar
            self.loadin.setValue(90+i)        


        self.loadin.setHidden(True)
        

        #display to label_2 code here
        #self.im = QPixmap(f'{outdir}/seed{seed:04d}.png')
        self.im = QPixmap("./images/image_512.jpg")
        self.label.setPixmap(self.im)

        #!!button becomes active

    #select pickle



#initalize app
app = QApplication(sys.argv)
UIWindow  = UI()

app.exec()