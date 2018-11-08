from app3 import *
from main3 import *
from view import *

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
        Model('1',batch)
        # Model('2',batch)
        # Model('3',batch)                
        # Model('4',batch)
        # Model('5',batch)                
        



# Model.check(Start())



if __name__ == '__main__':
    if sys.argv[1] == '1':
        Start.batchver()
    else:
        Start.consolever()


# 오늘 넣고보니 apptype=5의 price에 null 존재
# -> 신규 유료라 한시적 무료 제공 혹은 가격 표시 자체가 없는 데이터(<- 애초에 api에서 줄때부터 잘못)












