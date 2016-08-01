from datetime import date

from PyQt5.QtWidgets import(QWidget,
                            QComboBox,
                            QStackedLayout,
                            QVBoxLayout,
                            QApplication)

from SportlerEdit import SportlerEdit
from SportlerShow import SportlerShow
from ErgebnissListe import ErgebnissListe
from ErgebnisseDrucken import ErgebnisseDrucken
from ErgebnissVorlage import ErgebnissVorlage


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.actionAuswahl = QComboBox()
        self.actionAuswahl.addItem("Einen Sportler bearbeiten")
        self.actionAuswahl.addItem("Liste aller Sportler anzeigen")
        self.actionAuswahl.addItem("Eine Ergebnissliste bearbeiten")
        self.actionAuswahl.addItem("Ergebnisse & Urkunden drucken")
        self.actionAuswahl.addItem("Ergebnissvorlagen drucken")
        self.actionAuswahl.setEditable(False)
        self.actionAuswahl.activated.connect(self.setAction)

        self.actionSportlerEdit = SportlerEdit()
        self.actionSportlerShow = SportlerShow()
        self.actionErgebnissListe = ErgebnissListe()
        self.actionErgebnisseDrucken = ErgebnisseDrucken()
        self.actionErgebnissVorlage = ErgebnissVorlage()

        self.actionLayout = QStackedLayout()
        self.actionLayout.addWidget(self.actionSportlerEdit)
        self.actionLayout.addWidget(self.actionSportlerShow)
        self.actionLayout.addWidget(self.actionErgebnissListe)
        self.actionLayout.addWidget(self.actionErgebnisseDrucken)
        self.actionLayout.addWidget(self.actionErgebnissVorlage)


        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.actionAuswahl)
        self.mainLayout.addStretch(0)
        self.mainLayout.addLayout(self.actionLayout)
        self.mainLayout.addStretch(0)

        self.setLayout(self.mainLayout)
        self.show()

    def setAction(self,index):
        self.actionLayout.setCurrentIndex(index)
        self.actionLayout.currentWidget().update()


if __name__ == '__main__':

    import os
    if not os.path.isfile("daten.db"):
        os.system("sqlite3 daten.db < setup.sql")

    import sys

    app = QApplication(sys.argv)

    import TestPackage

    Window = MainWindow()
    Window.setWindowTitle("Kinderolympiade {}".format(date.today().year))
    Window.resize(640, 480)
    Window.show()

    sys.exit(app.exec_())
