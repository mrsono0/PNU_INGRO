import pymysql as my
import os

def selectData(rankType):
    rows = None # 쿼리 결과        
    conn = my.connect(
            host='127.0.0.1',            
            user='root',
            password='12341234',
            db='pythondb',
            charset='utf8',
            cursorclass=my.cursors.DictCursor
            )

    tbl_name = 'app_ranking_%s' % rankType
    subquery = '(SELECT * FROM %s ORDER BY date DESC LIMIT 50) lastdata' % tbl_name

    try:            
        with conn.cursor() as cursor:
            sql    = 'select * from %s' % subquery
            cursor.execute( sql )
            rows   = cursor.fetchall()
    except Exception as e:
        rows = None
        print('에러->',e)        
    return rows
    # conn.close()


def getFiles(rankType):
    path_dir = 'C:/Users/idec/Documents/analysis_project/App_ranking/static/batch_image/rankType%s' % rankType
    # path_dir3 = 'C:/Users/idec/Documents/analysis_project/App_ranking/console_csv'
    # path_dir4 = 'C:/Users/idec/Documents/analysis_project/App_ranking/console_image'
    # path_dir = [path_dir1, path_dir2]
    file_list = os.listdir(path_dir)
    # print(file_list)
    return file_list




def selectDesc(rankType):
    rows = None # 쿼리 결과        
    conn = my.connect(
            host='127.0.0.1',            
            user='root',
            password='12341234',
            db='pythondb',
            charset='utf8',
            cursorclass=my.cursors.DictCursor
            )

    tbl_name = 'app_ranking_%s' % rankType
    subquery = '(SELECT * FROM %s ORDER BY date DESC LIMIT 50) lastdata' % tbl_name

    try:            
        with conn.cursor() as cursor:
            sql    = 'select ranking, gameName, score, developer, genre from %s order by score desc' % subquery
            cursor.execute( sql )
            rows   = cursor.fetchall()
    except Exception as e:
        rows = None
        print('에러->',e)        
    return rows




