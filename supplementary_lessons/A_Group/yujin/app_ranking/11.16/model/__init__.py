import pymysql as my


def selectData(rankType):
    rows = None # 쿼리 결과        
    conn = sql.connect(
            host='127.0.0.1',            
            user='root',
            password='12341234',
            db='pythondb',
            charset='utf8',
            cursorclass=sql.cursors.DictCursor
            )

    tbl_name = 'app_ranking_%s' % rankType
    subquery = '(SELECT * FROM %s ORDER BY date DESC LIMIT 50) lastdata' % tbl_name

    try:            
        with conn.cursor() as cursor:
            sql    = 'select * from %s'           
            cursor.execute( sql, (subquery, ))
            rows   = cursor.fetchall()
    except Exception as e:
        rows = None
        # print('에러->',e)        
    return rows
    # conn.close()



