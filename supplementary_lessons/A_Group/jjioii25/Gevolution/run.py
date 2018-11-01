import requests
import xmltodict
from urllib.request import urlopen
import pandas as pd
import numpy as np
import pymysql as my

conn    = my.connect(
                    host = '127.0.0.1',
                    user = 'root',
                    password = '12341234',
                    db = 'pythondb',
                    charset = 'utf8',
                    cursorclass=my.cursors.DictCursor
)

# 메뉴 선택하는 함수
def menuShow():
    i = True
    while i:
        choice=input('''
        DB관련해서 하실 일을 골라주세요 :
        I - 게임랭킹데이터 적재
        V - 게임랭킹데이터 조회
        D - 게임랭킹데이터 삭제
        Q - 프로그램 종료
        ''')
        if choice == 'Q':
            print('DB관련 프로그램을 종료합니다.')
            i = menuChoice(choice)
        else:
            menuChoice(choice)


def menuChoice(choice):
    if choice == 'I':
        uploadDB()
    elif choice=="V":
        viewData()
    elif choice=="D":
        deleteData()
    elif choice=="Q":
        return False

# Gevolution 사이트 연동하여 필요한 데이터 크롤링하는 함수
def getWebdata():
    # 발급된 계정의 인증키
    GEVOLUTION_API_KEY = 'MNOP826189'
    # g:구글플레이, a:애플 앱스토어
    market = 'a'
    # game:게임, app:일반앱, all:전체(게임+일반앱)
    app_type = 'game'
    # 1:무료, 2:유료,3:매출,4:신규무료,5:신규유료
    rank_type = 1
    # 1~OO위까지 출력 (max:100)
    rank = 50
    url = 'http://api.gevolution.co.kr/rank/xml/?aCode={code}&market={market}&appType={app_type}&rankType={rank_type}&rank={rank}'.format(code=GEVOLUTION_API_KEY, market=market, app_type=app_type, rank_type=rank_type, rank=rank)
    doc = xmltodict.parse( urlopen(url).read() )
    return doc, rank

# 크롤링한 데이터로 데이터프레임 생성하는 함수
def makeDataFrame( ):
    doc, rank = getWebdata()
    aid = [ doc['response']['items']['item'][d]['aid'] for d in range(rank) ]
    ranking = [ doc['response']['items']['item'][d]['ranking'] for d in range(rank) ]
    lastWeek = [ doc['response']['items']['item'][d]['lastWeek'] for d in range(rank) ]
    rating = [ doc['response']['items']['item'][d]['rating'] for d in range(rank) ]
    gameName = [ doc['response']['items']['item'][d]['gameName'] for d in range(rank) ]
    publisher = [ doc['response']['items']['item'][d]['publisher'] for d in range(rank) ]
    game_dict = { 'aid':aid, 'ranking':ranking, 'lastWeek':lastWeek, 'rating':rating, 
                    'gameName':gameName, 'publisher':publisher }

    game_df = pd.DataFrame(game_dict)
    return game_df

# insert sql문 실행하는 함수
def insertData( aid,ranking,lastWeek,rating,gameName,publisher ):
    with conn.cursor() as cursor:
        sql = 'insert into tbl_game (aid,ranking,lastWeek,rating,gameName,publisher) values(%s, %s, %s, %s, %s, %s);'
        cursor.execute( sql, (aid,ranking,lastWeek,rating,gameName,publisher) )
    # 디비 반영
    conn.commit()
    # 영향받은 row의 수
    return conn.affected_rows()

# 데이터베이스 해제
def closeDB():
    if conn:conn.close()


# DB에 데이터를 적재하는 함수
def uploadDB():
    game_df = makeDataFrame()
    # 현재 range에 50이라고 하드코딩되어있는 것 수정
    for i in range(50):
        insertData(game_df['aid'][i], game_df['ranking'][i], game_df['lastWeek'][i], game_df['rating'][i], 
            game_df['gameName'][i], game_df['publisher'][i])
    closeDB()
    print('게임랭킹데이터를 DB에 적재완료했습니다.')





def viewData():
    return ''

def deleteData():
    return ''


menuShow()
