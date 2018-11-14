import pymysql as sql
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns

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

        genreset=set(genrelist)
        genredict=dict.fromkeys(genreset,0)

        for genre in genrelist:
            genredict[genre] += 1

        # print(genreSer)

        # 2% 이하일 경우 합하여 기타로 빼기
        # genredict.values()
        countgenre=len(genrelist)
        standard = len(genrelist) * 0.02
        genredict_cp=genredict.copy()
        for genre in genredict_cp:
            if genredict[genre] < standard:
                genredict.pop(genre)

        genreSer = pd.Series(genredict)

        # 파이차트 그리기
        # 라벨과 퍼센트 붙이기 ========================================
        plt.pie(genreSer,labels=genreSer.index,autopct='%1.1f%%')
        
        plt.show()


        # print(df.head(10))
        conn.close()        


    # 가격을 범위를 구분하여 범위별 빈도 수
    def priceHist(rankType):
        conn = sql.connect(
                        host='127.0.0.1',            
                        user='root',
                        password='12341234',
                        db='pythondb',
                        charset='utf8',
                        cursorclass=sql.cursors.DictCursor
                        )
        tbl_name = 'app_ranking_%s' % rankType

        df = pd.read_sql('select price from ' + tbl_name , con = conn)

        # 먼저 리스트로 받고 -> for 문
        # 하나씩 나눠 받아서 ,을 없애고 -> 정규식
        # 최소값 최대값 구한 뒤 -> min, max
        # 계급 설정

        p=re.compile('[\,]')
        price1=[]
        for price in df['price']:
            if price == '':
                price = '0'
            else:
                price1.append(p.sub('',price))
        price1 = list(map(int, price1))
        # 1000 ~ 33000 가격 존재
        # print(min(price1),max(price1))

        # 98개 나옴 (2개 None값)
        # print(len(price1))

        # 3000원 단위로 계급 10개 나누기
        # pricedict={'less3000':0,'3000to5999':0,'6000to8999':0,'9000to11999':0,'12000to14999':0,
        # '15000to17999':0,'18000to20999':0,'21000to23999':0,'24000to26999':0,'more30000':0}
        # for price in price1:
        #     if price<3000:
        #         pricedict['less3000'] += 1
        #     elif price<6000:
        #         pricedict['3000to5999'] += 1
        #     elif price<9000:
        #         pricedict['6000to8999'] += 1
        #     elif price<12000:
        #         pricedict['9000to11999'] += 1    
        #     elif price<15000:
        #         pricedict['12000to14999'] += 1
        #     elif price<18000:
        #         pricedict['15000to17999'] += 1
        #     elif price<21000:
        #         pricedict['18000to20999'] += 1
        #     elif price<24000:
        #         pricedict['21000to23999'] += 1
        #     elif price<27000:
        #         pricedict['24000to26999'] += 1    
        #     else:
        #         pricedict['more30000'] += 1
        pricelist=[]
        for price in price1:
            if price<3000:
                price='less3000'
                pricelist.append(price)
            elif price<6000:
                price='3000to5999'
                pricelist.append(price)
            elif price<9000:
                price='6000to8999'
                pricelist.append(price)
            elif price<12000:
                price='9000to11999'    
                pricelist.append(price)
            elif price<15000:
                price='12000to14999'
                pricelist.append(price)
            elif price<18000:
                price='15000to17999'
                pricelist.append(price)
            elif price<21000:
                price='18000to20999'
                pricelist.append(price)
            elif price<24000:
                price='21000to23999'
                pricelist.append(price)
            elif price<27000:
                price='24000to26999'
                pricelist.append(price)
            else:
                price='more30000'
                pricelist.append(price)
        # print(pricelist)
        # priceSer = pd.Series(pricedict)
        # plt.hist(priceSer)
        # plt.show()

        # sns.countplot(priceSer)
        sns.countplot(pricelist)
        plt.title('Histogram of Price')
        # 가격 범위 오름차순 혹은 빈도수 내림차순으로 재정렬
        # 가능하면 빈도수 0인 항목도 표시되게
        plt.show()

        # print(df)
        conn.close() 



    # 앱 평가점수 기준 10순위 내림차순 도표
    def scoreDesc(rankType):
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
        df = pd.read_sql('select ranking, gameName, score, developer, genre from %s order by score desc' % subquery, con = conn)

        pd.set_option('display.max_columns', 20)
        # 나중에 gameName 왼쪽 혹은 오른쪽 정렬 해놓기

        print(df[:10])



getData.genreProp('5')

# getData.priceHist('5')

# getData.scoreDesc('5')



# a=getData.priceHist('5')
# print(a.iloc[:6].values)
# if a.iloc[4].any():
#     print('None아님')
# else:print('none')
