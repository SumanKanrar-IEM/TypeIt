#ifndef WEBVIEW_H
#define WEBVIEW_H

#include <QWebView>
#include <QWebPage>
#include <QNetworkAccessManager>
#include <QDebug>

class WebView : public QWebView
{
    Q_OBJECT
public:
    explicit WebView(QWidget *parent = 0);

signals:

public slots:
    void onLoadFinish(bool);
};

class WebPage : public QWebPage {
    Q_OBJECT

public:
    explicit WebPage(QWidget *parent = 0)
        : QWebPage(parent) {
    }

public slots:
    bool shouldInterruptJavaScript() {
        return false;
    }

public:
    virtual void javaScriptConsoleMessage(const QString & message, int /*lineNumber*/, const QString & /*sourceID*/) {
        qDebug() << message;
    }
};

#endif // WEBVIEW_H
