var PDFViewer;
(function(global) {
  'use strict';
  PDFViewer = {};

  PDFViewer.isUndefined = function(value) {
    return typeof value === 'undefined';
  };

  PDFViewer.proxy = function(targetFunction, context) {
    return $.proxy(targetFunction, context);
  };

  PDFViewer.css = function(element, key, value) {
    if (PDFViewer.isUndefined(value)) {
      return $(element).css(key);
    } else {
      // workaround for applying '!important' directive.
      if (typeof value === 'string' && value.indexOf('!important') != -1) {
        $(element).css(key, '');
        var original = $(element).attr('style');
        $(element).attr('style', original + key + ':' + value + ";");
      } else {
        $(element).css(key, value);
      }
    }
  };

  PDFViewer.appendChild = function(element, tag, id, cls) {
    var child = document.createElement(tag);
    if (!PDFViewer.isUndefined(id)) {
      child.setAttribute('id', id);
    }
    if (!PDFViewer.isUndefined(cls)) {
      child.setAttribute('class', cls);
    }
    return element.appendChild(child);
  };

  if (global) {
    global.PDFViewer = PDFViewer;
  }
})(this);

PDFViewer.TAG_CONTENTS = 'ul';
PDFViewer.TAG_CHAPTER = 'li';
PDFViewer.ID_STYLES = 'book-viewer-style';
PDFViewer.ID_CONTENTS = 'book-viewer-contents';
PDFViewer.ID_CHAPTER = 'book-viewer-chapter';
PDFViewer.ID_BOOKVIEWER = 'book-viewer';
PDFViewer.ID_CANVAS_PREFIX = 'pdf-canvas-';

function BookViewer() {
  this.element = document.getElementById(PDFViewer.ID_BOOKVIEWER);
  this.contents = PDFViewer.appendChild(this.element, PDFViewer.TAG_CONTENTS, PDFViewer.ID_CONTENTS);
  this.styleElement = PDFViewer.appendChild(document.head, 'style', PDFViewer.ID_STYLES);

  this.pageSizeCover_ = { 'width': undefined, 'height': undefined };
  this.pageSizeOther_ = { 'width': undefined, 'height': undefined };

  this.processTimer = undefined;
  this.processIndex = [];

  this.load();
}

