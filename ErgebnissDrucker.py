from PyQt5.QtCore import QRectF

from LGPdfWriter import LGPdfWriter
from Sportler import Sportler
from ErgebnissListe import getDisziplin

class ErgebnissDrucker():
    def __init__(self,sportler:Sportler):
        self.dateiName = "Ergebnisse/{}/{}/{}.pdf"
        self.dateiName = self.dateiName.format(sportler.Alter,sportler.geschlechtStr,
                                               sportler.Vname+" "+sportler.Name)
        self.disziplinen = getDisziplin(sportler.Alter)

        try:
            with LGPdfWriter(self.dateiName) as p:

                #Überschrift
                p.text("Kinder - und Jugendzehnkampf", QRectF(1, 40, 765, 30), size=20, bold=True)
                p.text("Wettkampfkarte", QRectF(1, 80, 765, 30), size=20, bold=True)

                #Wettkampfkarte
                p.table(QRectF(60, 140, 650, 100),
                        ["Name", "Vorname", "Alter", "Gruppe",
                         sportler.Name, sportler.Vname, sportler.jahrgang, sportler.klasseSep], 4, 2)

                p.text("Disziplin", QRectF(20, 290, 200, 30), size=20, bold=True)
                p.text("Ergebnis", QRectF(210, 290, 400, 30), size=20, bold=True)
                p.text("Punkte", QRectF(610, 290, 100, 30), size=20, bold=True)

                punkte = sportler.Ranking.prepare4PDF()
                tabledata = list()
                numrows = 0
                for i in range(10):
                    if punkte[i][0] is "-":
                        continue
                    numrows+=1
                    tabledata.append(punkte[i][0])
                    if i < 4:
                        tabledata.append({"text":"{}".format(punkte[i][2][0]),"x":(1,3)})
                        tabledata.append("{}".format(punkte[i][1]))
                    else:
                        tabledata.append("{}".format(punkte[i][2][0]))
                        tabledata.append("{}".format(punkte[i][2][1]))
                        tabledata.append("{}".format(punkte[i][2][2]))
                        tabledata.append("{}".format(punkte[i][1]))

                p.table(QRectF(60, 350, 650, 570),tabledata, 5, numrows, w={0: 280, 4: 70})

                p.table(QRectF(60, 940, 650, 100),
                       ["Gesammtpunkte", {"text": "{}".format(punkte["Total"][0]), "color": p._sg, "shaded": True},
                        "Gesammtplatzierung", {"text":  "{}".format(punkte["Total"][1]), "color": p._sg, "shaded": True}
                    ], 2, 2, w={1: 70})
        except PermissionError:
            return