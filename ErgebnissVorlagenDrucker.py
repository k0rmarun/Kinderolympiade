from PyQt5.QtCore import QRectF
from LGPdfWriter import LGPdfWriter
from QueryTool import QueryTool
from ErgebnissListe import getDisziplin

class ErgebnissVorlagenDrucker:
    disziplinen = ("Sprint",
               "Hürdenlauf",
               "200_400m",
               "400_800_1000m",
               "Weitsprung",
               "Stabweitsprung",
               "Hochsprung",
               "Reifenweitwurf",
               "Weitwurf",
               "Kugelstoßen")
    def __init__(self,Alter:int,Geschlecht:bool,Disziplin:int):
        self.disziplinen = list(getDisziplin(Alter))
        if self.disziplinen[Disziplin] is "-":
            return
        self.dateiName = "Vorlagen/{}{}/{}.pdf"
        self.dateiName = self.dateiName.format("W" if Geschlecht else "M", Alter, self.disziplinen[Disziplin])

        tabledata = list()
        tabledata.append({"text":"Name"})
        col = 1
        if Disziplin >= 4:
            col = 3
        for i in range(col):
            tabledata.append({"text":"Versuch {}".format(i+1)})

        users = self.queryUsers(Alter,Geschlecht)
        if len(users) == 0:
            return

        for user in users:
            tabledata.append("{}, {}".format(user[1],user[2]))
            for i in range(col):
                tabledata.append(" ")

        self.printer = LGPdfWriter(self.dateiName)

        #Überschrift
        self.printer.text("Kinder - und Jugendzehnkampf", QRectF(1, 40, 765, 30), size=20, bold=True)
        self.printer.text("Wettkampfvorlage {} ({}{})".format(self.disziplinen[Disziplin].replace("_","/"),"W" if Geschlecht else "M", Alter), QRectF(1, 80, 765, 30), size=20, bold=True)

        self.printer.table(QRectF(60, 140, 650, 885),tabledata, col+1, min(30,max(20,len(users))), w={0: 280})
        self.printer.end()

    def queryUsers(self,Alter:int, Geschlecht:bool)->list:
        return QueryTool().fetchAllByWhere("LG_NGD",WieAlt=Alter,Geschlecht=Geschlecht)