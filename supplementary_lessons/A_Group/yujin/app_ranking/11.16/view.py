import model_write
import model_read

class View:
    # 적재할 데이터 타입 입력
    def choiceInput():
        batch='console'
        rankType=input(
        '''
            적재할 랭킹 데이터의 어플 종류를 입력해주세요.
            (데이터 로딩까지 약 4분정도 소요됩니다)
            1 : 무료
            2 : 유료
            3 : 매출
            4 : 신규무료
            5 : 신규유료
            q : 프로그램 종료
         ''')
        if rankType=='q':
            quit()
        else:
            doc, load = model_write.Model.loading(model_write.Model,rankType,batch)
            if load == 'ok':
                model_write.Model.makeDataFrame(model_write.Model,doc)
            else:quit()


    # 불러올 데이터 타입 입력
    def choiceOutput():
        rankType=input(
        '''
            불러올 랭킹 데이터의 어플 종류를 입력해주세요.
            1 : 무료
            2 : 유료
            3 : 매출
            4 : 신규무료
            5 : 신규유료
            q : 프로그램 종료
        ''')            
        if rankType=='q':
            quit() 
        elif rankType in ('2','5'):
            visualType=input(
            # 일단 날짜는 제일 최신것으로 고정
            # 후에 일자 지정 및 기간 지정 가능하게 고치기
            '''
                원하는 데이터 시각화 서비스를 선택해주세요.
                1 : 10순위 내 앱 기본 정보
                2 : 50순위 내 앱 장르별 비율
                3 : 50순위 내 가격 범위별 비율
                4 : 앱 평가점수 기준 10순위 내림차순 도표
                q : 프로그램 종료
            ''')  
            if visualType =='1':              
                # 후에 창으로 띄우는 거로 수정해보기     
                model_read.getData.initDB(rankType)
            elif visualType =='2':
                model_read.getData.genreProp(rankType)
            elif visualType =='3':
                model_read.getData.priceHist(rankType)
            elif visualType =='4':
                model_read.getData.scoreDesc(rankType)
            elif visualType =='q':
                quit()
        else:
            visualType=input(
            # 일단 날짜는 제일 최신것으로 고정
            # 후에 일자 지정 및 기간 지정 가능하게 고치기
            '''
                원하는 데이터 시각화 서비스를 선택해주세요.
                1 : 10순위 내 앱 기본 정보
                2 : 50순위 내 앱 장르별 비율
                3 : 앱 평가점수 기준 10순위 내림차순 도표
                q : 프로그램 종료
            ''')  
            if visualType =='1':              
                # 후에 창으로 띄우는 거로 수정해보기     
                model_read.getData.initDB(rankType)
            elif visualType =='2':
                model_read.getData.genreProp(rankType)
            elif visualType =='3':
                model_read.getData.scoreDesc(rankType)
            elif visualType =='q':
                quit()


    # 받아온 데이터 보여주고 확인하기
    def check(doc_df2):
        print(doc_df2.head())
        checking=input(
        '''
            원하는 랭킹 데이터가 맞습니까?
            예 : y 아니오 : n
            ('예' 선택 시 DB에 적재)
        ''')
        if checking =='y':
            model_write.Model.genrestruc(doc_df2)
        else:
            rankType=input(
            '''
                적재할 랭킹 데이터의 어플 종류를 입력해주세요.
                (데이터 로딩까지 약 4분정도 소요됩니다)
                1 : 무료
                2 : 유료
                3 : 매출
                4 : 신규무료
                5 : 신규유료
                q : 프로그램 종료
            ''')            
            if rankType=='q':
                quit()
            else:
                model_write.Model.loading(model_write.Model,rankType)


