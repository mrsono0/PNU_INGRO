from run_batch import openDB, closeDB
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime


# 한글 처리
import platform
from matplotlib import font_manager, rc
# 한글처리
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin': # 맥
    rc( 'font', family='AppleGothic' )
elif platform.system() == 'Windows': # 윈도우
    # 폰트 차후 확인
    fontPath = 'c:/Windows/Fonts/malgun.ttf'
    fontName = font_manager.FontProperties( fname=fontPath ).get_name()
    rc( 'font', family=fontName )
else:
    print( '알 수 없는 시스템. 미적용' )



# 사용자에게 검색하고자 하는 일자와 마켓을 입력받는 함수
def inputMarket():
    # 정규화 적용하기
    market = str(input('검색하고자하는 스토어를 입력해주세요. Google: G, Apple: A'))
    return market

def inputDate():
    # 정규화 적용하기
    date = input('검색하고자하는 일자를 입력해주세요. yyyy-mm-dd 형태로')
    date = date + '%'
    return date


# 사용자에게 입력받은 일자로 select문 실행하는 함수
# select * from tbl_game where market ='G' and regdate like '2018-11-13%'
def selectData(market,date):
    conn = openDB()
    rows = None
    with conn.cursor() as cursor:
        sql = "select * from tbl_game where market =%s and regdate like %s"
        cursor.execute(sql,(market,date))
        rows = cursor.fetchall()
    closeDB()
    return rows


# select문 실행한 결과를 보여주는 함수
def viewData():
    market = inputMarket()
    date = inputDate()
    rows = selectData(market,date)
    return rows, date, market



# 콘솔모드 그래프 시각화 실행하는 함수
def consoleStageGraph():
    rows, date, market = viewData()
    title = '%s %s Top5 Publisher'%(date[:-1], market)
    dir_path = makeDir(date)
    path = '%s/%s'%(dir_path, title)

    df =  pd.DataFrame(rows)
    countPublisher = df['publisher'].value_counts(sort=True, ascending=False)
    
    top5fig = top5PublisherGraph(countPublisher, title, market)
    saveGraph(top5fig, path )

    top5Df = makeTop5Df(countPublisher, df)

    # barplot그릴때 사용할 index값
    indexList = getIndex(countPublisher)

    fig1 = rankingGraph(top5Df, countPublisher, indexList)
    fig2 = ratingGraph(top5Df, countPublisher, indexList)
    
    saveGraph(fig1, path, type='ranking')
    saveGraph(fig2, path, type='rating')


# 배치모드 그래프 시각화하는 함수
def batchStageGraph(market):
    # 오늘 날짜
    sysdt = datetime.datetime.now()
    date = sysdt.strftime('%Y-%m-%d')+'%'
    rows = selectData(market, date)
    title = '%s %s Top5 Publisher'%(date[:-1], market)
    dir_path = makeDir(date, True)
    path = '%s/%s'%(dir_path, title)

    df =  pd.DataFrame(rows)
    countPublisher = df['publisher'].value_counts(sort=True, ascending=False)
    
    top5fig = top5PublisherGraph(countPublisher, title, market)
    saveGraph(top5fig, path )

    top5Df = makeTop5Df(countPublisher, df)

    # barplot그릴때 사용할 index값
    indexList = getIndex(countPublisher)

    fig1 = rankingGraph(top5Df, countPublisher, indexList)
    fig2 = ratingGraph(top5Df, countPublisher, indexList)
    
    saveGraph(fig1, path, type='ranking')
    saveGraph(fig2, path, type='rating')




# 저장디렉토리 생성하는 함수
def makeDir(date, *batch):
    if batch:
        dir_path = './plot/batch/%s' % date[:-1]
    else:
        dir_path = './plot/console/%s' % date[:-1]
    try:
        if not(os.path.isdir(dir_path)):
            os.makedirs(os.path.join(dir_path))
    except OSError as e:
        if e.errno != e.EEXIST:
            print("Failed to create directory!!!!!")
    return dir_path

