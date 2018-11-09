from app3 import *
from main3 import *
from view import *
import sys

# 콘솔창에서 디비에 적재할지 꺼낼지 여부 먼저 판단


class Start:
    # 수행할 기능 선택
    def consolever():
        whatExe=input(
        '''
            수행할 기능을 입력해주세요.
            r : DB 데이터 불러오기
            w : DB 데이터 적재
            q : 프로그램 종료
        ''')
        if whatExe=='q':
            quit()
        elif whatExe =='r':
            View.choiceOutput()
        elif whatExe =='w':  
            View.choiceInput()      

    def batchver():
        batch='batch'
        doc, load= Model.loading(Model,'1',batch)
        if load == 'ok':
            Model.makeDataFrame(Model,doc)
            print('랭킹 타입 1 적재 완료')
        else:pass


        doc, load=Model.loading(Model,'2',batch)
        if load == 'ok':
            Model.makeDataFrame(Model,doc)
            print('랭킹 타입 2 적재 완료')

        else:pass        

        doc, load=Model.loading(Model,'3',batch)                
        if load == 'ok':
            Model.makeDataFrame(Model,doc)
            print('랭킹 타입 3 적재 완료')

        else:pass        

        doc, load=Model.loading(Model,'4',batch)
        if load == 'ok':
            Model.makeDataFrame(Model,doc)
            print('랭킹 타입 4 적재 완료')

        else:pass        

        doc, load=Model.loading(Model,'5',batch)                
        if load == 'ok':
            Model.makeDataFrame(Model,doc)
            print('랭킹 타입 5 적재 완료')

        else:pass        



if __name__ == '__main__':
    if sys.argv[1] == '1':
        Start.batchver()
    else:
        Start.consolever()


# 오늘 넣고보니 apptype=5의 price에 null 존재
# -> 신규 유료라 한시적 무료 제공 혹은 가격 표시 자체가 없는 데이터(<- 애초에 api에서 줄때부터 잘못)












