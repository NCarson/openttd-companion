from PyQt5.QtWidgets import (
    QWidget, QAction,
    QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit,
)
from PyQt5.QtGui import(
    #QKeySequence, QIcon,
    QColor, 
    QTextDocument, QTextCursor, 
    QTextFormat, QTextBlockFormat, QTextCharFormat
)
from PyQt5.QtCore import(
    Qt, 
)

from .view import View

def tr(text): return text

class MainWidget(QWidget):

    def __init__(self):
        super().__init__()
        #self.actions = self._initActions(self.view)
        self.actions = {}

        self._output = TextOutputWidget()
        self._input = TextInputWidget(self.onInput)

        outer = QVBoxLayout()
        #outer.addStretch(1)
        outer.addWidget(self._output)
        outer.addWidget(self._input)
        self.setLayout(outer)

    def onInput(self, text):
        print(11, text)

    def _initActions(self, view):
        pass


class TextOutputWidget(QTextEdit):

    style_dark = '''
        QTextEdit { 
            font-family: monospace;
            background-color: black;
            color: white;
        }

    '''
    
    def __init__(self):
        super().__init__()
        #self.setTextBackgroundColor(Qt.black)

        self.setReadOnly(True)
        self.setStyleSheet(self.style_dark)
        self._history = []

        for i in range(13):
            self.appendLogLine(1, "[today]", "stuff happened")

    def appendLogLine(self, level, stamp, line):

        cursor = self.textCursor()
        fmt = QTextCharFormat()
        fmt.setFontFamily("monospace")

        fmt.setForeground(Qt.blue)
        cursor.setCharFormat(fmt)
        if self._history:
            cursor.insertText("\n")
        cursor.insertText(stamp.strip())

        fmt.setForeground(Qt.white)
        cursor.setCharFormat(fmt)
        cursor.insertText(" " + line.strip())

        self._history.append((level, stamp, line))


class TextInputWidget(QLineEdit):

    style_dark = '''
        QLineEdit { 
            font-family: monospace;
            background-color: black;
            color: white;
            margin: 0;
            padding: .5em;
            font-size: bigger;
        }

    '''

    def __init__(self, callback):
        super().__init__()
        self.insert("> ")
        self.callback = callback
        self.setStyleSheet(self.style_dark)

    def onReturnPressed(self):
        text = self.text()
        if text[0] == ">":
            text = text[1:]
        text = text.strip()
        self.callback(text)
        self.clear()
        self.insert("> ")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.onReturnPressed()
        else:
            super().keyPressEvent(event)
