import pymysql as my
import pandas as pd
import matplotlib.pyplot as plt
import platform
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin':# 맥
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows': # 윈도우
    # 폰트 차후 확인
    fontPath = 'c:/Windows/Fonts/malgun.ttf'
    fontName = font_manager.FontProperties(fname=fontPath).get_name()
    rc('font', family=fontName )
else:
    print('알수없는 시스템. 미적용')

class DBMgr:
    def __init__(self):
        self.initDB()
        self.load_data()
        self.load_data_all()

    def initDB(self):
        self.conn = my.connect(
                    host = 'localhost',
                    user='root',
                    password='sb0515',
                    db='pythondb',
                    charset='utf8',
                    cursorclass=my.cursors.DictCursor
                    )
        return self.conn

    def load_data(self):
        # DataFrame으로 불러오기
        self.df_box = pd.read_sql('select gameName, ranking, lastWeek, rating, datetime from gev_info1', self.conn,
                             index_col=['ranking'])
        # 최근 5기간만 불러옴.
        self.df_box = self.df_box.tail(100)
        return self.df_box

    def load_data_all(self):
        # 수집된 전체 기간을 다 불러옴.
        self.df_box_all = pd.read_sql('select gameName, ranking, lastWeek, rating, datetime from gev_info1', self.conn,
                                  index_col=['ranking'])
        return self.df_box_all

    def view_data(self):
        # 현재 최근 기간의 상위 20위 게임
        return print(self.df_box.tail(20))

    def gap_data(self, game_count=5):
        '''
        첫 기간 코드
        df_box.loc[df_box['datetime'] == df_box.iloc[0][-1]]

        마지막 기간 코드
        df_box.loc[df_box['datetime'] == df_box.iloc[-1][-1]]
        
        # 앞의 인덱싱이 게임이름을 가리킴 0 -> 1위 1 -> 2위.....
        df_box.iloc[0][0]
        '''
        # 마지막 기간의 20개의 게임만 불러옴.
        df_box_last_per = (self.df_box.loc[self.df_box['datetime'] == self.df_box.iloc[-1][-1]])

        # 순위 차이 계산을 위해서 마지막기간에 게임이 있으면 그 게임이 몇위인지를
        # True 일때 True의 위치를 시리즈를 리스트화하고 리스트에서 값으로 인덱스를 찾음.

        gap_dic = {}
        for n in range(len(df_box_last_per)):
            if any(df_box_last_per['gameName'] == self.df_box.iloc[n][0]):
                rank_gap = list(df_box_last_per['gameName'] == self.df_box.iloc[0][0]).index(True) - n
                if rank_gap >= 0:
                    gap_dic[self.df_box.iloc[n][0]] = rank_gap
                else:
                    gap_dic[self.df_box.iloc[n][0] + '-'] = abs(rank_gap)
                # print('{}의 순위변동 량: {}'.format(df_box.iloc[n][0], rank_gap))
        while len(gap_dic) != game_count:
            minimum = min(gap_dic, key=gap_dic.get)  # Just use 'min' instead of 'max' for minimum.
            del gap_dic[minimum]

        # 시각화
        gap_df = pd.DataFrame.from_dict(gap_dic, orient='index', columns=['순위변동량'])
        plt.figure()
        gap_df['순위변동량'].plot(kind='bar', grid=True, figsize=(10, 10))
        plt.show()
        return print(gap_dic)

    def long_live_data(self):# 범위 기간 중 잔류 기간.
        # 기간을 임의로 설정하고, 해당 기간동안의 잔류 기간을 체크 할 것인가? 혹은
        # 정해진 기간 안의(ex 5주중 x주) 잔류 기간으로 할 것인지.

        # => 지금 구상하는 방법은 아래와같음
        # 총 데이터를 싸그리 다불러온다
        # unique를 이용해서 게임 이름을 싸그리 불러온다.
        # 불러와진 게임이름들을 검색해서
        # 나온 row의 개수를 산정한다.
        """
        과정
        df_box_all['gameName'].unique() => 게임이름들이 array로 불러와짐.
        len(df_box.loc[df_box['gameName'] == 'array들어가는자리']) 하면
        총 기간중 몇기간 동안 잔류하고있는지 확인 가능.
        """
        gamelist = self.df_box_all['gameName'].unique()
        stay_period = {}
        for game in gamelist:
            a_stay_len = len(self.df_box_all.loc[self.df_box_all['gameName'] == game])
            stay_period[game] = a_stay_len

        # 잔류기간 뽑아온거 다시 DataFrame 화
        gap_df = pd.DataFrame.from_dict(stay_period, orient='index', columns=['잔류기간'])
        gap_df = gap_df.sort_values(['잔류기간'], ascending=False) # 내림차순 정리한 잔류기간
        # 시각화
        plt.figure()
        gap_df['잔류기간'].plot(kind='bar', grid=True, figsize=(10, 10))
        plt.show()
        return gap_df

    def mixed_score(self):  # 랭킹+평점 혼합점수 순위
        pass

if __name__ != '__main__':
    load = DBMgr()
    load
