
# coding: utf-8

# In[58]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import xmltodict
import pandas as pd
import pymysql as sql
from sqlalchemy import create_engine
import pandas.io.sql as pSql
# 샘플
code='LMNO147679'
market='g'
app_type='all'
rank_type=2
rank=50
url = 'http://api.gevolution.co.kr/rank/xml/?aCode={code}&market={market}&appType={app_type}&rankType={rank_type}&rank={rank}'.format(code=code, market=market, app_type=app_type, rank_type=rank_type, rank=rank)
docdoc = xmltodict.parse(urlopen(url).read())


# In[37]:


# 일단 모든 종류의 데이터 다 가져오자
# 구글 먼저하자
# 앱타입은 게임/일반앱/게임+일반앱 인데, 게임+일반앱으로 다하자
# rank_type 별로 다 가져오자 -> 1:무료, 2:유료,3:매출,4:신규무료,5:신규유료 <= 3은 아직 쓸 생각 없지만 for문 쓸때 편하게 그냥 가져오자
# 모든 분류 다 랭크 50까지
# 즉 rank_type 만 바꾸면됨
doc=[]
for i in range(0,5):    
    url = 'http://api.gevolution.co.kr/rank/xml/?aCode={code}&market={market}&appType={app_type}&rankType={rank_type}&rank={rank}'.format(code=code, market=market, app_type=app_type, rank_type=i, rank=rank)
    doc.append(xmltodict.parse(urlopen(url).read()))
len(doc)


# In[38]:


# doc1은 무료, doc2는 유료 doc3은 매출 doc4는 신규무료 doc5는 신규유료
doc1=doc[0]
doc2=doc[1]
doc3=doc[2]
doc4=doc[3]
doc5=doc[4]


# In[39]:


# 일단 앱 기본 정보부터 담자
# doc1로 먼저해보고 나머지 적용하자
# 앱 고유값, 현재 순위, 지난주 순위, 앱 이름, 앱 평가점수, 앱 상세페이지  
len(doc1['response']['items']['item'])
# 일단 50개 잘 들어옴


# In[45]:


# 홈페이지 내용과 다르게 타입이 전부다 string
print(type(doc1['response']['items']['item'][0]['aid']),
type(doc1['response']['items']['item'][0]['ranking']),
type(doc1['response']['items']['item'][0]['lastWeek']),
type(doc1['response']['items']['item'][0]['gameName']),
type(doc1['response']['items']['item'][0]['rating']),
type(doc1['response']['items']['item'][0]['googleUrl']))


# In[46]:


# 우선 받아오는 필드가 컬럼이 되는 dataframe을 만든다
# 인덱스는 앱 고유값으로할지 현재 순위로 할지 추후에 정한다
doc1_data=[]
tmp=[]
col = ['aid','ranking','lastWeek','gameName','rating','googleUrl']
for i in range(0,len(doc1['response']['items']['item'])):
    tmp=[doc1['response']['items']['item'][i][colname] for colname in col]
    doc1_data.append(tmp)
print(doc1_data[:3])


# In[62]:


doc1_df=pd.DataFrame(doc1_data)
doc1_df.head()


# In[63]:


# 컬렴명 변경하기
doc1_df.columns=['app_id','ranking','lastWeek','gameName','score','googleUrl']
doc1_df.head()


# In[64]:


# 디비에 계속해서 넣으려면 수집한 시간 컬럼이 필요하겠다
from datetime import datetime 
nownow = datetime.now() 
now='%s-%s-%s' % ( nownow.year, nownow.month, nownow.day )
doc1_df['date']=now
doc1_df.head()
# 생각해보니 디비에서 자동으로 타임스탬프 생성해서 필요가 없었다
# 또 다시 생각해보니 테이블 구색을 맞추려면 date 가 필요하겠다


# In[ ]:


# 받아온 파일 디비에 넣기 ㅠㅠㅠ
DB_CONNECTION_TEST_URL = 'mysql+pymysql://root:12341234@localhost:3306/pythondb'
DB_CONNECTION_REAL_URL = 'mysql+pymysql://root:12341234@pythondb.cnuyexfvmvqz.ap-northeast-2.rds.amazonaws.com:3306/pythondb'
def insertCrawlingData(df, rankingInfo):
    # 디비 오픈
    engine  = create_engine(self.DB_CONNECTION_TEST_URL, encoding='utf8')
    conn    = engine.connect()
    doc1_df.to_sql( name='app_ranking', con=conn, if_exists='append' ,index=False)
    # 디비 닫기
    conn.close()
