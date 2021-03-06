namespace Poppler {

class Document {
%TypeHeaderCode
#include <qt4/poppler-qt4.h>
%End

public:
%If(POPPLER_V0_22_0 -)
    enum FormType {
        NoForm,
        AcroForm,
        XfaForm,
    };
%End
    enum PageMode {
        UseNone,
        UseOutlines,
        UseThumbs,
        FullScreen,
        UseOC,
        UseAttach,
    };
    enum PageLayout {
        NoLayout,
        SinglePage,
        OneColumn,
        TwoColumnLeft,
        TwoColumnRight,
        TwoPageLeft,
        TwoPageRight,
    };
    enum RenderBackend {
        SplashBackend,
        ArthurBackend,
    };
    enum RenderHint {
        Antialiasing = 0x00000001,
        TextAntialiasing = 0x00000002,
%If(POPPLER_V0_12_1 -)
        TextHinting = 0x00000004,
%End
%If(POPPLER_V0_18_0 -)
        TextSlightHinting = 0x00000008,
%End
%If(POPPLER_V0_22_0 -)
        OverprintPreview = 0x00000010,
%End
%If(POPPLER_V0_24_0 -)
        ThinLineSolid = 0x00000020,
        ThinLineShape = 0x00000040,
%End
    };
    typedef QFlags<Poppler::Document::RenderHint> RenderHints;
    
    void setColorDisplayProfile(void *outputProfileA);
    void setColorDisplayProfileName(const QString &name);
    void* colorRgbProfile() const;
    void* colorDisplayProfile() const;
    static Poppler::Document *load(const QString & filePath,
                            const QByteArray &ownerPassword=QByteArray(),
                            const QByteArray &userPassword=QByteArray()) /Factory, ReleaseGIL/;
    static Poppler::Document *loadFromData(const QByteArray &fileContents,
                            const QByteArray &ownerPassword=QByteArray(),
                            const QByteArray &userPassword=QByteArray()) /Factory, ReleaseGIL/;
    Poppler::Page *page(int index) const /Factory/;
    Poppler::Page *page(const QString &label) const /Factory/;
    int numPages() const;
    PageMode pageMode() const;
    PageLayout pageLayout() const;
    bool unlock(const QByteArray &ownerPassword, const QByteArray &userPassword);
    bool isLocked() const;
    QDateTime date( const QString & data ) const;
    QString info( const QString & data ) const;
    QStringList infoKeys() const;
    bool isEncrypted() const;
    bool isLinearized() const;
    bool okToPrint() const;
    bool okToPrintHighRes() const;
    bool okToChange() const;
    bool okToCopy() const;
    bool okToAddNotes() const;
    bool okToFillForm() const;
    bool okToCreateFormFields() const;
    bool okToExtractForAccessibility() const;
    bool okToAssemble() const;
%If(POPPLER_V0_16_0 -)
    bool getPdfId(QByteArray *permanentId, QByteArray *updateId) const;
%End
    void getPdfVersion(int *major, int *minor) const;
    QList<Poppler::FontInfo> fonts() const /ReleaseGIL/;
%If(POPPLER_V0_22_0 -)
    FormType formType() const;
%End
    Poppler::FontIterator* newFontIterator( int startPage = 0 ) const /Factory/;
    QByteArray fontData(const Poppler::FontInfo &font) const;
    QList<Poppler::EmbeddedFile*> embeddedFiles() const;
    bool hasEmbeddedFiles() const;
    QDomDocument *toc() const;
    Poppler::LinkDestination *linkDestination( const QString &name ) /Factory, ReleaseGIL/;
    void setPaperColor(const QColor &color);
    QColor paperColor() const;
    void setRenderBackend( RenderBackend backend );
    RenderBackend renderBackend() const;
    static QSet<Poppler::Document::RenderBackend> availableRenderBackends();
    void setRenderHint( RenderHint hint, bool on = true );
    RenderHints renderHints() const;
    Poppler::PSConverter *psConverter() const /Factory/;
    Poppler::PDFConverter *pdfConverter() const /Factory/;
    QString metadata() const;
    bool hasOptionalContent() const;
    Poppler::OptContentModel *optionalContentModel() /Factory/;
    QStringList scripts() const;
private:
    Document();
    Document(const Poppler::Document &);
        
}; // class Document

}; // namespace Poppler
