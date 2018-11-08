
# kakao api 사용=>계정등록=>앱생성=>인증키 발급(restful  key)
from urllib.request import urlopen
import xmltodict
import pandas as pd
import datetime
from sqlalchemy import create_engine

def upload_data():
    GEV_API = 'STUV378914'
    url= 'http://api.gevolution.co.kr/rank/xml/?aCode={GEV_API}&market=g&appType=game&rankType=1&rank=20'.format(GEV_API=GEV_API)

    doc = xmltodict.parse(urlopen(url).read())

    gevo_df = pd.read_csv('./data/game.csv', encoding='utf-8')
    gevo_df_beta = gevo_df.T
    gevo_df_beta

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

    gevo_df_beta2 = gevo_df_beta.T
    gevo_df_final = gevo_df_beta2.set_index('gameName')
    gevo_df_final


    # 연결
    engine = create_engine('mysql+pymysql://root:sb0515@localhost:3306/pythondb', encoding = 'utf8')
    conn = engine.connect()

    # SQL로 보내기
    gevo_df_final.to_sql( name='game_info',
                 con=conn,
                 if_exists='append')
    # 닫기
    conn.close()
    print('수집완료')
    return None


if __name__ == '__main__':
    upload_data()
else:
    pass
