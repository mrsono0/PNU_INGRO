
# coding: utf-8

# In[56]:


# kakao api 사용=>계정등록=>앱생성=>인증키 발급(restful  key)
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import xmltodict
import pandas as pd
import datetime
import pymysql as my
GEV_API = 'STUV378914'
code = GEV_API


# In[4]:


url = 'http://api.gevolution.co.kr/rank/xml/?aCode=HIJK372129&market=g&appType=game&rankType=1&rank=20'


# In[5]:


# 의도한대로 url을 구성함.
def url_maker(code=code):
    url= 'http://api.gevolution.co.kr/rank/xml/?aCode= {code}&market=g&appType=game&rankType=1&rank=50'.format(code=code)
    return url


# In[6]:


url_maker()


# In[7]:


doc = xmltodict.parse(urlopen(url).read())


# In[13]:


gevo_df = pd.read_csv('./data/game.csv', encoding='utf-8')


# In[48]:


gevo_df_beta = gevo_df.T
gevo_df_beta


# In[49]:


for i in range(20):
    info_i = []
    now = '%s'% str(datetime.datetime.now())[:10]
    Base = doc['response']['items']['item'][i]
    info_i.append(Base['gameName'])
    info_i.append(Base['ranking'])
    info_i.append(Base['lastWeek'])
    info_i.append(Base['publisher'])
    info_i.append(Base['gevolUrl'])
    info_i.append(Base['rating'])
    info_i.append(Base['movieUrl'])
    info_i.append(Base['cafeUrl'])
    info_i.append(now)
    gevo_df_beta.insert(loc=i, column=i, value=info_i)
gevo_df_beta


# In[55]:


gevo_df_beta2 = gevo_df_beta.T
gevo_df_final = gevo_df_beta2.set_index('gameName')
gevo_df_final


# In[58]:


import pymysql as sql
from sqlalchemy import create_engine
import pandas.io.sql as pSql


# In[59]:


# 연결
engine = create_engine('mysql+pymysql://root:sb0515@localhost:3306/pythondb', encoding = 'utf8')
conn = engine.connect()


# In[60]:


gevo_df_final.to_sql( name='game_info',
             con=conn,
             if_exists='append')
#닫기
conn.close()


# ## 게임 이름을 인덱스로하는건 마지막에하자.

# >>> import pandas as pd
# >>> import numpy as np
# >>> df = pd.DataFrame(columns=['lib', 'qty1', 'qty2'])
# >>> for i in range(5):
# >>>     df.loc[i] = [np.random.randint(-1,1) for n in range(3)]
# >>>
# >>> print(df)
#     lib  qty1  qty2
# 0    0     0    -1
# 1   -1    -1     1
# 2    1    -1     1
# 3    0     0     0
# 4    1    -1    -1
# 
# [5 rows x 3 columns]
