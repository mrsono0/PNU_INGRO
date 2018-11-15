import pymysql as sql
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
from datetime import datetime
import os

class getData:
    # 10순위 내 앱 기본 정보
    def initDB(rankType,batch='console'):
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
        df = pd.read_sql('select * from %s' % subquery , con = conn)
        pd.set_option('display.max_columns', 20)
        finaldf=df.head(10)
        if batch=='console':
            print(finaldf)

        getData.saveCsv(finaldf,rankType,'basic',batch)

        conn.close()
        
    #  50순위 내 앱 장르별 비율 
    def genreProp(rankType,batch='console'):
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
        df = pd.read_sql('select * from %s' % subquery , con = conn)

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

        # 2% 이하일 경우 합하여 기타로 빼기
        countgenre=len(genrelist)
        standard = len(genrelist) * 0.02
        genredict_cp=genredict.copy()
        genredict["'etc'"]=0
        for genre in genredict_cp:
            if genredict[genre] < standard:
                genredict["'etc'"] += genredict[genre]
                genredict.pop(genre)
    
        genreSer = pd.Series(genredict)

        # 파이차트 그리기
        # 비율이 제일 큰게 떨어져 나오지며, 비율이 큰 순대로 이어지게 만들기
        explode = [0 for i in range(len(genreSer))]
        explode[0]=0.1
        explode=tuple(explode)
        fig=plt.figure(figsize=(9,9))
        sns.set_palette("coolwarm", 7)
        genreSer = genreSer.sort_values(ascending=False)
        plt.pie(genreSer,explode=explode,labels=genreSer.index,autopct='%1.1f%%')
        plt.title('Proportion of Genres')
        if batch=='console':
            plt.show()

        getData.saveImg(fig,rankType,'genrepie',batch)
        conn.close()        


    # 가격을 범위를 구분하여 범위별 빈도 수
    def priceHist(rankType,batch='console'):
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
        df = pd.read_sql('select price from %s' % subquery , con = conn)

        # ,을 없애고 최소값 최대값 구한 뒤 계급 설정
        p=re.compile('[\,]')
        price1=[]
        for price in df['price']:
            if price == '':
                price = '0'
            else:
                price1.append(p.sub('',price))
        price1 = list(map(int, price1))
        
        # 1000 ~ 33000 가격 존재
        # 98개 나옴 (2개 None값)
        # 3000원 단위로 계급 10개 나누기
        pricedict={'less3000':0,'3000to5999':0,'6000to8999':0,'9000to11999':0,'12000to14999':0,
        '15000to17999':0,'18000to20999':0,'21000to23999':0,'24000to26999':0,'more30000':0}
        for price in price1:
            if price<3000:
                pricedict['less3000'] += 1
            elif price<6000:
                pricedict['3000to5999'] += 1
            elif price<9000:
                pricedict['6000to8999'] += 1
            elif price<12000:
                pricedict['9000to11999'] += 1    
            elif price<15000:
                pricedict['12000to14999'] += 1
            elif price<18000:
                pricedict['15000to17999'] += 1
            elif price<21000:
                pricedict['18000to20999'] += 1
            elif price<24000:
                pricedict['21000to23999'] += 1
            elif price<27000:
                pricedict['24000to26999'] += 1    
            else:
                pricedict['more30000'] += 1

        priceSer = pd.Series(pricedict)

        fig=plt.figure(figsize=(14,6))
        ax=sns.barplot(priceSer.index, priceSer.values,palette='RdBu') 
        ax.set(xlabel="Price class", ylabel='Frequency')
        ax.set_title('Frequencies of Price class', y=1.02)
        # 가능하면 후에 비율 %로 annot
        for p in ax.patches:
            ax.annotate('{}'.format(int(p.get_height())), (p.get_x()+0.35, p.get_height()+0.4))
        if batch=='console':
            plt.show()
        getData.saveImg(fig,rankType,'pricebar',batch)
        conn.close() 


    # 앱 평가점수 기준 10순위 내림차순 도표
    def scoreDesc(rankType,batch='console'):
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
        finaldf=df.head(10)
        if batch=='console':
            print(finaldf)
        getData.saveCsv(finaldf,rankType,'scoredesc',batch)
        conn.close() 

    # 저장여부 물어보고 저장하는 함수
    def saveImg(fig,rankType,plotType,batch):
        if batch =='batch':
            save_q = 'y'
        else:        
            save_q=input(
            '''
                이미지를 저장하시겠습니까?
                예 : y 아니오 : n
                ('예' 선택 시 폴더에 적재, '아니오' 선택 시 프로그램 종료)
            '''
            )
        if save_q=='y':
            if batch=='console':
                path = './console_image' 
            else:
                path = './batch_image' 
            if not os.path.exists(path): 
                os.mkdir(path)    
            path = path + '/ranktype' + rankType 
            if not os.path.exists(path): 
                os.mkdir(path)                           
            nowtime = datetime.now().strftime('%Y%m%d%H%M%S')
            fig.savefig(path + '/%s_%s_%s.png' % (plotType,nowtime,rankType))
        else:
            quit()


    def saveCsv(finaldf,rankType,plotType,batch):
        if batch =='batch':
            save_q = 'y'
        else:
            save_q=input(
            '''
                데이터프레임을 저장하시겠습니까?
                예 : y 아니오 : n
                ('예' 선택 시 폴더에 적재, '아니오' 선택 시 프로그램 종료)
            '''
            )   
        if save_q=='y':
            if batch=='console':
                path = './console_csv'
            else:
                path = './batch_csv'        
            if not os.path.exists(path): 
                os.mkdir(path)     
            path = path + '/ranktype' + rankType 
            if not os.path.exists(path): 
                os.mkdir(path)                      
            nowtime = datetime.now().strftime('%Y%m%d%H%M%S')
            finaldf.to_csv(path + '/%s_%s_%s.csv' % (plotType,nowtime,rankType), encoding='utf-8-sig')
        else:
            quit()


