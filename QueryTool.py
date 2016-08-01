import sqlite3
from Utility import SingletonDecorator

@SingletonDecorator
class QueryTool():
    def __init__(self):
        self.dbConnection = sqlite3.connect("daten.db")
        with self.dbConnection as con:
            self.db = con.cursor()

    def query(self,queryString:str, *params)->sqlite3.Cursor:
        return self.db.execute(queryString, params)

    def queryAndFetch(self,queryString:str, *params)->list:
        return self.query(queryString, *params).fetchall()

    def chainedQuery(self, querys:tuple, index:int=0, *params)->list:
        current = querys[index]

        data = self.query(current,params).fetchall()

        if len(querys)<=index:
            return data
        else:
            return self.chainedQuery(querys=querys, index=index+1, *data)

    def insert(self,table: str, **data)->sqlite3.Cursor:

        newID = self.numEntryInTable(table)

        params = (newID,)

        query = "INSERT INTO "+table+" (ID,"+  (",".join(data.keys())) +") VALUES ("
        for k,v in data.items():
            query += "?,"
            params += (v,)
        query += "?)"
        ret = self.query(query, *params)
        self.dbConnection.commit()
        return ret

    def update(self,table: str, ID: int, **data)->sqlite3.Cursor:
        query = "UPDATE "+table+" SET "

        params = ()

        for k,v in data.items():
            query += k+"=?, "
            params += (v,)
        query = query[0:-2]

        query += " WHERE ID=?"
        params += (ID,)

        ret = self.query(query, *params)
        self.dbConnection.commit()
        return ret

    def numEntryInTable(self, table: str)->int:
        l = self.query("SELECT ID FROM "+table).fetchall()
        flatten = lambda *n: (e for a in n for e in(flatten(*a) if isinstance(a,(tuple,list)) else (a,)))
        l2 = list(flatten(l))

        try:
            return max(l2)+1
        except ValueError:
            return 1

    def fetchOneCol2List(self, table: str, col: str)->list:
        query = "SELECT "+col+" FROM "+table
        ret = []
        for i in self.query(query).fetchall():
            ret.append(i[0])
        return ret

    def fetchAll(self, table: str)->list:
        query = "SELECT * FROM "+table
        return self.query(query).fetchall()

    def fetchAllByWhere(self, table: str, **where)->list:
        query = "SELECT * FROM "+table+" WHERE "
        params = ()
        for k,v in where.items():
            query += k+"=? AND "
            params += (v,)
        query = query[0:-5]
        return self.query(query, *params).fetchall()


    def queryByNames(self, VName: str, Name: str):
        query = "SELECT * FROM LG_NGD WHERE Name=? AND Vorname=?"

        ret = []
        for i in self.query(query,VName,Name).fetchall():
            ret.append(i)
        for i in self.query(query,Name,VName).fetchall():
            ret.append(i)

        if(len(ret) !=1):
            return None
        else:
            return ret[0]