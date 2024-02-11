from PyQt5.QtWidgets import (
 QApplication, QWidget, QFileDialog,
 QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import os
from PIL import Image
from PIL.ImageFilter import SHARPEN
app = QApplication([])
win = QWidget()
win.resize(1200, 700)
win.setWindowTitle('Easy Editor')
win.setStyleSheet('background-color:#03fcf8; font-size:24px; padding:5px; color:white')

lb_image = QLabel('Картинка')
btn_dir = QPushButton('Папка')
lw_files = QListWidget()
btn_left = QPushButton('Вліво')
btn_right = QPushButton('Вправо')
btn_flip = QPushButton('Віддзеркалити')
btn_sharp = QPushButton('Різкість')
btn_bw = QPushButton('Ч-б')

btn_dir.setStyleSheet('background-color:blue; border;2px solid white; border-radius: 10px')
btn_left.setStyleSheet('background-color:blue; border;2px solid white; border-radius: 10px')
btn_right.setStyleSheet('background-color:blue; border;2px solid white; border-radius: 10px')
btn_flip.setStyleSheet('background-color:blue; border;2px solid white; border-radius: 10px')
btn_bw.setStyleSheet('background-color:blue; border;2px solid white; border-radius: 10px')
btn_sharp.setStyleSheet('background-color:blue; border;2px solid white; border-radius: 10px')

btn_left.setCursor(Qt.PointingHandCursor)
btn_right.setCursor(Qt.PointingHandCursor)
btn_flip.setCursor(Qt.PointingHandCursor)
btn_sharp.setCursor(Qt.PointingHandCursor)
btn_bw.setCursor(Qt.PointingHandCursor)

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col3 = QVBoxLayout()

col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image)
col3.addWidget(btn_left)
col3.addWidget(btn_right)
col3.addWidget(btn_flip)
col3.addWidget(btn_sharp)
col3.addWidget(btn_bw)

row.addLayout(col1, 20)
row.addLayout(col2, 60)
row.addLayout(col3, 20)
win.setLayout(row)

win.show()
workdir = ""
def filter(files, extensions):
    result = []
    for filename in files:
       for ext in extensions:
          if filename.endswith(ext):
           result.append(filename)
    return result

def chooseworkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = [".jpg", ".jpeg", ".png", ".gift"]
    chooseworkdir()
    filenames = filter(os.listdir(workdir), extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)
btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor:
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not (os.path.exists(path) and os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path= os.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        pixmapimage = pixmapimage.scaled(600, 650, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)
workimage = ImageProcessor()
lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)
app.exec_()