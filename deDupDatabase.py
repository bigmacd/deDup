import sqlite3

class DeDupDatabase:
    """
    This class provides the dedup database and makes getting data into it easy.
    """
    def __init__(self, create = True):
        self.connection = sqlite3.connect("dedup.db")
        self.connection.isolation_level = None
        self.cursor = self.connection.cursor()
        self.resetStatement = "DROP TABLE if exists dups"
        self.createStatement = "CREATE TABLE dups (filespec VARCHAR(1024), pathspec VARCHAR(2048), md5 VARCHAR(1000))"
        self.insertStatement = "insert into dups (filespec, pathspec, md5) VALUES (?, ?, ?)"
        self.getStatement = "select pathspec, filespec from dups where md5 = '{0}'"
        self.getHashGroupsQuery = "select md5 from dups group by md5 having count(*) > 1"

        if create:
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
        self.cursor.execute(self.getHashGroupsQuery)
        return self.cursor.fetchall()


    def getByHash(self, hash: str):
        self.cursor.execute(self.getStatement.format(hash))
        return self.cursor.fetchall()
