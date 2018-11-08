# from app3 import *
import app3
import main3 

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
            app3.Model.loading(Model,rankType,batch)

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
        else:                   
            main3.getData(rankType)



    # 받아온 데이터 보여주고 확인하기
    def check(doc_df2):
        print(doc_df2.head())
        checking=input('''
        원하는 랭킹 데이터가 맞습니까?
        예 : y 아니오 : n
        ('예' 선택 시 DB에 적재)
        ''')
        if checking =='y':
            app3.Model.genrestruc(doc_df2)
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
                app3.Model.loading(Model,rankType)


