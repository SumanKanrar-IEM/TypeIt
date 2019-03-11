import sys
import PyPDF2
import os
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
import webbrowser


class Window(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setWindowIcon(QtGui.QIcon("icons/text-editor.png"))
        self.setWindowTitle('TypeIt Mini Text Editor')
        self.statusbar = self.statusBar().showMessage("Qt Mini text Editor Application Launched!!")
        self.saved_data = ''
        self.wrap_mode = False
        self.filename = ""
        self.changesSaved = True
        self.setGeometry(50, 50, 640, 300)

        self.menu()
        self.home()
        self.show()

    def menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        edit = mainMenu.addMenu('Edit')
        datetime = mainMenu.addMenu('Insert')
        view = mainMenu.addMenu('View')
        formatMenu = mainMenu.addMenu('Format')
        helpMenu = mainMenu.addMenu('Help')

        newFileAction = QtGui.QAction(QtGui.QIcon("icons/new.png"), 'New', self)
        newFileAction.triggered.connect(self.new_file)
        newFileAction.setShortcut('Ctrl+N')
        newFileAction.setStatusTip('Create a new file')

        openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"), "File Open ", self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a File')
        # TODO
        # Check the extension of the file and call the open function accordingly.

        openAction.triggered.connect(self.open_File)

        saveFileAction = QtGui.QAction(QtGui.QIcon("icons/Save-as.png"), "File Save As...", self)
        saveFileAction.setStatusTip("Save document")
        saveFileAction.setShortcut("Ctrl+S")
        saveFileAction.triggered.connect(self.File_save)

        saveAsFileAction = QtGui.QAction(QtGui.QIcon("icons/save.png"), "Save", self)
        saveAsFileAction.setStatusTip("Save document")
        saveAsFileAction.setShortcut("Ctrl+S")
        saveAsFileAction.triggered.connect(self.File_save_text)

        exitAction = QtGui.QAction(QtGui.QIcon('icons/Exit.png'), 'Exit', self)
        exitAction.triggered.connect(self.exit_fuction)
        exitAction.setShortcut('Ctrl+Q')

        printAction = QtGui.QAction(QtGui.QIcon("icons/print.png"), "Print document", self)
        printAction.setStatusTip("Print document")
        printAction.setShortcut("Ctrl+P")
        printAction.triggered.connect(self.Print)

        dateAction = QtGui.QAction(QtGui.QIcon("icons/Calender.png"), "Date", self)
        dateAction.setStatusTip("Insert date")
        dateAction.setShortcut("Ctrl+d")
        dateAction.triggered.connect(self.date)

        timeAction = QtGui.QAction(QtGui.QIcon("icons/Date_and_time.png"), "Time", self)
        timeAction.setStatusTip("Insert time")
        timeAction.setShortcut("Ctrl+t")
        timeAction.triggered.connect(self.time)

        cutAction = QtGui.QAction(QtGui.QIcon("icons/cut.png"), "Cut to clipboard", self)
        cutAction.setStatusTip("Delete and copy text to clipboard")
        cutAction.setShortcut("Ctrl+X")
        cutAction.triggered.connect(self.Cut)

        copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"), "Copy to clipboard", self)
        copyAction.setStatusTip("Copy text to clipboard")
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self.Copy)

        pasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"), "Paste from clipboard", self)
        pasteAction.setStatusTip("Paste text from clipboard")
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.triggered.connect(self.Paste)

        undoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"), "Undo last action", self)
        undoAction.setStatusTip("Undo last action")
        undoAction.setShortcut("Ctrl+Z")
        undoAction.triggered.connect(self.Undo)

        redoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"), "Redo last undone thing", self)
        redoAction.setStatusTip("Redo last undone thing")
        redoAction.setShortcut("Ctrl+Y")
        redoAction.triggered.connect(self.Redo)

        previewAction = QtGui.QAction(QtGui.QIcon("icons/if_Preview_.png"), "Page view", self)
        previewAction.setStatusTip("Preview page before printing")
        previewAction.setShortcut("Ctrl+Shift+P")
        previewAction.triggered.connect(self.PageView)

        pdfAction = QtGui.QAction(QtGui.QIcon("icons/ACP_PDF.png"), "Save To PDF File", self)
        pdfAction.setStatusTip("Save PDF to Document")
        pdfAction.triggered.connect(self.SavetoPDF)

        self.wrapAction = QtGui.QAction("WordWrap", self)
        self.wrapAction.triggered.connect(self.word_wrap)

        fontAction = QtGui.QAction(QtGui.QIcon("icons/Font.png"), 'Font', self)
        fontAction.triggered.connect(self.font_dialog)
        fontAction.setStatusTip('SetTextTont')

        colorAction = QtGui.QAction(QtGui.QIcon("icons/Color.png"), 'Color', self)
        colorAction.triggered.connect(self.colorDialog)
        colorAction.setStatusTip('SetTextColor')

        numberedAction = QtGui.QAction(QtGui.QIcon("icons/number.png"), "Insert numbered List", self)
        numberedAction.setStatusTip("Insert numbered list")
        numberedAction.setShortcut("Ctrl+Shift+L")
        numberedAction.triggered.connect(self.numberList)

        boldAction = QtGui.QAction(QtGui.QIcon("icons/bold.png"), "Bold", self)
        boldAction.triggered.connect(self.bold)

        italicAction = QtGui.QAction(QtGui.QIcon("icons/italic.png"), "Italic", self)
        italicAction.triggered.connect(self.italic)

        underlAction = QtGui.QAction(QtGui.QIcon("icons/underline.png"), "Underline", self)
        underlAction.triggered.connect(self.underline)

        alignLeft = QtGui.QAction(QtGui.QIcon("icons/align-left.png."), "Align left", self)
        alignLeft.triggered.connect(self.alignLeft)

        alignCenter = QtGui.QAction(QtGui.QIcon("icons/align-center.png"), "Align center", self)
        alignCenter.triggered.connect(self.alignCenter)

        alignRight = QtGui.QAction(QtGui.QIcon("icons/align-right.png"), "Align right", self)
        alignRight.triggered.connect(self.alignRight)

        alignJustify = QtGui.QAction(QtGui.QIcon("icons/align-justify.png"), "Align justify", self)
        alignJustify.triggered.connect(self.alignJustify)

        bulletAction = QtGui.QAction(QtGui.QIcon("icons/bullet.png"), "Insert Bullet List", self)
        bulletAction.triggered.connect(self.BulletList)

        helpAction = QtGui.QAction(QtGui.QIcon("icons/about.png"), "More Info", self)
        helpAction.triggered.connect(self.help_menu)

        self.toolbar2Height = 20  # added by Patrick
        self.fontFamily = QtGui.QFontComboBox(self)
        self.fontFamily.setMinimumHeight(self.toolbar2Height)  # added by Patrick
        self.fontFamily.currentFontChanged.connect(self.FontFamily)

        self.fontSize = QtGui.QComboBox(self)
        self.fontSize.setMinimumHeight(self.toolbar2Height)
        self.fontSize.setEditable(True)
        self.fontSize.setMinimumContentsLength(3)
        self.fontSize.activated.connect(self.FontSize)
        flist = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 26, 28, 32, 36, 40, 44, 48,
                 54, 60, 66, 72, 80, 88, 96]

        for i in flist:
            self.fontSize.addItem(str(i))

        self.toolbar = self.addToolBar("Options")
        # self.toolbar.setMaximumWidth(500)
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)
        self.toolbar.addSeparator()
        self.toolbar.setIconSize(QSize(16, 16))
        self.toolbar.addAction(newFileAction)
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(saveFileAction)
        self.toolbar.addAction(saveAsFileAction)
        self.toolbar.addAction(pdfAction)
        self.toolbar.addAction(printAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(undoAction)
        self.toolbar.addAction(redoAction)
        self.toolbar.addAction(cutAction)
        self.toolbar.addAction(copyAction)
        self.toolbar.addAction(pasteAction)

        self.toolbar.addAction(boldAction)
        self.toolbar.addAction(italicAction)
        self.toolbar.addAction(underlAction)
        self.toolbar.addAction(alignLeft)
        self.toolbar.addAction(alignCenter)
        self.toolbar.addAction(alignRight)
        self.toolbar.addAction(alignJustify)
        self.toolbar.addAction(bulletAction)
        self.toolbar.addSeparator()

        self.addToolBarBreak()
        # by Patrick. I broke up the toolbar and created a second tool bar
        self.toolbar2 = self.addToolBar('FontToolbar')
        self.toolbar2.setFloatable(False)
        self.toolbar2.setMovable(False)
        self.toolbar2.setMinimumHeight(self.toolbar2Height)
        self.toolbar2.addSeparator()
        self.toolbar2.addWidget(self.fontFamily)
        self.toolbar2.addWidget(self.fontSize)
        self.toolbar2.addSeparator()

        fileMenu.addAction(newFileAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveFileAction)
        fileMenu.addAction(saveAsFileAction)
        fileMenu.addAction(printAction)
        fileMenu.addAction(previewAction)
        fileMenu.addAction(pdfAction)
        fileMenu.addAction(exitAction)

        datetime.addAction(dateAction)
        datetime.addAction(timeAction)
        edit.addSeparator()
        edit.addAction(undoAction)
        edit.addAction(redoAction)
        edit.addAction(cutAction)
        edit.addAction(copyAction)
        edit.addAction(pasteAction)
        view.addAction(self.wrapAction)
        view.addAction(numberedAction)

        formatMenu.addAction(fontAction)
        formatMenu.addAction(colorAction)
        formatMenu.addAction(boldAction)
        formatMenu.addAction(italicAction)
        formatMenu.addAction(underlAction)
        formatMenu.addAction(alignLeft)
        formatMenu.addAction(alignCenter)
        formatMenu.addAction(alignRight)
        formatMenu.addAction(alignJustify)
        formatMenu.addAction(bulletAction)
        formatMenu.addAction(fontAction)
        formatMenu.addAction(colorAction)
        helpMenu.addAction(helpAction)

    def home(self):
        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setUndoRedoEnabled(True)
        self.textEdit.setAcceptRichText(False)
        self.setStyleSheet("QTextEdit{background-color: #404040}")
        self.textEdit.setStyleSheet("QTextEdit{font-size:20px;color:#ffffff}")
        self.textEdit.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.textFont = QtGui.QFont("Consolas", 15, )
        self.textEdit.setTabStopWidth(12)
        self.textEdit.setFont(self.textFont)
        # self.setCentralWidget(self.textEdit)
        self.tab = QtGui.QTabWidget(self)
        self.setCentralWidget(self.tab)
        self.tab.addTab(self.textEdit, "New Tab")


    def new_file(self):
        if self.textEdit.toPlainText() == self.saved_data:
            # self.textEdit.setText("")
            self.tab.addTab(self.textEdit, "New Tab")
        else:
            self.save_file_popup()

    def save_file_popup(self):
        choice = QtGui.QMessageBox.question(self, 'You have changes!', 'Do you want to quit?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.Yes:
            self.textEdit.setText("")
        else:
            pass

    # def open_Pdf_File(self, filename):
    #     if self.textEdit.toPlainText() == self.saved_data:
    #         self.textEdit.setText("")
    #         pass
    #
    #     # filter = "PDF (*.pdf);;"
    #     # filename = QtGui.QFileDialog.getOpenFileNameAndFilter(self, 'Open File', os.getenv('HOME'), filter)
    #     if filename:
    #         with open(filename, 'r') as pdf_file:
    #             pdfReader = PyPDF2.PdfFileReader(pdf_file)
    #             num_of_pages = pdfReader.numPages
    #             print(num_of_pages)
    #             pageObj = pdfReader.getPage(0)
    #             print(pageObj.extractText())
    #             pdf_file.close()

    def open_File(self):
        if self.textEdit.toPlainText() == self.saved_data:
            self.textEdit.setText("")
            pass

        # Change textEdit to QWebview
        # Read contents of the pdf file
        # SetContent() of the pdf to the QWebView

        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'),
                                                 "pdf(*.pdf);;txt(*.txt);;doc(*.doc)")
        if os.path.splitext(name)[1] == ".pdf":
            print(name)
            webbrowser.open_new(name)
        elif os.path.splitext(name)[1] == ".doc":
            with open(name, "rb") as docx_file:
                # Check if image is present in the document or not
                result = mammoth.convert_to_html(docx_file)
                html = result.value  # The generated HTML
                messages = result.messages  # Any messages, such as warnings during conversion


        else:
            if name:
                with open(name, 'r') as stream:
                    self.opendFileText = stream.read()
                    self.saved_data = self.opendFileText
                    self.textEdit.setText(self.opendFileText)
                self.current_save_file_path = name

        self.setWindowTitle(name + "Qt Mini text Editor")

    def File_save(self):

        # Only open dialog if there is no filename yet
        if not self.filename:
            self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', "",
                                                              "pdf(*.pdf);;txt(*.txt);;doc(*.doc)")

        if self.filename:

            # Append extension if not there yet
            if not str(self.filename).endswith(".writer"):
                self.filename += ".writer"
            # icons for the files.
            # We just store the contents of the text file along with the
            # format in html, which Qt does in a very nice way for us
            with open(self.filename, "wt") as file:
                file.write(self.textEdit.toHtml())

            self.changesSaved = True
            self.current_tab = self.tab.currentIndex()
            print(self.current_tab, self.filename)
            tab_text = os.path.basename(self.filename)
            self.tab.setTabText(self.current_tab, str(tab_text))

    def File_save_text(self):
        # Only open dialog if there is no filename yet
        if not self.filename:
            self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save As...')

        if self.filename:

            # Append extension if not there yet
            if not str(self.filename).endswith(".writer"):
                self.filename += ".writer"

            # We just store the contents of the text file along with the
            # format in html, which Qt does in a very nice way for us
            with open(self.filename, "wt") as file:
                file.write(self.textEdit.toHtml())

            self.changesSaved = True
            self.current_tab = self.tab.currentIndex()
            print(self.current_tab, self.filename)
            tab_text = os.path.basename(self.filename)
            self.tab.setTabText(self.current_tab, str(tab_text))

    def Cut(self):
        self.textEdit.cut()

    def Undo(self):
        self.textEdit.undo()

    def Redo(self):
        self.textEdit.redo()

    def Copy(self):
        self.textEdit.copy()

    def Paste(self):
        self.textEdit.paste()

    def Print(self):
        dialog = QtGui.QPrintDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.text.document().print(dialog.printer())

    def PageView(self):
        preview = QtGui.QPrintPreviewDialog()
        preview.paintRequested.connect(self.PaintPageView)
        preview.exec_()

    def PaintPageView(self, printer):
        self.textEdit.print_(printer)

    def SavetoPDF(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save to PDF', 'All Files', 'documents(*.PDF)')
        if name:
            printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
            printer.setPageSize(QtGui.QPrinter.A4)
            printer.setColorMode(QtGui.QPrinter.Color)
            printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            printer.setOutputFileName(name)
            self.textEdit.document().print_(printer)

    def word_wrap(self):
        if self.wrap_mode == False:
            self.wrap_mode = True
            self.wrapAction.setIcon(QtGui.QIcon('icons/True.png'))
            self.textEdit.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)

        # else:
        # self.word_wrap = False
        # self.wrapAction.setIcon(QtGui.QIcon('icons/False.png'))
        # self.textEdit.setWordWrapMode(QtGui.QTextOption.NoWrap)

    def font_dialog(self):
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

        else:
            font = QtGui.QFont("Consolas")
            self.textEdit.setCurrentFont(font)

    def FontFamily(self, font):
        font = QtGui.QFont(self.fontFamily.currentFont())
        self.textEdit.setCurrentFont(font)

    def FontSize(self, fsize):
        size = (int(fsize))
        self.textEdit.setFontPointSize(size)

    def colorDialog(self):
        color = QtGui.QColorDialog.getColor()
        self.textEdit.setTextColor(color)

    def numberList(self):

        cursor = self.textEdit.textCursor()

        # Insert list with numbers
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)

    def bold(self):

        if self.textEdit.fontWeight() == QtGui.QFont.Bold:

            self.textEdit.setFontWeight(QtGui.QFont.Normal)

        else:

            self.textEdit.setFontWeight(QtGui.QFont.Bold)

    def italic(self):

        state = self.textEdit.fontItalic()

        self.textEdit.setFontItalic(not state)

    def underline(self):

        state = self.textEdit.fontUnderline()

        self.textEdit.setFontUnderline(not state)

    def alignLeft(self):
        self.textEdit.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.textEdit.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.textEdit.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.textEdit.setAlignment(Qt.AlignJustify)

    def BulletList(self):
        cursor = self.textEdit.textCursor()
        text = cursor.selectedText()
        cursor.insertList(QTextListFormat.ListDecimal)
        cursor.insertText(text)

    def date(self):
        # print(time.strftime("%d/%m/%Y %I:%M:%S"))
        self.textEdit.insertHtml(time.strftime("%d/%m/%Y"))

    def time(self):
        # print(time.strftime("%d/%m/%Y %I:%M:%S"))
        self.textEdit.insertHtml(time.strftime("%I:%M:%p"))

    def help_menu(self):

        self.helpwindow = QtGui.QDialog()
        self.helpwindow.setWindowTitle('Type it....')
        self.helpwindow.setWindowIcon(QtGui.QIcon("icons/text-editor.png"))
        self.helpwindow.setFixedSize(400, 200)
        Lbl = QtGui.QLabel("", self.helpwindow)
        pixmap = QtGui.QPixmap("icons/windows1.jpg")
        MY_Btn = QtGui.QPushButton('quit', self.helpwindow)
        MY_Btn.move(350, 160)
        MY_Btn.resize(30, 30)
        MY_Btn.clicked.connect(self.helpwindow_close)
        Lbl.setPixmap(pixmap)
        self.helpwindow.exec_()

    def helpwindow_close(self):
        self.helpwindow.hide()
        self.helpwindow.exec_()

    def closeEvent(self, event):

        if self.saved_data == self.textEdit.toPlainText():
            event.accept()
        else:
            choice = QtGui.QMessageBox.question(self, 'You have changes!', 'Do you want to quit?',
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if choice == QtGui.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    def exit_fuction(self):
        if self.textEdit.toPlainText() == self.saved_data:
            self.textEdit.setText("")

        else:
            choice = QtGui.QMessageBox.question(self, 'You have changes!', 'Do you want to quit?',
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        sys.exit()


def main():
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet('QMainWindow{background-color: #ffffff;border: 2px solid black;}')
    app.setWindowIcon(QtGui.QIcon('text-editor.png'))
    Gui = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
