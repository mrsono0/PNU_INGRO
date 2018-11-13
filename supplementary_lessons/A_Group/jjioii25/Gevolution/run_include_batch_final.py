import requests
import xmltodict
from urllib.request import urlopen
import pandas as pd
import numpy as np
import pymysql as my
from random import choice
import sys
from dask.array.random import _choice

conn = None
# 데이터베이스 연결
def openDB():
    conn    = my.connect(
                        host = '127.0.0.1',
                        user = 'root',
                        password = '12341234',
                        db = 'pythondb',
                        charset = 'utf8',
                        cursorclass=my.cursors.DictCursor
    )
    return conn

# 데이터베이스 해제
def closeDB():
    if conn:conn.close()



# 웹크롤링관련 메뉴 선택하는 함수
def crawlMenuChoice(*choice):
    if not choice:
        choice=input('''
        웹크롤링 프로그램입니다.
        수집하고자하는 데이터를 선택해주세요 :
        G - 구글플레이
        A - 애플앱스토어
        Q - 프로그램 종료
        ''')
    return choice


# 콘솔버전일때 실행하는 함수
def consoleStage():
    choice = crawlMenuChoice()
    if choice == 'Q':
        print('웹크롤링 프로그램을 종료합니다.')
        sys.exit()
    else:
        getWebdata(choice)

# # 배치버전일때 실행하는 함수
def batchStage(choice, state):
    getWebdata(choice, state)
    pass


# Gevolution 사이트 연동하여 필요한 데이터 크롤링하는 함수
def getWebdata(choice, *state):
    print('웹 크롤링을 시작합니다.')
    # 발급된 계정의 인증키
    GEVOLUTION_API_KEY = 'MNOP826189'
    # g:구글플레이, a:애플 앱스토어
    market = choice[0].lower()
    # game:게임, app:일반앱, all:전체(게임+일반앱)
    app_type = 'game'
    # 1:무료, 2:유료,3:매출,4:신규무료,5:신규유료
    rank_type = 1
    # 1~OO위까지 출력 (max:100)
    rank = 100
    url = 'http://api.gevolution.co.kr/rank/xml/?aCode={code}&market={market}&appType={app_type}&rankType={rank_type}&rank={rank}'.format(code=GEVOLUTION_API_KEY, market=market, app_type=app_type, rank_type=rank_type, rank=rank)
    fp = urlopen(url)
    doc = xmltodict.parse( fp.read() )
    print('웹 크롤링이 완료되었습니다.')
    fp.close()
    
    game_df = makeDataFrame(doc, rank, choice)
    if state:
        checkData(game_df, state)
    else:
        state = checkData(game_df)        
    nextStage(game_df, state)



# 크롤링한 데이터로 데이터프레임 생성하는 함수
def makeDataFrame( doc, rank, choice ):
    aid = [ doc['response']['items']['item'][d]['aid'] for d in range(rank) ]
    ranking = [ doc['response']['items']['item'][d]['ranking'] for d in range(rank) ]
    lastWeek = [ doc['response']['items']['item'][d]['lastWeek'] for d in range(rank) ]
    rating = [ doc['response']['items']['item'][d]['rating'] for d in range(rank) ]
    gameName = [ doc['response']['items']['item'][d]['gameName'] for d in range(rank) ]
    publisher = [ doc['response']['items']['item'][d]['publisher'] for d in range(rank) ]
    game_dict = { 'aid':aid, 'ranking':ranking, 'lastWeek':lastWeek, 'rating':rating, 
                    'gameName':gameName, 'publisher':publisher, 'market':choice[0] }

    game_df = pd.DataFrame(game_dict)
    return game_df

# 크롤링한 데이터가 사용자가 원하는 데이터가 맞는지 개수를 확인하는 함수
def checkData(game_df, *state):
    print('데이터의 개수가 맞는지 확인합니다.')
    if len(game_df) == 100:    
        print('게임랭킹데이터가 100개 수집되었습니다.')
        if state:
            # print('크롤링후state',state)
            return state
        else: 
            state='ok'
            return state
    else:
        print('게임랭킹데이터의 개수가 100개가 아닙니다.')
        state = 'restart'
        return state


# 크롤링 후 다음 단계를 실행하는 함수
def nextStage(game_df, state):
    # print(state[0])
    if state == 'ok':
        choice2 = str(input('다음 단계를 실행하려면 yes를 입력해주세요.'))
        if choice2 == 'yes':
            print('DB에 수집한 데이터를 적재합니다.')
            uploadDB(game_df)
            # sys.exit(1)
        else:
            print('처음으로 돌아갑니다.')
            consoleStage()
    elif state == 'restart':
        print('프로그램을 다시 시작합니다.')
        consoleStage()
    elif state[0] == 'batch':
        print('DB에 수집한 데이터를 적재합니다.')
        uploadDB(game_df)
        # sys.exit(1)
        


# insert sql문 실행하는 함수
def insertData( game_df, i ):
    conn = openDB()
    with conn.cursor() as cursor:
        sql = 'insert into tbl_game (aid,ranking,lastWeek,rating,gameName,publisher,market) values(%s, %s, %s, %s, %s, %s, %s);'
        cursor.execute( sql, (game_df['aid'][i],game_df['ranking'][i],game_df['lastWeek'][i],
            game_df['rating'][i],game_df['gameName'][i],game_df['publisher'][i],game_df['market'][i] ) )
    # 디비 반영
    conn.commit()
    # 영향받은 row의 수
    return conn.affected_rows()

# DB에 데이터를 적재하는 함수
def uploadDB(game_df):
    for i in range(len(game_df)):
        insertData(game_df, i)
    closeDB()
    print('게임랭킹데이터를 DB에 적재완료했습니다.')


######################### DB관련 업무 - 추후에 추가하는방안 생각해보기

#사용자에게 검색하고자 하는 제작사를 입력받는 함수
def inputPublisher():
    publisher = input('검색하고자하는 제작사를 입력해주세요.')
    return publisher

# 사용자에게 입력받은 제작사로 select문 실행하는 함수 
def selectData( publisher ):
    conn = openDB()
    rows=None
    with conn.cursor() as cursor:
        sql    = "select * from tbl_game where publisher=%s;"       
        cursor.execute( sql, (str(publisher)))
        rows = cursor.fetchall()
    closeDB()
    return rows


# select문 실행한 결과를 보여주는 함수
def viewData( ):
    publisher = inputPublisher()
    rows = selectData( publisher )
    print(rows)


# 배치함수
def batchRun():
    print('구글플레이스토어 게임랭킹 100개를 적재합니다.')
    batchStage('G', 'batch')
    print('애플앱스토어 게임랭킹 100개를 적재합니다.')
    batchStage('A', 'batch')


# 콘솔버전 실행
# consoleStage()

# 배치버전 실행
# batchStage('G', 'batch')

if __name__ == '__main__':
    print('배치함수실행')
    batchRun()
