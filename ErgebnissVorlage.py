from datetime import date

from PyQt5.QtWidgets import (QWidget,
                             QFormLayout,
                             QLabel,
                             QComboBox,
                             QPushButton,
                             QProgressBar)
from ErgebnissVorlagenDrucker import ErgebnissVorlagenDrucker
from QueryTool import QueryTool


class ErgebnissVorlage(QWidget):
    def __init__(self, parent=None):
        super(ErgebnissVorlage, self).__init__(parent)

        self.auswahlAlter = QComboBox()
        self.auswahlAlter.addItem("Bitte auswählen")
        for i in range(3, 18):
            self.auswahlAlter.addItem("{} Jahre / Jahrgang {}".format(i, date.today().year - i))

        self.auswahlGeschlecht = QComboBox()
        self.auswahlGeschlecht.addItem("Bitte auswählen")
        self.auswahlGeschlecht.addItem("Männlich")
        self.auswahlGeschlecht.addItem("Weiblich")

        self.printerProgress = QProgressBar()
        self.printerProgress.hide()

        self.mainLayout = QFormLayout()
        self.mainLayout.addRow(QLabel("Alter:"),self.auswahlAlter)
        self.mainLayout.addRow(QLabel("Geschlecht:"),self.auswahlGeschlecht)
        self.mainLayout.addRow(self.printerProgress)

        self._drucken = QPushButton("Drucken")
        self._drucken.clicked.connect(self.drucken)

        self.mainLayout.addRow(self._drucken)

        self.setLayout(self.mainLayout)

    def queryUsers(self,Alter:int, Geschlecht:bool)->list:
        return QueryTool().fetchAllByWhere("LG_NGD",WieAlt=Alter,Geschlecht=Geschlecht)

    def drucken(self):
        self.printerProgress.show()

        if (self.auswahlAlter.currentIndex() is 0) and (self.auswahlGeschlecht.currentIndex() is 0):
            Alter = range(3,18)
            Geschlecht = range(0,2)
        else:
            Alter = self.auswahlAlter.currentIndex()+2
            Alter = range(Alter,Alter+1)

            Geschlecht = self.auswahlGeschlecht.currentIndex()-1
            Geschlecht = range(Geschlecht,Geschlecht+1)

        self.printerProgress.setMaximum(len(Alter)*len(Geschlecht)*10)
        self.printerProgress.setValue(0)

        prog = 0

        for a in Alter:
            for g in Geschlecht:
                for d in range(10):
                    ErgebnissVorlagenDrucker(a,g,d)
                    self.printerProgress.setValue(prog)
                    prog +=1
        self.printerProgress.hide()
