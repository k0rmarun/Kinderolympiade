from PyQt5.QtCore import QRectF

from Sportler import Sportler
from LGPdfWriter import LGPdfWriter


class UrkundenDrucker:
    def __init__(self,sportler:Sportler):
        self.dateiName = "Urkunden/{}/{}/{}.pdf"
        self.dateiName = self.dateiName.format(sportler.Alter,sportler.geschlechtStr,sportler.Vname+" "+sportler.Name)
        try:
            with LGPdfWriter(self.dateiName) as p:
                p.rect(QRectF(61, 60, 645, 980))
                p.rect(QRectF(66, 65, 635, 970))

                p.text("Urkunde",QRectF(60,120,645,100),size=100,shaded=10)
                p.text("Leichtathletik-Gemeinschaft-Neckargemünd",QRectF(60,230,645,30),size=20,shaded=True)
                p.image("images/Multikampf.jpeg",QRectF(200,290,328,328))

                p.text("Jedermann-Zehnkampf / Kinderolympiade",QRectF(60,640,645,30),size=20,shaded=True)

                p.text("Name:",QRectF(80,700,0,0),shaded=True)
                p.text("Klasse:",QRectF(80,760,0,0),shaded=True)
                p.text("Platzierung:",QRectF(80,820,0,0),shaded=True)
                p.text("Punkte:",QRectF(80,880,0,0),shaded=True)

                p.text("{}, {}".format(sportler.Name,sportler.Vname),QRectF(300,700,0,0),shaded=True)
                p.text(sportler.klasseSep,QRectF(300,760,0,0),shaded=True)
                p.text(sportler.Ranking.platz(),QRectF(300,820,0,0),shaded=True,color=p._sg)
                p.text(sportler.Ranking.punkte(),QRectF(300,880,0,0),shaded=True, color=p._sg)
        except PermissionError:
            return