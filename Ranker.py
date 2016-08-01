from math import floor

from Ranking import Ranking
from Wert import Wert


class Ranker:
    def __init__(self,alter:int):
        self.RankingDisziplin = -1
        self.Rankings = []
        self.alter = alter

    def append(self,elem:Ranking)->None:
        self.Rankings.append(elem)

    def Platz2Punkte(self,i: int)->int:
        """
        Vergibt Punkte anhand des Platzes in der Punkteliste

        >>> Ranker(10).Platz2Punkte(0)
        30
        >>> Ranker(10).Platz2Punkte(10)
        10
        >>> Ranker(10).Platz2Punkte(30)
        5
        """
        if i is 999:
            return 0
        try:
            return [30,25,20,18,16,15,14,13,12,11,10,9,8,7,6][i]
        except IndexError:
            return 5

    def IteratePlatz(self,Werte:tuple):
        """
        Iteriert über eine Liste von Werten ung gibt die zugehörige Liste der Plätze aus

        >>> list(Ranker(10).IteratePlatz((Wert(1),Wert(1),Wert(3),Wert(3),Wert(3),Wert(4)))) #doctest: +NORMALIZE_WHITESPACE
        [1, 1, 3, 3, 3, 6]
        """
        if isinstance(Werte[0],Wert):
            curWert = Wert(99999999999999999,999999999999999999999999999999999999,99999999999999999999999999999999999999999)
        else:
            curWert = Ranking(self.alter)
        platz = 0
        übersprungene = 1

        for wert in Werte:
            if isinstance(wert,Wert) and wert.isEmpty():
                yield 999
                continue
            if curWert == wert:
                übersprungene += 1
            else:
                platz += übersprungene
                übersprungene = 1
            curWert = wert
            yield max(platz,1)

    def extractDisziplin(self)->tuple:
        ret = []
        for Rank in self.Rankings:
            ret.append( Rank.werte(self.RankingDisziplin))
        return tuple(ret)

    def RankingCalc(self)->None:
        for disziplin in range(10):
            self.RankingDisziplin = disziplin
            self.Rankings.sort(key=self.RankingCalcPrepare)
            if self.RankingDisziplin >= 4:
                self.Rankings.reverse()

            plätze = self.IteratePlatz(self.extractDisziplin())
            for Rank in self.Rankings:
                p = self.Platz2Punkte(plätze.__next__()-1)
                Rank.setPunkte(disziplin,p)

            self.Rankings.sort(reverse=True)
            plätze = self.IteratePlatz(self.Rankings)
            for Rank in self.Rankings:
                Rank.setPlatz(plätze.__next__())

    def invertiereNachkomma(self,el:float)->float:
        """
        Invertiert die Nachkommastellen einer Zahl und schneide bei 0,4 ab => Hochsprung: 4. versuch = ungültig

        >>> Ranker(10).invertiereNachkomma(0.0)
        1.0
        >>> Ranker(10).invertiereNachkomma(0.3)
        0.7
        >>> Ranker(10).invertiereNachkomma(5.5)
        0
        """
        d = el - floor(el)
        if d > 0.3:
            return 0
        return floor(el)+(1 - d)

    def RankingCalcPrepare(self,el: Ranking)->Wert:
        if el.werte(self.RankingDisziplin).isEmpty():
            return Wert()
        if self.RankingDisziplin is not 6:
            return el.werte(self.RankingDisziplin)
        else: #Hochsprung xxx.1 -> xxx.9, xxx.2 -> xxx.8, xxx.3 = xxx.7
            ele = el.werte(self.RankingDisziplin)
            ele = (ele.min(),ele.len(),ele.max())
            ele = map(self.invertiereNachkomma,ele)
            return Wert(*ele)

    def __str__(self):
        ret = ""
        for i in self.Rankings:
            ret += str(i)+"\r\n"
        return ret

    def __repr__(self):
        ret = "Ranker(\r\n"
        for i in self.Rankings:
            ret += "\t" + repr(i)+",\r\n"
        return ret[0:-3]+"\r\n)"

    def prepare4PDF(self):
        ret = list()
        for i in self.Rankings:
            ret.append(i.prepare4PDF())
        return ret


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print("Doctest Succeeded")
