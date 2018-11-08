from urllib.request import urlopen
from bs4 import BeautifulSoup
import xmltodict
import pandas as pd
import pymysql as sql
from sqlalchemy import create_engine
import pandas.io.sql as pSql
import re
import numpy as np



# 앱 전체 문서 가져오기
# 앱 종류별 분류 입력
def take_document():
    code='LMNO147679'
    market='g'
    app_type='all'
    rank=50
    doc=[]
    for i in range(0,5):    
        idx=i+1
        url = 'http://api.gevolution.co.kr/rank/xml/?aCode={code}&market={market}&appType={app_type}&rankType={rank_type}&rank={rank}'.format(code=code, market=market, app_type=app_type, rank_type=idx, rank=rank)
        doc.append(xmltodict.parse(urlopen(url).read()))

    doc1=doc[0]
    doc2=doc[1]
    doc3=doc[2]
    doc4=doc[3]
    doc5=doc[4]
    makeDataFrame(doc1,doc2,doc3,doc4,doc5)


# 각 데이터 프레임 생성
def makeDataFrame(doc1,doc2,doc3,doc4,doc5):
    col = ['aid','ranking','lastWeek','gameName','rating','googleUrl']
    doc1_data=[]
    tmp=[]
    for i in range(0,len(doc1['response']['items']['item'])):
        tmp=[doc1['response']['items']['item'][i][colname] for colname in col]
        doc1_data.append(tmp)

    doc2_data=[]
    tmp=[]
    for i in range(0,len(doc2['response']['items']['item'])):
        tmp=[doc2['response']['items']['item'][i][colname] for colname in col]
        doc2_data.append(tmp)
        
    doc3_data=[]
    tmp=[]
    for i in range(0,len(doc3['response']['items']['item'])):
        tmp=[doc3['response']['items']['item'][i][colname] for colname in col]
        doc3_data.append(tmp)
        
    doc4_data=[]
    tmp=[]
    for i in range(0,len(doc4['response']['items']['item'])):
        tmp=[doc4['response']['items']['item'][i][colname] for colname in col]
        doc4_data.append(tmp)
        
    doc5_data=[]
    tmp=[]
    for i in range(0,len(doc5['response']['items']['item'])):
        tmp=[doc5['response']['items']['item'][i][colname] for colname in col]
        doc5_data.append(tmp)

    doc1_df=pd.DataFrame(doc1_data)
    doc2_df=pd.DataFrame(doc2_data)
    doc3_df=pd.DataFrame(doc3_data)
    doc4_df=pd.DataFrame(doc4_data)
    doc5_df=pd.DataFrame(doc5_data)

    # 컬렴명 변경하기
    doc1_df.columns=['app_id','ranking','lastWeek','gameName','score','googleUrl']
    doc2_df.columns=['app_id','ranking','lastWeek','gameName','score','googleUrl']
    doc3_df.columns=['app_id','ranking','lastWeek','gameName','score','googleUrl']
    doc4_df.columns=['app_id','ranking','lastWeek','gameName','score','googleUrl']
    doc5_df.columns=['app_id','ranking','lastWeek','gameName','score','googleUrl']
    
    getUrl(doc1_df, doc2_df, doc3_df,doc4_df,doc5_df)

# 받아온 파일 디비에 넣기 ㅠㅠㅠ
DB_CONNECTION_TEST_URL = 'mysql+pymysql://root:12341234@localhost:3306/pythondb'
# DB_CONNECTION_REAL_URL = 'mysql+pymysql://root:12341234@pythondb.cnuyexfvmvqz.ap-northeast-2.rds.amazonaws.com:3306/pythondb'
def insertCrawlingData(df, tbl_name):
    # 디비 오픈
    engine  = create_engine(DB_CONNECTION_TEST_URL, encoding='utf8')
    conn    = engine.connect()
    df.to_sql( name=tbl_name, con=conn, if_exists='append' ,index=False)
    # 디비 닫기
    conn.close()



