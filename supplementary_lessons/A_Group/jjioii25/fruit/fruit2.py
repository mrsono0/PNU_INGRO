# **콘솔형 과일 재고 관리 프로그램**

import re
import datetime
import pandas as pd

class Fruit:
    fruitlist=[]
    fruit_df = pd.DataFrame(fruitlist, 
    columns=['fruit_name', 'in_price', 'out_price','quantity','in_date','exp_date','disc_rate'])

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
        elif choice=="U":
            self.updateFruit()
        elif choice=="C":
            self.checkFruit()
        elif choice=="S":
            self.sellFruit()
        elif choice=="D":
            self.deleteFruit()
        elif choice=="Q":
            return False


    def insertFruit(self):
        fruit = {'fruit_name':'','in_price':0,'out_price':0,'quantity':0,'in_date':'','exp_date':'','disc_rate':0}
        fruit['fruit_name'] = str(input("과일명을 입력하세요 ( 한글로 ): "))
        fruit['in_price'] = float(input('과일의 입고가격을 입력하세요.'))
        fruit['out_price'] = fruit['in_price']*1.5
        fruit['quantity'] = int(input('입고된 과일의 수량을 입력하세요.'))
        now = datetime.datetime.now()
        fruit['in_date'] = now.strftime('%Y-%m-%d %H:%M')
        keep_days = int(input('이 과일의 최대 보관일수를 입력해주세요. 예)3일이면 3'))
        fruit['exp_date'] = (now + datetime.timedelta(days=keep_days)).strftime('%Y-%m-%d %H:%M')
        self.fruitlist.append(fruit)
        print( self.fruitlist )
        self.fruit_df = pd.DataFrame( self.fruitlist )
        print( self.fruit_df )


    def updateFruit(self):
        # 과일이름 수정
        # 과일의 입고가격 수정
        # 과일의 수량 수정
        # 과일의 최대보관일수 수정
        print('수정')

    def checkFruit(self):
        # 입고일이 빠른 순으로 sorting 한다.
        fruit_df_sort = self.fruit_df.sort_values( by='in_date', ascending=True )
        print('재고확인 : 입고일이 빠른순')
        print(fruit_df_sort)

    def sellFruit(self):
        # > 창고에 있던 과일이 판매됨.  
        # > 0개인 과일은 출고 불가.  
        # > (+ 유통기한 임박 제품 판매시 할인율이 적용하여 출고가격이 생성됨.)
        print('과일 출고(판매)')
        


#### 로직 확인하기
    def deleteFruit(self):
        now = datetime.datetime.now()
        now.strftime('%Y-%m-%d %H:%M')
        self.fruit_df['exp_date'] = ( self.fruit_df['exp_date'] > now ) 
        if not self.fruit_df['exp_date']:
            print('유통기한이 지난 제품을 처분합니다.')



    # 유통기한에 따라 출고가 설정해주는 함수 작성
    # > 유통기한이 임박한 상품에 할인율 변수 값을 증가시킴.



    # 3. 구현
    # > - 입력시 딕셔너리로
    # > - 입력 후 append는 dataframe에
    # > - FIFO
    # > - 위 데이터 설명 내의 변수들이 컬럼값
    # > - 파일로 저장하여 콘솔 종료 후에도 입력 값이 남도록 한다
    # > - 콘솔 시작 시에는 저장된 파일을 불러와서 이용한다


