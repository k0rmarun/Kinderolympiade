from datetime import date

from PyQt5.QtWidgets import(QWidget,
                            QGridLayout,
                            QLabel,
                            QComboBox,
                            QPushButton,
                            QDoubleSpinBox,
                            QMessageBox)

from QueryTool import QueryTool

einheiten =   ("sec",   "sec",   "sec",   "min", "m",   "m",   "cm,V","m",     "m",   "m")
felderzahl=   (1,       1,       1,       1,     3,     3,     3,      3,      3,     3)  #Anzahl

def getDisziplin(alter:int)->str:
    if alter < 12:
        yield "50m Sprint"
        yield "60m Hürdenlauf"
    elif alter < 14:
        yield "75m Sprint"
        yield "80m Hürdenlauf"
    else:
        yield "100m Sprint"
        yield "80m Hürdenlauf"

    if alter < 10:
        yield "-"
    else:
        yield "200m Lauf"

    if alter < 10:
        yield "400m Lauf"
    else:
        yield "800m Lauf"

    yield "Weitsprung"
    yield "Stabweitsprung"
    if alter < 10:
        yield "-"
    else:
        yield "Hochsprung"
    yield "Reifenweitwurf"
    yield "Weitwurf"
    yield "Kugelstoßen"

class ErgebnissListe(QWidget):
    template = "<tr><td>Eintrag von </td><td>{: >20}</td><td>in der Disziplin {:<15} </td><td>{}erfolgreich {}</td></tr>"
    def __init__(self,parent=None):
        super(ErgebnissListe, self).__init__(parent)

        self.auswahlAlter = QComboBox()
        self.auswahlAlter.addItem("Bitte auswählen")
        for i in range(3,18):
            self.auswahlAlter.addItem("{} Jahre / Jahrgang {}".format(i, date.today().year-i))
        self.auswahlAlter.activated.connect(self.auswahlKlasse)
        self.auswahlAlter.activated.connect(self.waehleDisziplinen)

        self.auswahlGeschlecht = QComboBox()
        self.auswahlGeschlecht.addItem("Bitte auswählen")
        self.auswahlGeschlecht.addItem("Männlich")
        self.auswahlGeschlecht.addItem("Weiblich")
        self.auswahlGeschlecht.activated.connect(self.auswahlKlasse)
        self.auswahlGeschlecht.activated.connect(self.waehleDisziplinen)

        self.auswahlDisziplin = QComboBox()
        self.auswahlDisziplin.addItem("Bitte auswählen")
        for i in getDisziplin(10):
            self.auswahlDisziplin.addItem(i)
        self.auswahlDisziplin.activated.connect(self.auswahlKlasse)

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(QLabel("Alter:"), 0, 0)
        self.mainLayout.addWidget(self.auswahlAlter, 0, 1, 1, 3)
        self.mainLayout.addWidget(QLabel("Geschlecht:"), 1, 0)
        self.mainLayout.addWidget(self.auswahlGeschlecht, 1, 1, 1, 3)
        self.mainLayout.addWidget(QLabel("Disziplin:"), 2, 0)
        self.mainLayout.addWidget(self.auswahlDisziplin, 2, 1, 1, 3)

        self._speichern = QPushButton("Speichern")
        self._speichern.clicked.connect(self.speichern)

        self.setLayout(self.mainLayout)

        self._sportler = []

        self.update()

    def waehleDisziplinen(self):
        self.auswahlDisziplin.clear()
        self.auswahlDisziplin.addItem("Bitte auswählen")
        for i in getDisziplin(self.auswahlAlter.currentIndex()+2):
            self.auswahlDisziplin.addItem(i)


    def auswahlKlasse(self):
        if self.auswahlAlter.currentIndex() == 0:
            return False
        elif self.auswahlGeschlecht.currentIndex() == 0:
            return False
        elif self.auswahlDisziplin.currentIndex() == 0:
            return False

        self.clearAuswahl()

        disziplin = self.auswahlDisziplin.currentIndex()-1
        if self.auswahlDisziplin.currentText() is "-":
            return

        for sportler in QueryTool().queryAndFetch("SELECT ID, Name, Vorname FROM LG_NGD WHERE WieAlt = ? AND Geschlecht = ?",
                                                 self.auswahlAlter.currentIndex()+2,
                                                 bool(self.auswahlGeschlecht.currentIndex()-1)):
            self._sportler += [sportler[0]]
            name = "{} {}".format(sportler[2],sportler[1])
            #UID, Name

            for werte in reversed(QueryTool().queryAndFetch("SELECT Wert1, Wert2, Wert3 FROM LG_NGD_Ergebnisse WHERE UID = ? "
                                                   "AND Typ = ? UNION SELECT 0, 0, 0",
                                                   sportler[0],
                                                   disziplin)):

                row = self.mainLayout.rowCount()

                self.mainLayout.addWidget(QLabel(name), row, 0)
                for i in range(0,felderzahl[disziplin]):
                    el = QDoubleSpinBox()
                    el.setMaximum(99999)
                    el.setValue(werte[i])
                    el.setSuffix(" "+einheiten[disziplin])
                    el.setSingleStep(0.01)
                    self.mainLayout.addWidget(el, row, i+1, 1, 3/felderzahl[disziplin])
                break
        self._speichern = QPushButton("Speichern")
        self._speichern.clicked.connect(self.speichern)
        self.mainLayout.addWidget(self._speichern, self.mainLayout.rowCount(), 0, 1, 4)

    def speichern(self):
        row = self.mainLayout.rowCount()-len(self._sportler)-1
        disziplin = self.auswahlDisziplin.currentIndex()-1

        ausgabe = "<table>"

        for UID in self._sportler:
            werte = ["0","0","0"]
            for col in range(1, 1+felderzahl[disziplin]):
                item = self.mainLayout.itemAtPosition(row, col)
                text = "0"
                try:
                    if type(item.widget()) is not type(QDoubleSpinBox()):
                        raise TypeError("No LineEdit")
                    text = item.widget().value()
                except TypeError:
                    text = "0"
                except AttributeError:
                    text = "0"
                werte[col-1]=text

            data = QueryTool().queryAndFetch("SELECT * FROM LG_NGD_Ergebnisse WHERE UID = ? AND Typ = ?",UID,disziplin)
            ergebnisse = None
            typ = None
            if len(data) is not 0:
                ergebniss = QueryTool().update("LG_NGD_Ergebnisse", data[0][0], Wert1=werte[0], Wert2=werte[1], Wert3=werte[2])
                typ = "aktualisiert"
            else:
                ergebniss = QueryTool().insert("LG_NGD_Ergebnisse", UID=UID, Typ=disziplin, Wert1=werte[0], Wert2=werte[1], Wert3=werte[2])
                typ = "eingetragen"

            username = self.mainLayout.itemAtPosition(row, 0)

            if type(username.widget()) is not type(QLabel()):
                username = ""
            else:
                username = username.widget().text()
            ausgabe += self.template.format(username, list(getDisziplin(self.auswahlAlter.currentIndex()+2))[disziplin],
                                            "nicht " if ergebniss is None else "", typ)

            row += 1
        ausgabe += "</table>"
        QMessageBox.information(self, "Eintragungsstatus", ausgabe)

    def clearAuswahl(self):
        for w in self.iterWidgets(True):
            w[0].setParent(None)
        self._sportler=[]

    def iterWidgets(self,allWidgets = False)->QWidget:
        for row in range(3, self.mainLayout.rowCount()-(1 if not allWidgets else 0)):
            for col in range(self.mainLayout.columnCount()):
                item = self.mainLayout.itemAtPosition(row, col)
                if item is not None and item.widget() is not None:
                    yield (item.widget(), row, col)
                else:
                    break

    def update(self):
        if not self.auswahlKlasse():
            return