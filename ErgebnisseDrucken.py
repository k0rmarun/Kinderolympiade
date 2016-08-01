from datetime import date

from PyQt5.QtWidgets import (QWidget,
                             QFormLayout,
                             QLabel,
                             QComboBox,
                             QPushButton,
                             QProgressBar)
from ErgebnissDrucker import ErgebnissDrucker
from ErgebnissListe import getDisziplin
from UrkundenDrucker import UrkundenDrucker
from Ranking import Ranking
from Ranker import Ranker
from Wert import Wert
from Sportler import Sportler
from QueryTool import QueryTool


class ErgebnisseDrucken(QWidget):
    def __init__(self, parent=None):
        super(ErgebnisseDrucken, self).__init__(parent)

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

    def queryUserData(self,uid:int)->list:
        userData = QueryTool().fetchAllByWhere("LG_NGD_Ergebnisse",UID=uid)
        userData.sort(key=self.disziplinSorter)
        return userData

    def disziplinSorter(self,element:tuple)->int:
        return element[2]

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

        numUsers=0
        curUser=0
        for a in Alter:
            for g in Geschlecht:
                numUsers+=len(self.queryUsers(a,g))
        self.printerProgress.setMaximum(numUsers*2)


        for a in Alter:
            for g in Geschlecht:
                ranker = Ranker(a)
                users = self.queryUsers(a,g)
                self.printerProgress.setValue(0)
                for j in range(len(users)):
                    self.printerProgress.setValue(j)
                    ergebnisse = self.queryUserData(users[j][0])
                    werte = {i:Wert() for i in range(10)}
                    for i in range(len(ergebnisse)):
                        werte[ergebnisse[i][2]]=Wert(*ergebnisse[i][3:6])
                    ranking = Ranking(a, Werte=werte)
                    ranker.append(ranking)
                    users[j]=Sportler(*users[j],Rank=ranking)
                ranker.RankingCalc()
                j=len(users)
                for sportler in users:
                    curUser+=2
                    self.printerProgress.setValue(curUser)
                    ErgebnissDrucker(sportler)
                    UrkundenDrucker(sportler)
                    j+=1
        self.printerProgress.hide()