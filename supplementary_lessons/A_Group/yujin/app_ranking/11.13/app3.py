from urllib.request import urlopen
from bs4 import BeautifulSoup
import xmltodict
import pandas as pd
import pymysql as sql
from sqlalchemy import create_engine
import pandas.io.sql as pSql
import re
import numpy as np
from view import *

import sys

class Model:
    # 받아온 파일 디비에 넣기 
    # DB_CONNECTION_REAL_URL = 'mysql+pymysql://root:12341234@pythondb.cnuyexfvmvqz.ap-northeast-2.rds.amazonaws.com:3306/pythondb'
    @staticmethod
    def insertCrawlingData(df, tbl_name):
        DB_CONNECTION_TEST_URL = 'mysql+pymysql://root:12341234@localhost:3306/pythondb'
        # 디비 오픈
        engine  = create_engine(DB_CONNECTION_TEST_URL, encoding='utf8')
        conn    = engine.connect()
        df.to_sql( name=tbl_name, con=conn, if_exists='append' ,index=False)
        # 디비 닫기
        conn.close()


    # 앱 전체 문서 가져오기
    # 앱 종류별 분류 입력
    def loading(self,rankType,batch='console'):
        self.batch=batch
        Model.rankType = rankType
        code='LMNO147679'
        market='g'
        app_type='all'
        rank=50
        url = 'http://api.gevolution.co.kr/rank/xml/?aCode={code}&market={market}&appType={app_type}&rankType={rank_type}&rank={rank}'.format(code=code, market=market, app_type=app_type, rank_type=rankType, rank=rank)
        doc = xmltodict.parse(urlopen(url).read())
        if doc['response']['header']['resultCode']== '0000':
            load = 'ok'
        else:
            print('랭킹 타입 %s 에 대한 정보를 불러오지 못했습니다' % rankType)
            print('에러 이유 : ', doc['response']['header']['resultMsg'])
            load = 'no'

        return doc, load    



    # 각 데이터 프레임 생성
    def makeDataFrame(self,doc):
        col = ['aid','ranking','lastWeek','gameName','rating','googleUrl']
        doc_data=[]
        tmp=[]
        for i in range(0,len(doc['response']['items']['item'])):
            tmp=[doc['response']['items']['item'][i][colname] for colname in col]
            doc_data.append(tmp)

        doc_df=pd.DataFrame(doc_data)
        # 컬렴명 변경하기
        doc_df.columns=['app_id','ranking','lastWeek','gameName','score','googleUrl']
        
        self.getUrl(self,doc_df)




    # 상세 페이지 주소 받아오기
    def getUrl(self,doc_df):
        # 이제 각 googleUrl로 접속해서
        # 앱 종류, 가격, 다운 수, 앱 내 평점 을 크롤링 해오자
        doc_url=list(doc_df['googleUrl'])
        if self.rankType in ('1','3','4'):    
            doc_df2 = self.getDetails_free(self,doc_url,doc_df)
        else:
            doc_df2 = self.getDetails_notfree(self,doc_url,doc_df)
        self.regexcol_name(self,doc_df2)


    # 상세 내용 받아오기
    # 1,3,4
    def getDetails_free(self,doc_url,doc_df):
        developer=[]
        genre=[]
        for url in doc_url:
            soup=BeautifulSoup(urlopen(url),'html.parser')
            detailinfo1=[]
            for span in soup.find('div', class_='i4sPve'):
                detailinfo1.append(span.text.strip())
            developer.append(detailinfo1[0])
            genre.append(detailinfo1[1:])
        dic={'developer':developer,'genre':genre}
        detail=pd.DataFrame(dic)
        doc_df2=pd.concat([doc_df,detail],axis=1)

        return doc_df2


    # 상세 내용 받아오기
    # 2,5
    def getDetails_notfree(self,doc_url,doc_df):
        developer=[]
        genre=[]
        price=[]
        for url in doc_url:
            soup=BeautifulSoup(urlopen(url),'html.parser')
            detailinfo2=[]
            for span in soup.find('div', class_='i4sPve'):
                detailinfo2.append(span.text.strip())
            developer.append(detailinfo2[0])
            genre.append(detailinfo2[1:])
            price.append(soup.find('span',class_='oocvOe').text.rstrip(' Buy'))
        dic={'developer':developer,'genre':genre, 'price':price}
        detail=pd.DataFrame(dic)
        doc_df2=pd.concat([doc_df,detail],axis=1)

        return doc_df2



    # 정규식 처리
    # gameName
    def regexcol_name(self,doc_df2):
        list_gamename=list(doc_df2['gameName'])
        p=re.compile('[^ㄱ-ㅣ가-힣\w\s\:\"\;\[\]\(\)\.\#\-]+')
        gName1=[]
        for name in list_gamename:
            gName1.append(p.sub(' ',name))
        doc_df2['gameName']=gName1   
        
        if self.batch=='batch':
            self.genrestruc(doc_df2)
        else:
            View.check(doc_df2)


    # 받아온 데이터 보여주고 확인하기

    # 장르 컬럼 구조 수정
    @classmethod
    def genrestruc(cls,doc_df2):
        genre2=[]
        for genre in doc_df2['genre']:
            genre=str(genre)
            genre2.append(genre)
        doc_df2['genre']=genre2
        if cls.rankType in ('2','5'):
            Model.regexcol_price(Model,doc_df2)
        else:
            tbl_name='app_ranking_%s' % cls.rankType
            Model.insertCrawlingData(doc_df2,tbl_name)
            print('랭킹 타입 %s 적재 완료' % cls.rankType)

    # 정규식 처리
    # price -> 2,5만
    def regexcol_price(self,doc_df2):
        list_price=list(doc_df2['price'])

        price222=[]
        for price in list_price:
            if len(price.split(' ')) == 2:
                price2=price.split(' ')[1]
            else:
                price2=price
            price222.append(price2)

        p=re.compile('[^\d\,]+')
        price2=[]
        for price in price222:
            price2.append(p.sub('',price))
        doc_df2['price']=price2

        tbl_name='app_ranking_%s' % self.rankType
        self.insertCrawlingData(doc_df2,tbl_name)
        print('랭킹 타입 %s 적재 완료' % self.rankType)
        

