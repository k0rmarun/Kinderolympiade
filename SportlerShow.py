from datetime import date

from PyQt5.QtWidgets import( QTableWidget,
                            QTableWidgetItem)

from QueryTool import QueryTool


class SportlerShow(QTableWidget):
    def __init__(self,parent=None):
        super(SportlerShow, self).__init__(parent)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(("Vorname","Name","Alter","Geschlecht"))
        self.update()
        self.setMinimumHeight(300)


    def update(self):
        data = QueryTool().fetchAll("LG_NGD")
        self.setRowCount(len(data))
        k = 0
        for v in data:
            self.setItem(k, 0, QTableWidgetItem(v[1]))
            self.setItem(k, 1, QTableWidgetItem(v[2]))
            self.setItem(k, 2, QTableWidgetItem("{}".format(date.today().year-int(v[3]))))
            self.setItem(k, 3, QTableWidgetItem("Weiblich" if bool(v[4]) else "Männlich"))
            k+=1

