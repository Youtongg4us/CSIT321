import mysql.connector
class Notification:
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

    def get_notifications_by_accountId(self,accountId):
        sql = "select * from notification where accountId=%s"
        val = (accountId,)
        return self.fetchAll(sql, val)

    def set_notification(self,accountId,notification,notificationType,referenceId):
        sql = "INSERT INTO notification(accountId,notification,notificationType,referenceId) VALUES (%s,%s,%s,%s)"
        val = (accountId,notification,notificationType,referenceId)
        self.commit(sql, val)
        sql = '''
                DELETE FROM notification
                WHERE notificationId NOT IN (
                    SELECT min_id FROM (
                        SELECT MIN(notificationId) as min_id
                        FROM notification
                        GROUP BY accountId, referenceId, notificationType
                    ) as subquery
                );'''
        val = ("")
        self.commit(sql, val)




if __name__ == "__main__":
    pass