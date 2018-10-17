# **콘솔형 과일 재고 관리 프로그램**

import re
import datetime

fruit = {'fruit_name':'','in_price':0,'out_price':0,'quantity':0,'in_date':'','exp_date':'','disc_rate':0}
fruitlist=[]
def selectChoice(self):
    self.i = True
    while self.i:
        self.choice=input('''
        다음 중에서 하실 일을 골라주세요 :
        I - 과일 정보 입력
        U - 과일 정보 수정
        C - 과일 재고 조회
        S - 과일 출고 (판매)
        D - 과일 재고 정리
        Q - 프로그램 종료
        ''')
        if self.choice == 'Q':
            self.i = self.frmChoice(self.choice)
        else:
            self.frmChoice(self.choice)


def frmChoice(self, choice):
    if choice == 'I':
        self.insertFruit()
    # elif choice=="U":
    #     self.updateFruit()
    # elif choice=="C":
    #     self.checkFruit()
    # elif choice=="S":
    #     self.sellFruit()
    # elif choice=="D":
    #     self.deleteFruit()
    elif choice=="Q":
        return False


def insertFruit(self):
    fruit = {'fruit_name':'','in_price':0,'out_price':0,'quantity':0,'in_date':'','exp_date':'','disc_rate':0}
    fruit['fruit_name']=str(input("과일명을 입력하세요 ( 한글로 ): "))
    fruit['in_price'] = float(input('과일의 입고가격을 입력하세요.'))
    fruit['out_price'] = fruit['in_price']*1.5
    fruit['quantity'] = int(input('입고된 과일의 수량을 입력하세요.'))
    now = datetime.datetime.now()
    fruit['in_date'] = now.strftime('%Y-%m-%d %H:%M')
    keep_days = int(input('이 과일의 최대 보관일수를 입력해주세요. 예)3일이면 3'))
    fruit['exp_date'] = (now + datetime.timedelta(days=keep_days)).strftime('%Y-%m-%d %H:%M')
    fruitlist.append(fruit)
    print(self.fruitlist)



# 1. 데이터
# > 입고시 아래의 변수를 포함하여 입력.
# - 과일 :  
# > 한정되어 있지 않음.  
# > 입력 시 새로운 키 값으로 딕셔너리에 추가.
# - 가격(입고가/출고가) :  
# > 입고 가격과 출고 가격이 다름.  
# > 입고와 출고시 각각 다른 가격 입력.  
# > 입고가 < 출고가 여야함.
# - 수량 : 
# - 입고일 :  
# > 과일이 입고된 날짜를 기록.
# - 유통기한 :  
# > 한번에 같이 입고된 과일은 같은 유통기한을 부여.  
# > 단, 과일별 유통기한은 다름.  
# > 입고일에 유통기한 일수를 더하여 생성.
# - (+ 할인율) :  
# > 유통기한 임박 제품에 부여.  
# > 초기에는 0이었다가, 유통기한 임박시 증가.  
# > 값 부여 시점 정해야(ex.유통기한 1일전)
# - (+ ID?) :  
# > 총 과일의 개수만 세는 것이 아니라 유통기한이 다 다른 과일이 입력되므로 1개씩 개별 데이터로 보게 될 시 필요.  
# > 자동 생성.

# 2. 기능
# - 입고 :  
# > 창고에 과일이 들어옴.  
# > 입고시 과일명, 입고가, 수량, 유통기한 등을 입력함.
# - 수정 :  
# > 입고 및 출고 변수 값 수정
# - 출고(판매) :  
# > 창고에 있던 과일이 판매됨.  
# > 0개인 과일은 출고 불가.  
# > 출고시 과일명, 출고가, 수량 등이 입력됨.  
# > (+ 유통기한 임박 제품 판매시 할인율이 적용하여 출고가격이 생성됨.)
# - 할인 :  
# > 유통기한이 임박한 상품에 할인율 변수 값을 증가시킴.
# - 처리 :  
# > 유통기한에 도달한 상품을 창고에서 버림.
# - 재고 확인 :  
# > 현재 창고 내에 있는 과일들의 이름, 입고가, 수량, 유통기한, 할인율, ID 등의 리스트를 보여준다.  
# > 유통기한이 임박한 순 혹은 입고일이 빠른 순으로 sorting 한다.


# 3. 구현
# > - 입력시 딕셔너리로
# > - 입력 후 append는 dataframe에
# > - FIFO
# > - 위 데이터 설명 내의 변수들이 컬럼값
# > - 고유값 생성 필요없이 index가 id로?
# > - 파일로 저장하여 콘솔 종료 후에도 입력 값이 남도록 한다
# > - 콘솔 시작 시에는 저장된 파일을 불러와서 이용한다


