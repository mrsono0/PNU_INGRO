import pymysql as sql
import pandas as pd
import matplotlib.pyplot as plt

class getData:
    ## 적재된거 가져오기
    # 디비 접속
    def initDB(rankType):
        conn = sql.connect(
                        host='127.0.0.1',            
                        user='root',
                        password='12341234',
                        db='pythondb',
                        charset='utf8',
                        cursorclass=sql.cursors.DictCursor
                        )
        tbl_name = 'app_ranking_%s' % rankType
        df = pd.read_sql('select * from ' + tbl_name , con = conn)
        print(df.head(10))
        conn.close()

        # df = pd.read_sql('select Date, Close from ' + tableName + ' where Date >= 20151101' , con = conn)


    #  50순위 내 앱 장르별 비율 
    def genreProp(rankType):
        conn = sql.connect(
                        host='127.0.0.1',            
                        user='root',
                        password='12341234',
                        db='pythondb',
                        charset='utf8',
                        cursorclass=sql.cursors.DictCursor
                        )
        tbl_name = 'app_ranking_%s' % rankType

        df = pd.read_sql('select * from ' + tbl_name , con = conn)

        genrelist = list()
        for genre in df['genre']:
            genre=genre.lstrip("[")
            genre=genre.rstrip("]")
            genre=genre.split(', ')

            for minigenre in genre:
                genrelist.append(minigenre)          

        # 파이차트 그리기
        # 데이터를 조정해야하므로 일단 히스토 먼저 시험
        plt.hist(genrelist)
        plt.show()


        # print(df.head(10))
        conn.close()        


getData.genreProp('5')
