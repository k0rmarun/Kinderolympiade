class Wert:
    def __init__(self, W1: float = 0, W2: float = 0, W3: float = 0):
        if isinstance(W1,str) or isinstance(W1,str) or isinstance(W1,str):
            raise NotImplementedError

        self._Werte = [W1, W2, W3]
        self._sortierteWerte = [W1, W2, W3]
        self._sortierteWerte.sort()

    def __len__(self)->float:
        """
        Gibt den Mittleren der 3 Versuche zurück.

        >>> w = Wert(1,3,2)
        >>> w.__len__()
        2
        >>> w = Wert(5.0,4.0,3.0)
        >>> w.__len__()
        4.0
        >>> w = Wert()
        >>> w.__len__()

        """
        if self.isEmpty():
            return None
        if(isinstance(self._sortierteWerte[1],str)):
            return float(self._sortierteWerte[1])
        else :
            return self._sortierteWerte[1]

    def len(self)->float:
        """
        Alias für __len__
        """
        return  self.__len__()

    def max(self)->float:
        """
        Gibt den Größten der 3 Versuche zurück.

        >>> w = Wert(1,3,2)
        >>> w.max()
        3
        >>> w = Wert(5.0,4.0,3.0)
        >>> w.max()
        5.0
        >>> w = Wert()
        >>> w.max()

        """
        if self.isEmpty():
            return None
        if(isinstance(self._sortierteWerte[2],str)):
            return float(self._sortierteWerte[2])
        else :
            return self._sortierteWerte[2]

    def min(self)->float:
        """
        Gibt den Kleinsten der 3 Versuche zurück.

        >>> w = Wert(1,3,2)
        >>> w.min()
        1
        >>> w = Wert(5.0,4.0,3.0)
        >>> w.min()
        3.0
        >>> w = Wert()
        >>> w.min()

        """
        if self.isEmpty():
            return None
        if(isinstance(self._sortierteWerte[0],str)):
            return float(self._sortierteWerte[0])
        else :
            return self._sortierteWerte[0]

    def __eq__(self, other)->bool:
        """
        Prüft ob beide Wertegruppen gleiche Ergebnisse liefern

        >>> a = Wert()
        >>> b = Wert()
        >>> a == b
        True
        >>> c = Wert(1,2,3)
        >>> d = Wert(3,2,1)
        >>> c == d
        True
        >>> e = Wert(1.001,2.003,3.005)
        >>> f = Wert(1.0,2.0,3.0)
        >>> e == f
        True
        """

        if not isinstance(other,Wert):
            raise TypeError("How did you get here?\r\n{}".format(other))

        if not (self.isEmpty() == other.isEmpty()):
            return False
        elif self.isEmpty() is True and other.isEmpty() is True:
            return True

        eqMax = abs(self.max() - other.max()) < 0.01
        eqLen = abs(self.len() - other.len()) < 0.01
        eqMin = abs(self.min() - other.min()) < 0.01
        return eqMax and eqLen and eqMin

    def __lt__(self, other)->bool:
        """
        Prüft ob eine Wertegruppe kleiner ist

        >>> a = Wert()
        >>> aa = Wert()
        >>> b = Wert(1,2,4)
        >>> c = Wert(1,2,3)
        >>> d = Wert(1,2,2)
        >>> e = Wert(1,1,1)
        >>> f = Wert(1,1,1)
        >>> a < aa
        False
        >>> a < b
        True
        >>> c < b
        True
        >>> d < c
        True
        >>> e < d
        True
        >>> f < e
        False
        """
        #Sind beide Default?
        try:
            if self.isEmpty() and other.isEmpty():
                return False
            elif self.isEmpty():
                return True
            elif other.isEmpty():
                return False
        except:
            print(other)
            raise

        #Größter Wert schon kleiner?
        if self.max() < other.max():
            return True
        elif self.max() > other.max():
            return False

        #Größter Wert gleich und zweitgrößter kleiner?
        if self.len() < other.len():
            return True
        elif self.len() > other.len():
            return False

        #Die ersten 2 Werte gleich, der letzte kleiner?
        if self.min() < other.min():
            return True

        #Narp
        return False

    def isEmpty(self):
        """
        Prüft ob der Wert ein Dummywert ist, oder befüllt wurde

        >>> Wert().isEmpty()
        True
        >>> Wert(1).isEmpty()
        False
        >>> Wert(1,2).isEmpty()
        False
        >>> Wert(1,2,3).isEmpty()
        False
        """
        return self._Werte[0] < 0.001 and self._Werte[1] < 0.001 and self._Werte[2] < 0.001

    def __str__(self):
        return "{}, {}, {}".format(self.max(),self.len(), self.min())

    def __repr__(self):
        return "Wert("+self.__str__()+")"

    def prepare4PDF(self,disziplin:int)->tuple:
        if self.isEmpty():
            return []
        if disziplin < 4:
            return [self.max()]
        return self._Werte.copy()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print("Doctest Succeeded")
