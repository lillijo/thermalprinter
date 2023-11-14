"""PyQt5 Multimedia Camera Example"""

import os
import sys
from PyQt5.QtCore import QDate, QDir, QStandardPaths, Qt, QUrl, QTimer
from PyQt5.QtGui import QPalette, QColor, QMouseEvent
from PyQt5.QtWidgets import (
    QApplication,
    QDialogButtonBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QButtonGroup,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QDialog,
    QLineEdit,
    QGridLayout,
)


colors = ["red", "blue", "orange", "green"]

smallkeys = [
    "^",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "ß",
    "<--",
    "tab",
    "q",
    "w",
    "e",
    "r",
    "t",
    "z",
    "u",
    "i",
    "o",
    "p",
    "ü",
    "+",
    "lock",
    "a",
    "s",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "ö",
    "ä",
    "#",
    "shift",
    "<",
    "y",
    "x",
    "c",
    "v",
    "b",
    "n",
    "m",
    ",",
    ".",
    "-",
    "enter",
    "space",
]
capitalkeys = [
    "°",
    "!",
    '"',
    "§",
    "$",
    "%",
    "&",
    "/",
    "(",
    ")",
    "=",
    "?",
    "<--",
    "tab",
    "Q",
    "W",
    "E",
    "R",
    "T",
    "Z",
    "U",
    "I",
    "O",
    "P",
    "Ü",
    "*",
    "lock",
    "A",
    "S",
    "D",
    "F",
    "G",
    "H",
    "J",
    "K",
    "L",
    "Ö",
    "Ä",
    "'",
    "shift",
    ">",
    "Y",
    "X",
    "C",
    "V",
    "B",
    "N",
    "M",
    ";",
    ":",
    "_",
    "enter",
    "space",
]


class KeyButton(QPushButton):
    def __init__(self, color, k, func):
        super(QPushButton, self).__init__(k)
        self.setAutoFillBackground(True)
        self.kval = k
        self.parentfunc = func
        self.setStyleSheet(
            "color: black;" f"background-color: {color}; padding: 2px; margin: 0px; "
        )
        self.clicked.connect(self.click_key)

    def click_key(self, e):
        self.parentfunc(self.kval)


class DescriptionDialog(QDialog):
    def __init__(self, description, parent=None):
        super().__init__(parent)
        self.resize(470, 250)
        self.setWindowTitle("Write Description of Image")

        self.description = description
        self.description_box = QLabel(self.description)

        self.description_box.setStyleSheet(
            "color: black; padding: 0px; background-color: white; margin: 0;"
        )

        self.group = QButtonGroup()
        layout_small = QGridLayout()
        layout_capital = QGridLayout()
        layout_small.setSpacing(0)
        layout_capital.setSpacing(0)
        layout_small.setContentsMargins(0,0,0,0)
        layout_capital.setContentsMargins(0,0,0,0)
        row = 0
        total = 0
        self.caps_lock = False
        self.caps = False
        for i, k in enumerate(smallkeys):
            col = i - total
            if k == "tab":
                row = 1
                total = i
                button = KeyButton("white", k, self.button_clicked)
                layout_small.addWidget(button, row, 0)
                buttonk = KeyButton("white", k, self.button_clicked)
                layout_capital.addWidget(buttonk, row, 0)
            elif k == "lock":
                row = 2
                total = i
                button = KeyButton("white", k, self.button_clicked)
                layout_small.addWidget(button, row, 0)
                buttonk = KeyButton("gray", k, self.button_clicked)
                layout_capital.addWidget(buttonk, row, 0)
            elif k == "shift":
                row = 3
                total = i
                button = KeyButton("white", k, self.button_clicked)
                layout_small.addWidget(button, row, 0)
                buttonk = KeyButton("white", k, self.button_clicked)
                layout_capital.addWidget(buttonk, row, 0)
            elif k == "space":
                row = 4
                total = i
                button = KeyButton("gray", k, self.button_clicked)
                layout_small.addWidget(button, row, 0)
                buttonk = KeyButton("gray", k, self.button_clicked)
                layout_capital.addWidget(buttonk, row, 0)
                saveb_small = KeyButton("#0f0", "save", self.accept)
                saveb_cap = KeyButton("#0f0", "save", self.accept)
                layout_small.addWidget(saveb_small, row, 12)
                layout_capital.addWidget(saveb_cap, row, 12)
            else:
                color = colors[i % 3]
                button = KeyButton(color, k, self.button_clicked)
                layout_small.addWidget(button, row, col)
                button_cap = KeyButton(color, capitalkeys[i], self.button_clicked)
                layout_capital.addWidget(button_cap, row, col)
            self.group.addButton(button)
        self.tabs = QTabWidget()
        swidget = QWidget()
        swidget.setLayout(layout_small)
        self.tabs.addTab(swidget, "0")
        cwidget = QWidget()
        cwidget.setLayout(layout_capital)
        self.tabs.addTab(cwidget, "1")
        swidget.setStyleSheet("padding: 0px; margin: 0px;")
        cwidget.setStyleSheet("padding: 0px; margin: 0px;")
        self.tabs.setStyleSheet(
            "QTabWidget::pane { margin: 0px; border: none; padding: 0px; top: -32px;} QTabBar::tab {margin:0px; padding:0px; font-size: 1px;}"
        )
        self.tabs.tabBar().setDrawBase(False)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.description_box)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def accept(self, e):
        loc = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DesktopLocation
        )
        fn = f"{loc}/description.txt"
        with open(fn, "w") as file:
            file.write(self.description)
        super().accept()

    def button_clicked(self, x):
        kval = x
        if kval == "tab":
            self.description += " "
        elif kval == "shift":
            if self.caps or self.caps_lock:
                self.tabs.setCurrentIndex(0)
                self.caps = False
            else:
                self.tabs.setCurrentIndex(1)
                self.caps = True
        elif kval == "lock":
            if self.caps_lock:
                self.tabs.setCurrentIndex(0)
                self.caps_lock = False
            else:
                self.tabs.setCurrentIndex(1)
                self.caps_lock = True
        elif kval == "<--":
            self.description = self.description[0:-1]
        elif kval == "space":
            self.description += " "
        elif kval == "enter":
            self.description += "\n"
        else:
            if self.caps:
                self.caps = False
                self.tabs.setCurrentIndex(0)
            self.description += str(kval)
        self.description_box.setText(self.description)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = DescriptionDialog("test")
    main_win.show()
    sys.exit(app.exec())