# 상세 페이지 주소 받아오기
def getUrl(doc1_df, doc2_df, doc3_df,doc4_df,doc5_df):
    # 이제 각 googleUrl로 접속해서
    # 앱 종류, 가격, 다운 수, 앱 내 평점  을 크롤링 해오자
    # 우선 이것도 doc1 부터 먼저하고 후에 나머지 적용하자
    # doc1의 googleUrl 먼저 리스트에 담고
    # for 문을 돌려서 각 url에 접속
    doc1_url=list(doc1_df['googleUrl'])
    doc2_url=list(doc2_df['googleUrl'])
    doc3_url=list(doc3_df['googleUrl'])
    doc4_url=list(doc4_df['googleUrl'])
    doc5_url=list(doc5_df['googleUrl'])
    doc1_df2, doc3_df2, doc4_df2 = getDetails_free(doc1_url,doc3_url,doc4_url,doc1_df,doc3_df,doc4_df)
    doc2_df2, doc5_df2 = getDetails_notfree(doc2_url,doc5_url,doc2_df,doc5_df)
    regexcol_name(doc1_df2,doc2_df2,doc3_df2,doc4_df2,doc5_df2)


# 상세 내용 받아오기
# 1,3,4
def getDetails_free(doc1_url,doc3_url,doc4_url,doc1_df,doc3_df,doc4_df):
    developer=[]
    genre=[]
    for url in doc1_url:
        soup=BeautifulSoup(urlopen(url),'html.parser')
        detailinfo1=[]
        for span in soup.find('div', class_='i4sPve'):
            detailinfo1.append(span.text.strip())
        developer.append(detailinfo1[0])
        genre.append(detailinfo1[1:])
    dic={'developer':developer,'genre':genre}
    detail=pd.DataFrame(dic)
    doc1_df2=pd.concat([doc1_df,detail],axis=1)

    developer=[]
    genre=[]
    for url in doc3_url:
        soup=BeautifulSoup(urlopen(url),'html.parser')
        detailinfo3=[]
        for span in soup.find('div', class_='i4sPve'):
            detailinfo3.append(span.text.strip())
        developer.append(detailinfo3[0])
        genre.append(detailinfo3[1:])
    dic={'developer':developer,'genre':genre}
    detail=pd.DataFrame(dic)
    doc3_df2=pd.concat([doc3_df,detail],axis=1)        

    developer=[]
    genre=[]
    for url in doc4_url:
        soup=BeautifulSoup(urlopen(url),'html.parser')
        detailinfo4=[]
        for span in soup.find('div', class_='i4sPve'):
            detailinfo4.append(span.text.strip())
        developer.append(detailinfo4[0])
        genre.append(detailinfo4[1:])
    dic={'developer':developer,'genre':genre}
    detail=pd.DataFrame(dic)
    doc4_df2=pd.concat([doc4_df,detail],axis=1)        
    
    return doc1_df2, doc3_df2, doc4_df2


# 상세 내용 받아오기
# 2,5
def getDetails_notfree(doc2_url,doc5_url,doc2_df,doc5_df):
    developer=[]
    genre=[]
    price=[]
    for url in doc2_url:
        soup=BeautifulSoup(urlopen(url),'html.parser')
        detailinfo2=[]
        for span in soup.find('div', class_='i4sPve'):
            detailinfo2.append(span.text.strip())
        developer.append(detailinfo2[0])
        genre.append(detailinfo2[1:])
        price.append(soup.find('span',class_='oocvOe').text.rstrip(' Buy'))
    dic={'developer':developer,'genre':genre, 'price':price}
    detail=pd.DataFrame(dic)
    doc2_df2=pd.concat([doc2_df,detail],axis=1)

    developer=[]
    genre=[]
    price=[]
    for url in doc5_url:
        soup=BeautifulSoup(urlopen(url),'html.parser')
        detailinfo5=[]
        for span in soup.find('div', class_='i4sPve'):
            detailinfo5.append(span.text.strip())
        developer.append(detailinfo5[0])
        genre.append(detailinfo5[1:])
        price.append(soup.find('span',class_='oocvOe').text.rstrip(' Buy'))
    dic={'developer':developer,'genre':genre, 'price':price}
    detail=pd.DataFrame(dic)
    doc5_df2=pd.concat([doc5_df,detail],axis=1)
    return doc2_df2, doc5_df2