# 그래프 저장하는 함수
def saveGraph(fig, path, type=None):
    if type:
        fig.savefig(path+'_'+type)
    else:
        fig.savefig(path)


# Top5 게임회사 그래프
def top5PublisherGraph(countPublisher, title, market):
    countDf = pd.DataFrame(countPublisher[:5])
    fig = plt.figure(figsize=(7,7))
    plt.bar(countDf.index, countDf['publisher'], label='%s_Top5'%market, color='b')
    plt.legend()
    plt.title(title)
    return fig




# top5게임회사의 게임들로 데이터 프레임 만드는 함수
def makeTop5Df(countPublisher, df):
    tmp_l = list()
    for i in range(len(countPublisher)):
        tmp_df = df.loc[df.publisher == countPublisher.index[i]]
        tmp_l.append(tmp_df)
    top5Df = pd.concat([tmp_l[i] for i in range(5)])
    return top5Df


# 인덱스값 생성하는 함수 
def getIndex(countPublisher):
    sum = 0
    indexList = [  ]
    for count in countPublisher[:5]:
        sum += count
        indexList.append(sum)
    return indexList




# ranking데이터 시각화
def rankingGraph(top5Df, countPublisher, indexList):
    fig = plt.figure(figsize=(40,20))
    plt.bar(top5Df['gameName'][:indexList[0]], top5Df['ranking'][:indexList[0]].sort_values(), label=countPublisher.index[0])
    plt.bar(top5Df['gameName'][indexList[0]:indexList[1]], top5Df['ranking'][indexList[0]:indexList[1]].sort_values(), label=countPublisher.index[1])
    plt.bar(top5Df['gameName'][indexList[1]:indexList[2]], top5Df['ranking'][indexList[1]:indexList[2]].sort_values(), label=countPublisher.index[2])
    plt.bar(top5Df['gameName'][indexList[2]:indexList[3]], top5Df['ranking'][indexList[2]:indexList[3]].sort_values(), label=countPublisher.index[3])
    plt.bar(top5Df['gameName'][indexList[3]:], top5Df['ranking'][indexList[3]:].sort_values(), label=countPublisher.index[4])
    plt.legend()
    plt.title('Games Ranking Chart')
    # fig.savefig('./plot/%s Games Ranking Chart.png'%(title))
    return fig




# rating데이터 시각화
def ratingGraph(top5Df, countPublisher, indexList):
    fig = plt.figure(figsize=(40,20))
    plt.bar(top5Df['gameName'][:indexList[0]], top5Df['rating'][:indexList[0]].sort_values(ascending=False), label=countPublisher.index[0])
    plt.bar(top5Df['gameName'][indexList[0]:indexList[1]], top5Df['rating'][indexList[0]:indexList[1]].sort_values(ascending=False), label=countPublisher.index[1])
    plt.bar(top5Df['gameName'][indexList[1]:indexList[2]], top5Df['rating'][indexList[1]:indexList[2]].sort_values(ascending=False), label=countPublisher.index[2])
    plt.bar(top5Df['gameName'][indexList[2]:indexList[3]], top5Df['rating'][indexList[2]:indexList[3]].sort_values(ascending=False), label=countPublisher.index[3])
    plt.bar(top5Df['gameName'][indexList[3]:], top5Df['rating'][indexList[3]:].sort_values(ascending=False), label=countPublisher.index[4])
    plt.title('Games Rating Chart')
    plt.legend()
    plt.ylim(50,100)
    # fig.savefig('./plot/%s Games Rating Chart.png'%(title))
    return fig





# 배치함수
def batchRunGraph():
    print('구글플레이스토어 그래프를 저장합니다.')
    batchStageGraph('G')
    print('애플앱스토어 그래프를 저장합니다.')
    batchStageGraph('A')


# 콘솔버전 실행
# consoleStageGraph()

# 배치버전 실행
# batchStageGraph('G')

if __name__ == '__main__':
    print('배치함수실행')
    batchRunGraph()
