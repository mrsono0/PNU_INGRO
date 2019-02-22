import numpy
import pandas

class Popularity_Recommender():
    # 변수 설정
    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.item_id = None
        self.popularity_recommenadations = None
    
    def create(self,train_data, user_id, item_id):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id
        # 트레인 데이터는 듀플 형식으로 정리된 아이템들에 의해 그룹화된다. 이러한 아이템들의 유저의 아이디에서 'count'와 함께 
        # 정리된 정보들이 함께 축적된 것이다.
        # 그리고 인덱스는 리셋된다
        train_data_grouped = train_data.groupby([self.item_id]).agg({self.user_id: 'count'}).reset_index()
        train_data_grouped.rename(columns = {'user_id': 'score'}, inplace = True)
        
        # train data는 스코어에 따라 내림차순으로 정리가 되고, item_id는 올림차순으로 정리가 된다
        train_data_sort = train_data.sort_values(['score', self.item_id], ascending = [0, 1])
        # 새로운 컬럼"Rank"는 오름차순으로 정리된 score에 의해 만들어 진다
        # => Rank 컬럼은 내림차순으로 정리된 score들을 나타내는 것이다
        train_data_sort['Rank'] = train_data_sort['score'].rank(ascending = 0, method = 'first') # first : ranks assigned in order they appear in the array

        # 상위 15개 아이템들은 populraity_Recommender에 저장이 되고, 리턴된다.
        self.popularity_recommenadations = train_data_sort.head(15)

    def recommend(self, user_id):        
        user_recommendation = self.popularity_recommenadations
        user_recommendation['user_id'] = user_id


        # 컬럼 만들기
        cols = user_recommendation.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        user_recommendation = user_recommendation[cols]

        return user_recommendation
        


