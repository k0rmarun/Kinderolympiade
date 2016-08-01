import os
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QImage, QFontMetrics
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtPrintSupport import QPrinter


class LGPdfWriter(QPrinter):
    def __init__(self, name: str):
        super(LGPdfWriter, self).__init__()
        if not self.touch(name):
            raise PermissionError("Cannot open "+name)

        self.setOutputFileName(name)
        self.setOutputFormat(self.PdfFormat)
        self.setPageSize(self.A4)

        #self.setPageSizeMM(QSizeF(2100,2970))
        self._rot = QPen(QColor.red)
        self._blau = QPen(QColor.blue)
        self._grün = QPen(QColor.green)
        self._schwarz = QPen(QColor.black)
        self._weis = QPen(QColor(255, 255, 255))
        self._fg = self._schwarz
        self._fg.setWidth(3)
        self._bg = QPen(QColor.black)
        self._bg.setWidth(3)
        self._fgs = QPen(QColor(190, 190, 190))
        self._fgs.setWidth(3)
        self._sg = QColor(180, 20, 51)

        self._painter = QPainter(self)
        self._painter.setBackground(QColor(255, 255, 255))

        self._font = QFont("Arial", 20, QFont.Bold, True)

        #bordersize = 20/40mm

    def touch(self,filename)->bool:
        basedir = os.path.dirname(filename)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        try:
            with open(filename, 'a'):
                os.utime(filename, None)
        except PermissionError as e:
            entscheidung = QMessageBox.question(None,
                                                "Keine Schreibberechtigung","Keine Schreibberechtigung für Datei <br><b>{}</b><br>Bitte die Datei schließen und dann fortfahren.<br><b>Fortfahren?</b>".format(filename),
                                                QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            if entscheidung == QMessageBox.Yes:
                return self.touch(filename)
            else:
                return False
        else:
            return True

    def line(self, start: QPointF, ende: QPointF, shaded: int=0) -> None:
        if shaded:
            diff = 2 if isinstance(shaded,bool) and shaded == True else shaded
            self._painter.setPen(self._fgs)
            self._painter.drawLine(start + diff, ende + diff)
        self._painter.setPen(self._fg)
        self._painter.drawLine(start, ende)


    def rect(self, rect: QRectF, shaded: int=0) -> None:
        if shaded:
            diff = 6 if isinstance(shaded,bool) and shaded == True else shaded
            self._painter.setPen(self._fgs)
            rect.translate(diff, diff)
            self._painter.drawRect(rect)
            rect.translate(-diff, -diff)

        self._painter.setPen(self._bg)
        self._painter.drawRect(rect)

    def text(self, text: str, pos: QRectF, color: QColor=None, size: int=20, shaded: int=0,
             bold: bool=False,shrinkToFit=10) -> None:
        if not isinstance(text,str):
            text = "{}".format(text)

        self._font.setPointSize(size)
        if bold:
            self._font.setWeight(QFont.Black)
        else:
            self._font.setWeight(QFont.Bold)
        self._painter.setFont(self._font)

        fm = QFontMetrics(self._font)
        if pos.width() == 0:
            pos.setWidth(fm.width(text))
        if pos.height() == 0:
            pos.setHeight(fm.height())

        if size > shrinkToFit:
            #
            if fm.width(text) > pos.width() or fm.height() > pos.height()+2:
                self.text(text,pos,color,size-1,shaded,bold,shrinkToFit)
                return

        if shaded:
            diff = size//4 if isinstance(shaded,bool) and shaded == True else shaded
            self._painter.setPen(self._fgs)
            pos2 = pos.translated(diff, diff)
            self._painter.drawText(pos2, Qt.AlignCenter, text)
        p = QPen(color if color is not None else self._fg)
        self._painter.setPen(p)
        self._painter.drawText(pos, Qt.AlignCenter, text)

    def image(self, img: str, pos: QRectF, shaded: int=0):
        img = QImage(img)
        imgSize = QRectF(0, 0, img.width(), img.height())

        if shaded:
            diff = 10 if isinstance(shaded,bool) and shaded == True else shaded
            pos2 = pos.translated(diff,diff)
            self._painter.drawImage(pos2, img, imgSize, Qt.MonoOnly)
        self._painter.drawImage(pos, img)

    def table(self,
              rect: QRectF,
              lineData: list=None,
              columnCount: int=0,
              rowCount:int=0,
              w: dict=None,
              h: dict=None,
              size:int=18,
              border:bool=True) -> None:
        #lineData: [{x:1,y:2,text:"hallo"}...]
        #    oder  [{x:[1,3],y:[2,4],text."hallo"}..]

        for id in range(len(lineData)):
            if not isinstance(lineData[id], dict):
                lineData[id] = {"text": "{}".format(lineData[id])}

        if w is None:
            w = dict()
        if h is None:
            h = dict()


        #Berechne Reservierte Größen
        reserved = {"w": 0, "h": 0}

        for wr in w.values():
            reserved["w"] += wr
        for hr in h.values():
            reserved["h"] += hr

        #Berechne Zellengrößen
        marginX = 5
        marginY = 5

        remCol = columnCount - len(w)
        remRow = rowCount - len(h)

        regularWidth = (rect.width() - reserved["w"] - (columnCount + 1) * marginX) / remCol
        regularHeight = (rect.height() - reserved["h"] - (rowCount + 1) * marginY) / remRow

        def calcCellUsage() -> list:
            index = 0
            pos = []

            for column in range(columnCount):
                l = list()
                for row in range(rowCount):
                    l.append(None)
                pos.append(l)

            curX = 0
            curY = 0
            for i in lineData:
                if "x" in i.keys():
                    x = i["x"]
                    if isinstance(x, int):
                        x = range(x, x + 1)
                    elif isinstance(x, tuple):
                        x = range(x[0], x[-1] + 1)
                else:
                    x = range(curX, curX + 1)
                    i["x"] = x

                if "y" in i.keys():
                    y = i["y"]
                    if isinstance(y, int):
                        y = range(y, y + 1)
                    elif isinstance(y, tuple):
                        x = range(y[0], y[-1] + 1)
                else:
                    y = range(curY, curY + 1)

                    i["y"] = y

                curX = x[-1] + 1
                curY = y[-1]

                if curX >= columnCount:
                    curX = 0
                    curY += 1

                for xx in x:
                    for yy in y:
                        pos[xx][yy] = index
                index += 1
            return pos

        def calcWidth(col:int) -> float:
            try:
                if col in w.keys():
                    return w[col]
            except IndexError:
                pass
            return regularWidth

        def calcHeight(row:int) -> float:
            try:
                if row in h.keys():
                    return h[row]
            except IndexError:
                pass
            return regularHeight

        def calcCellSize(col:int, row: int) -> tuple:
            if col >= columnCount:
                raise IndexError
            if row >= rowCount:
                raise IndexError
            if pos[col][row] is None:
                raise IndexError

            width = calcWidth(col)
            height = calcHeight(row)

            id = pos[col][row]
            try:
                if pos[col + 1][row] is id:
                    width += calcCellSize(col + 1, row)[0] + marginX
            except IndexError:
                pass

            try:
                if pos[col][row + 1] is id:
                    height += calcCellSize(col, row + 1)[1] + marginY
            except IndexError:
                pass
            return width, height

        def calcCumulativeWidth(col: int) -> float:
            if col is 0:
                return marginX
            x = calcWidth(col - 1) + marginX + calcCumulativeWidth(col - 1)
            return x

        def calcCumulativeHeight(row: int) -> float:
            if row is 0:
                return marginY
            return calcHeight(row - 1) + marginY + calcCumulativeHeight(row - 1)

        def calcCell(index: int) -> tuple:
            x = lineData[index]["x"]
            if not isinstance(x, int):
                x = x[0]
            y = lineData[index]["y"]
            if not isinstance(y, int):
                y = y[0]

            left = rect.left() + calcCumulativeWidth(x)
            top = rect.top() + calcCumulativeHeight(y)

            d = calcCellSize(x, y)

            return left, top, d[0], d[1]

        def getFontOptions(index: int) -> dict:
            data = {
                "size": size,
                "color": self._fg,
                "shaded": False,
                "bold": False
            }

            elem = lineData[index]

            if "size" in elem.keys():
                data["size"] = elem["size"]
            if "color" in elem.keys():
                data["color"] = elem["color"]
            if "shaded" in elem.keys():
                data["shaded"] = elem["shaded"]
            if "bold" in elem.keys():
                data["bold"] = elem["bold"]
            return data

        if border:
            self.rect(rect, False)

        pos = calcCellUsage()

        for elem in range(len(lineData)):
            r = QRectF(*calcCell(elem))
            if border:
                self.rect(r, False)
            self.text(lineData[elem]["text"], r, **getFontOptions(elem))

    def end(self):
        self._painter.end()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()