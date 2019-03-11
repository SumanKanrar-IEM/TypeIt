#-------------------------------------------------
#
# Project created by QtCreator 2014-04-22T18:25:49
#
#-------------------------------------------------

QT       += core gui webkit webkitwidgets

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = pdftest
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    webview.cpp

HEADERS  += mainwindow.h \
    webview.h

FORMS    += mainwindow.ui

RESOURCES += \
    resource.qrc
