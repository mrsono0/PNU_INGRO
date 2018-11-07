import re
import pandas as pd
import numpy as np
from datetime import datetime

class FruitsManager:
    fruitslist=pd.DataFrame(columns=('fruitname','inprice','count','indate','expirdate'))
    
    def firstinput(self):
        choice=input('''
            다음 중에서 하실 일을 골라주세요 :
            I - 과일 입고 목록 입력
            C - 과일 재고 현황 보기
            O - 과일 출고 목록 입력
            Q - 프로그램 종료
            ''')  
        return choice

    def insertData(self): 
        fruitinfo={'fruitname':'','inprice':'',"count":'',"indate":'','expirdate':''}
        while True:
            fruitnameli=[]
            fruitname=str(input("과일명을 입력하세요 : "))
            fruitnameli.append(fruitname)
            fruitinfo['fruitname']=fruitnameli            
            break
            
        while True:
            inpriceli=[]
            inprice=input("입고가(단위 : 원)를 입력하세요 : ")
            try:
                inprice=int(inprice)
            except:
                print('숫자만 입력해주세요')
            else:
                if inprice >= 0:
                    inpriceli.append(inprice)
                    fruitinfo['inprice']=inpriceli
                    break
                else:
                    print('0원 이상만 입력 가능합니다')

        while True: 
            countli=[]
            count=input("수량을 입력하세요 : ")
            try:
                count=int(count)
            except:
                print('숫자만 입력해주세요')
            else:
                if count >= 0:
                    countli.append(count)
                    fruitinfo['count']=countli
                    break
                else:
                    print('0개 이상만 입력 가능합니다')                

        while True:
            indateli=[]
            indate=input("입고일을 입력해주세요 : (예 : 20180601)")    
            try: # 후에 가능하면 날짜 데이터로 바꾸기 구현
                int(indate)
            except:
                print('숫자만 입력해주세요')
            else:
                if len(indate)==8:
                    indateli.append(indate)
                    fruitinfo['indate']=indateli
                    break
                else:
                    print('형식에 맞게 입력해주세요 (예 : 20180601)')

        while True: 
            expirdateli=[]
            expirdate=input("유통기한(단위 : 일)을 입력하세요 : ")
            try:
                expirdate=int(expirdate)
            except:
                print('숫자만 입력해주세요')
            else:
                if expirdate >= 1:
                    expirdateli.append(expirdate)
                    fruitinfo['expirdate']=expirdateli
                    break
                else:
                    print('1일 이상만 입력 가능합니다')    

        print(fruitinfo)
        df_fruitinfo=pd.DataFrame(fruitinfo)
        self.fruitslist=pd.concat([self.fruitslist,df_fruitinfo],sort=True)
        self.fruitslist.reset_index(drop=True,inplace=True)
        print(self.fruitslist)

        
    def curSearch(self):
        print("현재 과일 재고 현황입니다") 
        print(self.fruitslist)


    def OutData(self):
        idx=True
        while idx:
            outfruitname=str(input("과일명을 입력하세요 : "))
            for fname in self.fruitslist['fruitname']:
                if fname == outfruitname:
                    idx=False
            if idx==True:
                print('입고되지 않은 과일입니다.')
                quit()   # 후에 가능하면 목록 입력으로 돌아가게 만들기    
    

        while True: 
            outcount=input("수량을 입력하세요 : ")
            try:
                outcount=int(outcount)
            except:
                print('숫자만 입력해주세요')
            else: # 두번 이상 가능하도록 후에 수정
                if outcount <= self.fruitslist.loc[self.fruitslist['fruitname']==outfruitname, 'count'][0]:
                    pass
                else:
                    print('현재 재고보다 많이 입력 하셨습니다')                

            for i in self.fruitslist.index:
                while self.fruitslist['fruitname'][i] == outfruitname:
                    self.fruitslist.loc[self.fruitslist['fruitname']==outfruitname, 'count'] = self.fruitslist.loc[self.fruitslist['fruitname']==outfruitname, 'count'] - outcount
                    if self.fruitslist.loc[self.fruitslist['fruitname']==outfruitname, 'count'][0]==0:
                        self.fruitslist.drop(np.where(self.fruitslist['fruitname'] == outfruitname)[0],inplace=True)
                    break

            print('%s가 창고에서 출고 처리되었습니다.' % outfruitname)
            print(self.fruitslist)
            break
    
    def exe(self,choice):
        if choice=='I':
            self.insertData()
            
        elif choice=='C':
            self.curSearch()
        
        elif choice=='O':
            self.OutData()
        
        elif choice=='Q':
            quit()


    def __init__(self):
        while True:
            self.exe(self.firstinput())

                
FruitsManager()



