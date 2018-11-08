import pymysql as sql
import pandas as pd

class getData:
    ## 적재된거 가져오기
    # 디비 접속
    def __init__(self,rankType):
        self.rankType=rankType
        self.initDB()

    def initDB(self):
        conn = sql.connect(
                        host='127.0.0.1',            
                        user='root',
                        password='12341234',
                        db='pythondb',
                        charset='utf8',
                        cursorclass=sql.cursors.DictCursor
                        )
        # cur = conn.cursor()
        
        tbl_name = 'app_ranking_%s' % self.rankType

        df = pd.read_sql('select * from ' + tbl_name , con = conn)
        print(df)
        conn.close()

        # df = pd.read_sql('select Date, Close from ' + tableName + ' where Date >= 20151101' , con = conn)


