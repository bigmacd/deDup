import sqlite3

class DeDupDatabase:
    """
    This class provides the dedup database and makes getting data into it easy.
    """
    def __init__(self):
        self.connection = sqlite3.connect("dedup.db")
        self.cursor = self.connection.cursor()
        self.resetStatement = "DROP TABLE if exists dups"
        self.createStatement = "CREATE TABLE dups (filespec VARCHAR(1024), pathspec VARCHAR(2048), md5 VARCHAR(1000))"
        self.insertStatement = "insert into dups (filespec, pathspec, md5) VALUES (?, ?, ?)"
        self.getStatement = "select pathspec, filespec from dups where md5 = '?'"
        self.getHashGroupsQuery = "select md5 from dups group by md5 having count(*) > 1"


        try:
            self.cursor.execute(self.resetStatement)
            self.cursor.execute(self.createStatement)
        except:
            pass


    def insert(self, path: str, file: str, md5: str):
        try:
            self.cursor.execute(self.insertStatement, (path, file, md5))
        except Exception as ex:
            print(str(ex))
            print(path, file, md5)


    def getHashGroups(self):
        return self.cursor.execute(self.getHashGroupsQuery)


    def getByHash(self, hash: str):
        self.cursor.execute(self.getStatement, (hash))
        return self.cursor.fetchall()
