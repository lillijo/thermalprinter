# importing libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


# window class
class Drawing(QDialog):
    def __init__(self, file_path: str, image: QImage):
        super().__init__()
        self.file_path = file_path
        # setting title
        self.setWindowTitle("Paint On Image")

        # setting geometry to main window
        self.resize(350, 300)

        self.image = image
        self.resize(image.size())

        # variables
        # drawing flag
        self.drawing = False
        # default brush size
        self.brushSize = 2
        # default color
        self.brushColor = Qt.black

        # QPoint object to tract the point
        self.lastPoint = QPoint()

        # creating menu bar
        mainMenu = QHBoxLayout()

        # creating save action
        saveAction = QPushButton("Save", self)
        mainMenu.addWidget(saveAction)
        # adding action to the save
        saveAction.clicked.connect(self.save)

        # creating clear action
        clearAction = QPushButton("Clear", self)
        mainMenu.addWidget(clearAction)
        # adding action to the clear
        clearAction.clicked.connect(self.clear)

        # creating clear action
        cancelAction = QPushButton("Cancel", self)
        mainMenu.addWidget(cancelAction)
        # adding action to the clear
        cancelAction.clicked.connect(self.cancel)

        # creating options for brush sizes
        # creating action for selecting pixel of 4px
        pix_4 = QPushButton("4px", self)
        # adding this action to the brush size
        mainMenu.addWidget(pix_4)
        # adding method to this
        pix_4.clicked.connect(self.Pixel_4)

        # similarly repeating above steps for different sizes
        pix_7 = QPushButton("7px", self)
        mainMenu.addWidget(pix_7)
        pix_7.clicked.connect(self.Pixel_7)

        pix_9 = QPushButton("9px", self)
        mainMenu.addWidget(pix_9)
        pix_9.clicked.connect(self.Pixel_9)

        pix_12 = QPushButton("12px", self)
        mainMenu.addWidget(pix_12)
        pix_12.clicked.connect(self.Pixel_12)
        
        layout = QVBoxLayout()
        #layout.addStretch()
        layout.addLayout(mainMenu)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        container = QWidget(self)
        container.setLayout(layout)


    # method for checking mouse cicks
    def mousePressEvent(self, event):
        # if left mouse button is pressed
        if event.button() == Qt.LeftButton:
            # make drawing flag true
            self.drawing = True
            # make last point to the point of cursor
            self.lastPoint = event.pos()

    # method for tracking mouse activity
    def mouseMoveEvent(self, event):
        # checking if left button is pressed and drawing flag is true
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            # creating painter object
            painter = QPainter(self.image)

            # set the pen of the painter
            painter.setPen(
                QPen(
                    self.brushColor,
                    self.brushSize,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin,
                )
            )

            # draw line from the last point of cursor to the current point
            # this will draw only one step
            painter.drawLine(self.lastPoint, event.pos())

            # change the last point
            self.lastPoint = event.pos()
            # update
            self.update()

    # method for mouse left button release
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # make drawing flag false
            self.drawing = False

    # paint event
    def paintEvent(self, event):
        # create a canvas
        canvasPainter = QPainter(self)

        # draw rectangle on the canvas
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # method for saving canvas
    def save(self):
        print(self.file_path)
        self.image.save(self.file_path)
        self.close()

    # method for saving canvas
    def cancel(self):
        self.close()

    # method for clearing every thing on canvas
    def clear(self):
        # make the whole canvas white
        self.image.fill(Qt.white)
        # update
        self.update()

    # methods for changing pixel sizes
    def Pixel_4(self):
        self.brushSize = 4

    def Pixel_7(self):
        self.brushSize = 7

    def Pixel_9(self):
        self.brushSize = 9

    def Pixel_12(self):
        self.brushSize = 12


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = Drawing("test")
    main_win.show()
    sys.exit(app.exec())
