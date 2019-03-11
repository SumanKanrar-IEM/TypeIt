from PyQt4 import QtGui
from PyQt4 import QtCore


class Editor(QtGui.QTextEdit):

    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)


class Main(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.initUi()

    def initUi(self):
        self.setWindowTitle("Editor")
        self.resize(640, 480)

        newAc = QtGui.QAction('New', self)
        newAc.setShortcut('Ctrl+N')
        newAc.triggered.connect(self.new_)

        menu = self.menuBar()
        filemenu = menu.addMenu('&File')
        filemenu.addAction(newAc)

        self.tab = QtGui.QTabWidget(self)
        self.setCentralWidget(self.tab)
        self.tab.addTab(Editor(), "New Text")

    def new_(self):
        self.tab.addTab(Editor(), "New text")


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()