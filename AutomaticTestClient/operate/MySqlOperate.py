import pymysql
from constant.BaseConstant import mysqlHost, mysqlUsername, mysqlPassword, mysqlDatabase


class mySqlOperate:
    @staticmethod
    def search(sql, params):
        db = pymysql.connect(mysqlHost, mysqlUsername, mysqlPassword, mysqlDatabase)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        results = None
        try:
            cursor.execute(sql, params)
            results = cursor.fetchall()
        except Exception as e:
            print(e)
        db.close()
        return results

    @staticmethod
    def update(sql, params):
        db = pymysql.connect(mysqlHost, mysqlUsername, mysqlPassword, mysqlDatabase)
        cursor = db.cursor()
        try:
            cursor.execute(sql, params)
            db.commit()
            db.close()
            return 1
        except Exception as e:
            db.rollback()
            db.close()
            print(e)
            return 0
