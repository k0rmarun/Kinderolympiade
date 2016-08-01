from datetime import date

from PyQt5.QtWidgets import(QWidget,
                            QComboBox,
                            QPushButton,
                            QLabel,
                            QMessageBox,
                            QFormLayout )

from QueryTool import QueryTool


class SportlerEdit(QWidget):
    def __init__(self,parent=None):
        super(SportlerEdit, self).__init__(parent)

        self.sportlerAusDatenbank = False

        self.sportlerID = QLabel()
        self.sportlerID.setText("{}".format(QueryTool().numEntryInTable("LG_NGD")))

        self.sportlerName = QComboBox()
        self.sportlerName.activated.connect(self.loadUserByName)
        self.sportlerName.setEditable(True)
        self.sportlerName.setInsertPolicy(self.sportlerName.InsertAlphabetically)
        self.sportlerName.setMinimumWidth(200)
        self.sportlerVName = QComboBox()
        self.sportlerVName.activated.connect(self.loadUserByVName)
        self.sportlerVName.setEditable(True)
        self.sportlerVName.setInsertPolicy(self.sportlerVName.InsertAlphabetically)
        self.sportlerVName.setMinimumWidth(200)
        self.sportlerAlter = QComboBox()
        self.sportlerAlter.addItem("Bitte auswählen")

        today = date.today()

        for i in range(3,18):
            self.sportlerAlter.addItem("{} Jahre / Jahrgang {}".format(i,today.year - i))
        self.sportlerAlter.setEditable(False)

        self.sportlerGeschlecht = QComboBox()
        self.sportlerGeschlecht.addItem("Bitte auswählen")
        self.sportlerGeschlecht.addItem("Männlich")
        self.sportlerGeschlecht.addItem("Weiblich")

        self.sportlerSubmit = QPushButton("&Speichern")
        self.sportlerSubmit.clicked.connect(self.saveUser)
        self.sportlerSubmit.setToolTip("Save user to database")
        self.sportlerLoad = QPushButton("&Zurücksetzen")
        self.sportlerLoad.clicked.connect(self.clearUser)
        self.sportlerLoad.setToolTip("Clear Preview")


        self.sportlerLayout=QFormLayout()
        self.sportlerLayout.addRow(QLabel("ID:"),self.sportlerID)
        self.sportlerLayout.addRow(QLabel("Name:"),self.sportlerName)
        self.sportlerLayout.addRow(QLabel("Vorname:"),self.sportlerVName)
        self.sportlerLayout.addRow(QLabel("Alter:"),self.sportlerAlter)
        self.sportlerLayout.addRow(QLabel("Geschlecht:"),self.sportlerGeschlecht)
        self.sportlerLayout.addRow(self.sportlerLoad,self.sportlerSubmit)

        self.setLayout(self.sportlerLayout)
        self.getUserData()

    def update(self):
        self.clearUser()
        self.getUserData()
        self.sportlerName.setFocus()

    def saveUser(self):
        data = {"Name":self.sportlerName.currentText(),
                "Vorname":self.sportlerVName.currentText(),
                "WieAlt":self.sportlerAlter.currentIndex()+2,
                "Geschlecht":bool(self.sportlerGeschlecht.currentIndex()-1)}

        try:
            if self.sportlerAusDatenbank:
                QueryTool().update("LG_NGD",self.sportlerID.text(), **data)
            elif not self.sportlerAusDatenbank:
                QueryTool().insert("LG_NGD",**data)
        except:
            raise
        else:
            if(self.sportlerAusDatenbank):
                QMessageBox.information(self,"Erfolgreich aktualisiert","Aktualisiern des Datenbankeintrages war erfolgreich")
            else:
                QMessageBox.information(self,"Erfolgreich eingetragen","Eintrag in die Datenbank einfolgreich")
            self.update()


    def clearUser(self):
        self.sportlerID.setText("{}".format(QueryTool().numEntryInTable("LG_NGD")))
        self.sportlerName.setEditText("")
        self.sportlerVName.setEditText("")
        self.sportlerAlter.setCurrentIndex(0)
        self.sportlerGeschlecht.setCurrentIndex(0)
        self.sportlerAusDatenbank = False

    def loadUserByName(self):
        """
        Do not query for sporter if form already partially filled
        """
        if not self.sportlerVName.currentText():
            self.loadUser(self.sportlerName)

    def loadUserByVName(self):
        """
        Do not query for sporter if form already partially filled
        """
        if not self.sportlerName.currentText():
            self.loadUser(self.sportlerVName)

    def loadUser(self,elem:QComboBox):
        user = elem.currentText()
        userdata = user.split()
        if len(userdata) > 2:
            last = userdata[-1]
            userdata = [" ".join(userdata[:-1]), last]

        user = QueryTool().queryByNames(userdata[0], userdata[1])

        print(user)
        self.sportlerID.setText("{}".format(user[0]))
        self.sportlerName.setEditText(user[1])
        self.sportlerVName.setEditText(user[2])
        self.sportlerAlter.setCurrentIndex(user[3]-2)
        self.sportlerGeschlecht.setCurrentIndex(int(bool(user[4]))+1)
        self.sportlerAusDatenbank = True

    def getUserData(self)->None:
        self.sportlerNamen = QueryTool().fetchOneCol2List("LG_NGD","Name")
        self.sportlerVNamen = QueryTool().fetchOneCol2List("LG_NGD","Vorname")

        for i in range(len(self.sportlerVNamen)):
            j = self.sportlerVNamen[i]
            k = self.sportlerNamen[i]

            self.sportlerVName.addItem(j+" "+k)
            self.sportlerName.addItem(k+" "+j)
        self.sportlerVName.setEditText("")
        self.sportlerName.setEditText("")