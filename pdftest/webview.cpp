#include "webview.h"
#include <QNetworkReply>
#include <QWebSettings>
#include <QWebFrame>

static const QString WEB_VIEWER_PATH = "qrc:/res/res/pdf-viewer.html";

WebView::WebView(QWidget *parent) :
    QWebView(parent)
{
    QWebSettings* settings = QWebSettings::globalSettings();
    settings->setAttribute(QWebSettings::LocalContentCanAccessFileUrls, true);
    settings->setAttribute(QWebSettings::LocalContentCanAccessRemoteUrls, true);
    settings->setAttribute(QWebSettings::DeveloperExtrasEnabled, true);

    QNetworkAccessManager *nam = new QNetworkAccessManager();
    WebPage *page = new WebPage(this);
    page->setNetworkAccessManager(nam);
    setPage(page);

    connect(this, &QWebView::loadFinished, this, &WebView::onLoadFinish);

    setUrl(QUrl(WEB_VIEWER_PATH));
}

void WebView::onLoadFinish(bool success) {
    qDebug() << (success?"success":"fail");
    if (success) {
        page()->mainFrame()->evaluateJavaScript("init();");
    }
}
