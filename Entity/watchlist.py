import mysql.connector
class Watchlist():
    def __init__(self):
        self.mydb = self.connectToDatabase()

    def connectToDatabase(self):
        return mysql.connector.connect(
            host="154.64.252.69",
            user="root",
            password="csci321fyp",
            database="csci321",
            auth_plugin='mysql_native_password'
        )

    def fetchOne(self, sql, val) -> dict:
        with self.mydb.cursor(dictionary=True) as cursor:
            cursor.execute(sql, val)
            result = cursor.fetchone()
        return result

    def fetchAll(self, sql, val) -> list:
        with self.mydb.cursor(dictionary=True) as cursor:
            cursor.execute(sql, val)
            result = cursor.fetchall()
        return result

    def commit(self, sql, val):
        with self.mydb.cursor() as cursor:
            cursor.execute(sql, val)
            self.mydb.commit()
            return cursor.lastrowid
    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.close()

    def get_watchlist_by_accountID(self,accountId):
        sql = "select * from watchlist where accountId=%s"
        val = (accountId,)
        return self.fetchOne(sql, val)

    def update_watchlist(self, accountId, stockSymbol):
        sql = "UPDATE watchlist SET stockSymbol=%s WHERE accountId=%s"
        val = (stockSymbol,accountId)
        self.commit(sql, val)