import datetime

import Ranking

class Sportler:
    def __init__(self, ID: int, Name: str, Vname: str, Alter: int, Geschlecht: bool, Rank: Ranking):
        self.ID = ID
        self.Name = Name
        self.Vname = Vname
        self.Alter = Alter
        self.Geschlecht = Geschlecht
        #@var Ranking
        self.Ranking = Rank

    def __str__(self):
        return ("Benutzerkennung: {}\n" +
        "Name: {},{}\n" +
        "Alter: {} / Jahrgang {}\n" +
        "Geschlecht: {}\n" +
        "Punkte: \n {}\n\n").format(self.ID,
                                    self.Name,
                                    self.Vname,
                                    self.jahrgang,
                                    self.Alter,
                                    self.geschlechtStr,
                                    self.Ranking)
    def __repr__(self):
        return self.__str__()

    @property
    def geschlechtStr(self)->str:
        return "Weiblich" if self.Geschlecht else "Männlich"

    @property
    def klasse(self)->str:
        return "{}{}".format("W" if self.Geschlecht else "M", self.Alter)

    @property
    def klasseSep(self)->str:
        return "{}: {:2}".format("W" if self.Geschlecht else "M", self.Alter)

    @property
    def jahrgang(self):
        return datetime.date.today().year - self.Alter