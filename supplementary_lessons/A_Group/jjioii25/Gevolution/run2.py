import requests
import xmltodict
from urllib.request import urlopen
import pandas as pd
import numpy as np
import pymysql as my
from random import choice
import sys

conn    = my.connect(
                    host = '127.0.0.1',
                    user = 'root',
                    password = '12341234',
                    db = 'pythondb',
                    charset = 'utf8',
                    cursorclass=my.cursors.DictCursor
)

# 데이터베이스 해제
def closeDB():
    if conn:conn.close()


# # 웹크롤링관련 메뉴 선택하는 함수
# def crawlMenuShow():
#     i = True
#     while i:
#         choice=input('''
#         웹크롤링 프로그램입니다.
#         수집하고자하는 데이터를 선택해주세요 :
#         G - 구글플레이
#         A - 애플앱스토어
#         Q - 프로그램 종료
#         ''')
        
#         if choice == 'Q':
#             print('웹크롤링 프로그램을 종료합니다.')
#             i = crawlMenuChoice(choice)
#         else:
#             crawlMenuChoice(choice)


# 웹크롤링관련 메뉴 선택하는 함수
def crawlMenuShow():
    choice=input('''
    웹크롤링 프로그램입니다.
    수집하고자하는 데이터를 선택해주세요 :
    G - 구글플레이
    A - 애플앱스토어
    Q - 프로그램 종료
    ''')
        
    if choice == 'Q':
        print('웹크롤링 프로그램을 종료합니다.')
        i = crawlMenuChoice(choice)
    else:
        crawlMenuChoice(choice)


def crawlMenuChoice(choice):
    if choice=="Q":
        return False
    else:
        getWebdata(choice)


# # DB관련 메뉴 선택하는 함수
# def dbMenuShow():
#     i = True
#     while i:
#         choice=input('''
#         DB관련해서 하실 일을 골라주세요 :
#         I - 게임랭킹데이터 적재
#         V - 게임제작사 조회
#         Q - 프로그램 종료
#         ''')
#         if choice == 'Q':
#             print('DB관련 프로그램을 종료합니다.')
#             i = dbMenuChoice(choice)
#         else:
#             dbMenuChoice(choice)


# def dbMenuChoice(choice):
#     if choice == 'I':
#         uploadDB()
#     elif choice=="V":
#         viewData()
#     elif choice=="Q":
#         return False

# Gevolution 사이트 연동하여 필요한 데이터 크롤링하는 함수
def getWebdata(choice):
    print('웹 크롤링을 시작합니다.')
    # 발급된 계정의 인증키
    GEVOLUTION_API_KEY = 'MNOP826189'
    # g:구글플레이, a:애플 앱스토어
    market = choice.lower()
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
    
    game_df = makeDataFrame(doc, rank)
    checkData(game_df)



# 크롤링한 데이터로 데이터프레임 생성하는 함수
def makeDataFrame( doc, rank ):
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

# 크롤링 후 다음 단계를 실행하는 함수
def nextStage(state, *game_df):
    if state == 'ok':
        print('DB에 수집한 데이터를 적재합니다.')
        uploadDB(game_df)
        sys.exit(1)
    else:
        print('처음으로 돌아갑니다.')
        crawlMenuShow()


# 크롤링한 데이터가 사용자가 원하는 데이터가 맞는지 개수를 확인하는 함수
def checkData(game_df):
    print('데이터의 개수가 맞는지 확인합니다.')
    if len(game_df) == 100:
        print('게임랭킹데이터가 100개 수집되었습니다.')
        choice2 = str(input('다음 단계를 실행하려면 ok를 입력해주세요.'))
        if choice2 == 'ok':
            nextStage('ok', game_df)
        else:
            nextStage('no')
    else:
        print('게임랭킹데이터의 개수가 100개가 아닙니다.')
        game_df = None
        nextStage('restart', game_df)



# insert sql문 실행하는 함수
def insertData( game_df, i ):# aid,ranking,lastWeek,rating,gameName,publisher ):
    with conn.cursor() as cursor:
        sql = 'insert into tbl_game (aid,ranking,lastWeek,rating,gameName,publisher) values(%s, %s, %s, %s, %s, %s);'
        cursor.execute( sql, (game_df['aid'][i],game_df['ranking'][i],
                game_df['lastWeek'][i],game_df['rating'][i],game_df['gameName'][i],game_df['publisher'][i]) )
    # 디비 반영
    conn.commit()
    # 영향받은 row의 수
    return conn.affected_rows()

# DB에 데이터를 적재하는 함수
def uploadDB(game_df):
    for i in range(len(game_df[0])):
        insertData(game_df[0], i)
    closeDB()
    print('게임랭킹데이터를 DB에 적재완료했습니다.')


#사용자에게 검색하고자 하는 제작사를 입력받는 함수
def inputPublisher():
    publisher = input('검색하고자하는 제작사를 입력해주세요.')
    return publisher

# 사용자에게 입력받은 제작사로 select문 실행하는 함수 
def selectData( publisher ):
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





crawlMenuShow()
