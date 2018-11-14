import pymysql as my
import pandas as pd

class DBMgr:
    def __init__(self):
        self.initDB()
        self.load_data()

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
        self.df_box = pd.read_sql('select gameName, ranking, lastWeek, rating, datetime from game_info', self.conn,
                             index_col=['ranking'])
        print('로드완료')
        return self.df_box


    def gap_data(self, game_count=5): # 일반화 보정이 많이 필요
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
        return print(gap_dic)


    def long_live_data(self): # 잔류
        pass
        """
            try:
                self.initDB()
                pass
                # 3. 쿼리 획득 및 수행 
                
                with self.conn.cursor() as cursor:
                    sql ='''
                        
                        '''
                    cursor.execute(sql)
                    self.conn.commit()
                    result =

            except Exception as e:
                result = None
                print('에러 ->', e)
            
            if self.conn: # None 도 그 자체 불린은 false임.
                self.conn.close()
            #결과 리턴 : 튜플로 리턴 -> 리턴할 내용을 열거하면 된다.
            return result
        """

    def mixed_score(self):  # 랭킹+평점 혼합점수 순위
        pass
        
        
if __name__ != '__main__':
    load = DBMgr()
    load.load_data()
    print('데이터로드 끝')
