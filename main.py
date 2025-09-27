#создай тут фоторедактор Easy Editor!
from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import SHARPEN
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QRadioButton, QGroupBox, QButtonGroup, QTextEdit, QListWidget, QVBoxLayout, QLineEdit, QInputDialog,QFileDialog
from PyQt5.QtGui import QPixmap

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Easy Editor')
main_win.resize(1000,700)
image = QLabel('Картинка')
p = QPushButton('Папка')
i_files = QListWidget()


btn_left = QPushButton('Лево')
btn_right = QPushButton('Вправо')
btn_sharp = QPushButton('Резкость')
btn_mirror = QPushButton('Зеркало')
btn_btw = QPushButton('Ч/Б')

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_p = "/Modified"
    def loadImage (self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        image.hide()
        pixmapimage = QPixmap(path)
        w, h = image.width(), image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        image.setPixmap(pixmapimage)
        image.show()
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path=os.path.join(workdir, self.save_p, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_p, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_p, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image =  self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_p, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image =  self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_p, self.filename)
        self.showImage(image_path)


    def saveImage(self):
        path = os.path.join(workdir, self.save_p)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)
    

workimage = ImageProcessor()

def showChosenImage():
    if i_files.currentRow() >= 0:
        filename = i_files.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)

i_files.currentRowChanged.connect(showChosenImage)
btn_btw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_mirror.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharpen)       

workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def showFilenameList():
    extensions = ['.jpg', '.png', '.gif', '.jpeg']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    i_files.addItems(filenames)
p.clicked.connect(showFilenameList)

def filter(i_files,extensions):
    result = []
    for filename in i_files:
        for ex in extensions:
            if filename.endswith(ex):
                result.append(filename)
    return result



main_line = QHBoxLayout()
one_line = QVBoxLayout()
two_line = QVBoxLayout()


one_line.addWidget(p)
one_line.addWidget(i_files)
two_line.addWidget(image)
line_buttons = QHBoxLayout()

line_buttons.addWidget(btn_left)
line_buttons.addWidget(btn_right)
line_buttons.addWidget(btn_sharp)
line_buttons.addWidget(btn_mirror)
line_buttons.addWidget(btn_btw)

two_line.addLayout(line_buttons)

main_line.addLayout(one_line)
main_line.addLayout(two_line)
main_win.setLayout(main_line)

main_win.show()
app.exec_()