(function() {
  'use strict';
  BookViewer.prototype.load = function() {
    var loadFinishCount = 0;
    var that = this;
    function onPageLoad(page) {
      that.pageArray[page.pageInfo.pageIndex] = page;
      if (page.pageInfo.pageIndex === 0) {
        that.pageSizeCover_.width = page.pageInfo.view[2] - page.pageInfo.view[0];
        that.pageSizeCover_.height = page.pageInfo.view[3] - page.pageInfo.view[1];
      } else if (page.pageInfo.pageIndex === 1) {
        that.pageSizeOther_.width = page.pageInfo.view[2] - page.pageInfo.view[0];
        that.pageSizeOther_.height = page.pageInfo.view[3] - page.pageInfo.view[1];
      }

      loadFinishCount++;
      if (loadFinishCount === that.pdfdocument.numPages) {
        that.startRenderingFrom(1, 1);
      }
    }

    console.log('VIEWER start loading.');
    this.dirtyFlag_ = false;

    var data = './compressed.tracemonkey-pldi-09.pdf';

    PDFJS.getDocument(data).then(function(pdf) {
      that.pdfdocument = pdf;
      that.pageArray = new Array(that.pdfdocument.numPages);
      that.renderTask = null;
      that.setCanvasSize();

      for (var pageIndex = 1; pageIndex <= that.pdfdocument.numPages; pageIndex++) {
        that.pdfdocument.getPage(pageIndex).then(onPageLoad);
      }
    });
  };

  BookViewer.prototype.startRenderingFrom = function(pageNumber) {
    clearTimeout(this.processTimer);
    this.processIndex.length = 0;
    this.processOrigin_ = pageNumber;
    this.processIndex.push(pageNumber);

    this.renderFunction();
  };

  BookViewer.prototype.renderFunction = function() {
    var that = this;
    function calcNextPage(currentPage) {
      var tempPage = currentPage + 1;
      if (tempPage === 0) {
        tempPage = that.pdfdocument.numPages;
      } else if (tempPage === that.pdfdocument.numPages + 1) {
        tempPage = 1;
      }
      return tempPage;
    }

    if (this.processIndex > 1) {
      this.processIndex.length = 1;
    }

    var pageNumber = this.processIndex.pop();
    if (PDFViewer.isUndefined(pageNumber)) {
      return;
    }

    var nextPageNumber = calcNextPage(pageNumber);
    this.processIndex.length = 0;
    this.processIndex.push(nextPageNumber);

    var setNextRender = function() {
      if (that.processIndex > 0 && that.processIndex[0] !== nextPageNumber) {
        return;
      }

      var nextPage = that.processIndex.pop();

      if (!PDFViewer.isUndefined(nextPage) && nextPage !== that.processOrigin_) {
        that.processIndex.push(nextPage);
        clearTimeout(that.processTimer);
        that.processTimer = setTimeout(PDFViewer.proxy(that.renderFunction, that), 10);
      }
    };

    if (PDFViewer.isUndefined(pageNumber) || pageNumber > that.pdfdocument.numPages) {
      return;
    }

    var thisChapter = document.getElementById(PDFViewer.ID_CHAPTER + '-' + pageNumber);

    var page = this.pageArray[pageNumber-1];
    this.processPage(page, function() {
      setNextRender();
    });
  };

  BookViewer.prototype.processPage = function(page, renderCallbackFunc) {
    var contentsElement = document.getElementById(PDFViewer.ID_CONTENTS);
    var pagenum = (page.pageInfo.pageIndex + 1);
    var thisChapter = document.getElementById(PDFViewer.ID_CHAPTER + '-' + pagenum);

    var canvasSize = this.getCanvasSize();
    var pageSize = (page.pageInfo.pageIndex === 0)? this.pageSizeCover_:this.pageSizeOther_;
    var scaleH = canvasSize.width / pageSize.width;
    var scaleV = canvasSize.height / pageSize.height;
    var scale = Math.min(scaleH, scaleV);

    var viewport = page.getViewport(scale);
    var canvas = document.getElementById(PDFViewer.ID_CANVAS_PREFIX + pagenum);
    canvas.width = canvasSize.width;
    canvas.height = canvasSize.height;

    PDFViewer.css(this.contents, 'height', thisChapter.clientHeight * this.pdfdocument.numPages);

    thisChapter.setAttribute('align','center');

    var context = canvas.getContext('2d');
    var renderContext = {
      canvasContext: context,
      viewport: viewport
    };
    var renderTask = page.render(renderContext);
    renderTask.promise.then(function() {
        renderCallbackFunc();
    },
    function(error) {
      console.warn(error + ' ' + thisChapter.id);
    });
  };

  BookViewer.prototype.getCanvasSize = function() {
    var contentsElement = document.getElementById(PDFViewer.ID_CONTENTS);
    var scaleH = contentsElement.clientWidth  / this.pageSizeOther_.width;
    var scaleV = contentsElement.clientHeight / this.pageSizeOther_.height;
    var scale = Math.min(scaleH, scaleV);

    var otherPageScale = contentsElement.clientWidth / this.pageSizeOther_.width;
    var otherCanvasHeight = Math.floor(this.pageSizeOther_.height * otherPageScale);
    var coverPageScale = contentsElement.clientWidth / this.pageSizeCover_.width;
    if (this.pageSizeCover_.height * coverPageScale > otherCanvasHeight) {
      scale = otherCanvasHeight / this.pageSizeCover_.height;
    } else {
      scale = otherPageScale;
    }

    var canvasWidth = Math.floor(this.pageSizeOther_.width * scale);
    var canvasHeight = Math.floor(this.pageSizeOther_.height * scale);
    var returnSize = { 'width': canvasWidth, 'height': canvasHeight };
    return returnSize;
  };

  BookViewer.prototype.setCanvasSize = function(nocreate) {
    if (PDFViewer.isUndefined(this.pdfdocument)) {
        return;
    }

    this.contents.height = window.innerHeight;

    var canvasSize = this.getCanvasSize();
    for (var ind = 1; ind <= this.pdfdocument.numPages; ind++) {
      var thisChapter = document.getElementById(PDFViewer.ID_CHAPTER + '-' + ind);
      if (!PDFViewer.isUndefined(nocreate) && thisChapter === null) {
        continue;
      }
      if (thisChapter === null) {
        PDFViewer.appendChild(this.contents, PDFViewer.TAG_CHAPTER, PDFViewer.ID_CHAPTER + '-' + ind);
        thisChapter = document.getElementById(PDFViewer.ID_CHAPTER + '-' + ind);
      }

      var canvas = document.getElementById(PDFViewer.ID_CANVAS_PREFIX + ind);
      if (canvas === null) {
        canvas = document.createElement('canvas');
        canvas.id = PDFViewer.ID_CANVAS_PREFIX + ind;
        thisChapter.appendChild(canvas);
      }

      canvas.width = canvasSize.width;
      canvas.height = canvasSize.height;
    }
  };
})();
