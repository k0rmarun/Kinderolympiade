from math import floor

from Wert import Wert
from ErgebnissListe import getDisziplin


#ToDo: Clean up
class Ranking:
    Disziplinen = {
        "Sprint":0,
        "Hürden":1,
        "Mittel":2,
        "Lang":3,
        "Weit":4,
        "Stab":5,
        "Hoch":6,
        "Reifen":7,
        "Wurf":8,
        "Kugel":9
    }
    Disziplinen2Str = {
        0:"50m/75m Sprint",
        1:"60m/80m Hürden",
        2:"200m Lauf",
        3:"400m/800m/1000m Lauf",
        4:"Weitsprung",
        5:"Stabweitsprung",
        6:"Hochsprung",
        7:"Fahrradreifenweitwurf",
        8:"Wurfstabweitwurf",
        9:"Kugelstoßen"
        }

    Einheiten = ("sec",   "sec",   "sec",   "min", "m",   "m",   "cm"#,Versuche
    ,"m",     "m",   "m")

    def __init__(self,alter:int,Werte=None):
        if Werte is None:
            Werte = dict()

        d = list(getDisziplin(alter))

        for i in range(10):
            if i not in Werte.keys():
               Werte[i]=Wert()
            self.Disziplinen2Str[i] = d[i]
        self._Werte=Werte

        self._Punkte={
            0:0,
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:0,
            7:0,
            8:0,
            9:0
            }
        self._Platz=0

    def punkte(self,disziplin:int = -1)->int:
        """
        Gibt die Punktzahl einer Disziplin zurück

        >>> w = {0:Wert(1),1:Wert(1),9:Wert(1)}
        >>> a = Ranking(10,w)
        >>> a.setPunkte(0,10)
        >>> a.setPunkte(1,20)
        >>> a.setPunkte(9,30)
        >>> a.punkte(0)
        10
        >>> a.punkte(2)
        0
        >>> a.punkte(9)
        30
        >>> a.punkte()
        60
        >>> a.punkte(10)
        Traceback (most recent call last):
        ...
        AssertionError
        """
        assert disziplin >= -1 and disziplin < 10
        if disziplin == -1:
            return sum(self._Punkte.values())
        return self._Punkte[disziplin]

    def setPunkte(self,disziplin: int, wert: int = 0)->None:
        """
        Speichert die Punktzahl einer Disziplin
        >>> w = {0:Wert(1),1:Wert(1),3:Wert(1)}
        >>> a = Ranking(10,Werte=w)
        >>> a.setPunkte(0,10)

        >>> a.setPunkte(1,20)

        >>> a.setPunkte(3,-30)
        Traceback (most recent call last):
        ...
        AssertionError
        >>> a.setPunkte(10,0)
        Traceback (most recent call last):
        ...
        AssertionError
        """
        assert disziplin >= 0 and disziplin < 10
        assert wert >= 0 and wert <= 30
        if self.werte(disziplin).isEmpty():
            self._Punkte[disziplin] = 0
        else:
            self._Punkte[disziplin] = wert

    def werte(self,disziplin:int = -1)->Wert:
        """
        Speichert die Punktzahl einer Disziplin
        >>> w = {0:Wert(0,1,2)}
        >>> a = Ranking(10,w)
        >>> a.werte(0)
        Wert(2, 1, 0)
        >>> a.werte(2)
        Wert(None, None, None)
        >>> a.werte(-1)
        Traceback (most recent call last):
        ...
        AssertionError
        >>> a.werte(10)
        Traceback (most recent call last):
        ...
        AssertionError
        """
        assert disziplin>=0 and disziplin < 10
        assert disziplin in self._Werte.keys()
        return self._Werte[disziplin]

    def setPlatz(self,platz:int)->None:
        """
        Speichert den Platz des Rankings
        >>> a = Ranking(10)
        >>> a.setPlatz(1)

        >>> a.setPlatz(0)
        Traceback (most recent call last):
        ...
        AssertionError
        """
        assert isinstance(platz,int)
        assert platz > 0
        self._Platz = platz

    def platz(self)->int:
        return self._Platz

    def __lt__(self, other)->bool:
        """
        Prüft ob eines von 2 Rankings eine kleinere Gesammtpunktzahl aufweist
        >>> w = {1:Wert(1),2:Wert(1)}
        >>> a = Ranking(10,w)
        >>> a.setPunkte(1,10)
        >>> b = Ranking(10)
        >>> b.setPunkte(2,9)
        >>> a < b
        False
        >>> b < a
        True
        """
        if not isinstance(other,Ranking):
            raise TypeError("How did you get here?\r\n{}".format(other))

        return self.punkte() < other.punkte()

    def __eq__(self, other):
        """
        Prüft ob eines von 2 Rankings eine gleich hohe Gesammtpunktzahl aufweist

        >>> a = Ranking(10)
        >>> a.setPunkte(1,10)
        >>> b = Ranking(10)
        >>> b.setPunkte(2,10)
        >>> a == b
        True
        """
        if not isinstance(other,Ranking):
            raise TypeError("How did you get here?\r\n{}".format(other))
        return self.punkte() == other.punkte()

    def __str__(self)->str:
        return str(self.prepare4PDF())

    def prepare4PDF(self)->dict:
        r"""
        Erzeugt aus eine Struktur, die beim PDF-Drucken leicht iteriert werden kann

        >> Ranking(10,{0: Wert(),
        ... 1: Wert(9, 0, 0),
        ...  2: Wert(2, 0, 0),
        ...  3: Wert(7, 0, 0),
        ...  4: Wert(8, 1, 1),
        ...  5: Wert(8, 3, 2),
        ...  6: Wert(70.4, 63.0, 0),
        ...  7: Wert(9, 8, 0),
        ...  8: Wert(7, 5, 4),
        ...  9: Wert(9, 5, 1)}).prepare4PDF()  #doctest: +NORMALIZE_WHITESPACE
        {0: ('...', 0, ['-']),
         1: ('...', 0, ['9 sec']),
         2: ('...', 0, ['2 sec']),
         3: ('...', 0, ['7 min']),
         4: ('...', 0, ['8 m', '1 m', '1 m']),
         5: ('...', 0, ['8 m', '3 m', '2 m']),
         6: ('...', 0, ['70.4 cm\r\nxxx', '63.0 cm\r\no', '-']),
         7: ('...', 0, ['9 m', '8 m', '-']),
         8: ('...', 0, ['7 m', '5 m', '4 m']),
         9: ('...', 0, ['9 m', '5 m', '1 m']),
         'Total': (0, 0)}
        """
        ret = dict()
        for disziplin in range(10):
            if self.werte(disziplin).isEmpty():
                werte = ["-","-","-"] if disziplin >= 4 else ["-"]
            else:
                werte = self.werte(disziplin).prepare4PDF(disziplin)
                for j in range(len(werte)):
                    werte[j] = round(werte[j], 2)
                    if werte[j] < 0.01:
                        werte[j] = "-"
                        continue
                    versucheText = ""
                    if disziplin is 6:
                        w = werte[j]
                        werte[j] = int(floor(werte[j]))
                        versuche = w-floor(w)
                        versuche *= 10
                        versuche = int(max(1,versuche))
                        versucheText = "\r\n"+("x"*(versuche-1)) + ("o" if versuche < 4 else "")

                    werte[j]="{} {}{}".format(werte[j],self.Einheiten[disziplin],versucheText)
            ret[disziplin]=(self.Disziplinen2Str[disziplin],self.punkte(disziplin),werte)
        ret["Total"]=(self.punkte(),self._Platz)
        return ret

    def __repr__(self)->str:
        """
        >>> Ranking(10) #doctest: +NORMALIZE_WHITESPACE
        Ranking({0: Wert(None, None, None),
         1: Wert(None, None, None),
          2: Wert(None, None, None),
           3: Wert(None, None, None),
            4: Wert(None, None, None),
             5: Wert(None, None, None),
              6: Wert(None, None, None),
               7: Wert(None, None, None),
                8: Wert(None, None, None),
                 9: Wert(None, None, None)})
        """
        return "Ranking({})".format(self._Werte)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print("Doctest Succeeded")