# 정규식 처리
# gameName
def regexcol_name(doc1_df2,doc2_df2,doc3_df2,doc4_df2,doc5_df2):
    list_gamename1=list(doc1_df2['gameName'])
    list_gamename2=list(doc2_df2['gameName'])
    list_gamename3=list(doc3_df2['gameName'])
    list_gamename4=list(doc4_df2['gameName'])
    list_gamename5=list(doc5_df2['gameName'])

    p=re.compile('[^ㄱ-ㅣ가-힣\w\s\:\"\;\[\]\(\)\.\#\-]+')
    gName1=[]
    for name in list_gamename1:
        gName1.append(p.sub(' ',name))
    doc1_df2['gameName']=gName1

    gName2=[]
    for name in list_gamename2:
        gName2.append(p.sub(' ',name))
    doc2_df2['gameName']=gName2

    gName3=[]
    for name in list_gamename3:
        gName3.append(p.sub(' ',name))
    doc3_df2['gameName']=gName3

    gName4=[]
    for name in list_gamename4:
        gName4.append(p.sub(' ',name))
    doc4_df2['gameName']=gName4

    gName5=[]
    for name in list_gamename5:
        gName5.append(p.sub(' ',name))
    doc5_df2['gameName']=gName5
    
    genrestruc(doc1_df2,doc2_df2,doc3_df2,doc4_df2,doc5_df2)


# 장르 컬럼 구조 수정
def genrestruc(doc1_df2,doc2_df2,doc3_df2,doc4_df2,doc5_df2):
    genre2=[]
    for genre in doc1_df2['genre']:
        genre=str(genre)
        genre2.append(genre)
    doc1_df2['genre']=genre2

    genre2=[]
    for genre in doc2_df2['genre']:
        genre=str(genre)
        genre2.append(genre)
    doc2_df2['genre']=genre2
    doc2_df2['genre']

    genre2=[]
    for genre in doc3_df2['genre']:
        genre=str(genre)
        genre2.append(genre)
    doc3_df2['genre']=genre2

    genre2=[]
    for genre in doc4_df2['genre']:
        genre=str(genre)
        genre2.append(genre)
    doc4_df2['genre']=genre2

    genre2=[]
    for genre in doc5_df2['genre']:
        genre=str(genre)
        genre2.append(genre)
    doc5_df2['genre']=genre2
    
    regexcol_price(doc1_df2,doc2_df2,doc3_df2,doc4_df2,doc5_df2)



# 정규식 처리
# price -> 2,5만
def regexcol_price(doc1_df2,doc2_df2,doc3_df2,doc4_df2,doc5_df2):
    list_price2=list(doc2_df2['price'])
    list_price5=list(doc5_df2['price'])

    price222=[]
    for price in list_price2:
        if len(price.split(' ')) == 2:
            price2=price.split(' ')[1]
        else:
            price2=price
        price222.append(price2)

    p=re.compile('[^\d\,]+')
    price2=[]
    for price in price222:
        price2.append(p.sub('',price))
    doc2_df2['price']=price2

    price222=[]
    for price in list_price5:
        if len(price.split(' ')) == 2:
            price2=price.split(' ')[1]
        else:
            price2=price
        price222.append(price2)

    price2=[]
    for price in price222:
        price2.append(p.sub('',price))
    doc5_df2['price']=price2

    insertCrawlingData(doc1_df2,'app_ranking_1')
    insertCrawlingData(doc2_df2,'app_ranking_2')
    insertCrawlingData(doc3_df2,'app_ranking_3')
    insertCrawlingData(doc4_df2,'app_ranking_4')
    insertCrawlingData(doc5_df2,'app_ranking_5')





# take_document()




# makeDataFrame()
# getUrl()
# getDetails_free()
# getDetails_notfree()
# regexcol_name(doc1_df2,doc2_df2,doc3_df2,doc4_df2,doc5_df2)
# regexcol_price(doc2_df2, doc5_df2)
# genrestruc(doc1_df2,doc2_df2,doc3_df2,doc4_df2,doc5_df2)



# DB에 데이터 적재
# insertCrawlingData(doc1_df2,'app_ranking_1')
# insertCrawlingData(doc2_df2,'app_ranking_2')
# insertCrawlingData(doc3_df2,'app_ranking_3')
# insertCrawlingData(doc4_df2,'app_ranking_4')
# insertCrawlingData(doc5_df2,'app_ranking_5')





