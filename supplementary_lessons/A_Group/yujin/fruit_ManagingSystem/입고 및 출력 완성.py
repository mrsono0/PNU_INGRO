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
            U - 과일 재고 정보 수정 # 목록 자체를 수정할지 이전 입고/재고를 취소하고 다시하게 할지 미정
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
            try:
                #fruitinfo['indate']=datetime.strptime(fruitinfo['indate'], '%Y%m%d').date()
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
        self.fruitslist.reset_index(inplace=True)
        print(self.fruitslist)

        
    def curSearch(self):
        print("현재 과일 재고 현황입니다") 
        print(self.fruitslist)

        
    # def updateData(self): 
    #     while True:
    #         choice1=input('수정하시려는 고객 정보의 이메일을 입력하세요 : ')
    #         idx=0
    #         for i in range(0,len(self.custlist)):
    #             if self.custlist[i]['email'] == choice1:
    #                 idx=i
    #         if idx==0:
    #             print('등록되지 않은 이메일입니다.')       
    #             break
                        
    #         choice2=input('''
    #         다음 중 수정하실 정보를 골라주세요 
    #                 name, sex, birthyear
    #         (수정할 정보가 없으면 'exit' 입력)
    #         ''')
    #         if choice2 in ('name','sex','birthyear'):
    #             self.custlist[idx][choice2]=input('수정할 {}을 입력하세요 :'.format(choice2))
    #             break
    #         elif choice2 =='exit':
    #             break
    #         else:
    #             print('존재하지 않는 정보입니다.')
    #             break



    def OutData(self):
        # outfruitinfo={'fruitname':'','inprice':'',"count":'',"indate":'','expirdate':''}
        while True:
            outfruitname=str(input("과일명을 입력하세요 : "))
            idx=0
            # for i in range(0,len(self.fruitslist.index)):
            if outfruitname in self.fruitslist['fruitname']:
                idx=1
            if idx==0:
                print('입고되지 않은 과일입니다.')       
                break
                
            # inprice=input("출고가(단위 : 원)를 입력하세요 : ")
            # try:
            #     inprice=int(inprice)
            # except:
            #     print('숫자만 입력해주세요')
            # else:
            #     if inprice >= 0:
            #         inpriceli.append(inprice)
            #         fruitinfo['inprice']=inpriceli
            #         break
            #     else:
            #         print('0원 이상만 입력 가능합니다')

        while True: 
            outcount=input("수량을 입력하세요 : ")
            try:
                outcount=int(outcount)
            except:
                print('숫자만 입력해주세요')
            else:
                if outcount < self.fruitslist.loc['fruitname'==outfruitname,'count']:
                    break
                else:
                    print('현재 재고보다 많이 입력 하셨습니다')                

        # while True:
        #     indateli=[]
        #     indate=input("출고일을 입력해주세요 : (예 : 20180601)")    
        #     try:
        #         #fruitinfo['indate']=datetime.strptime(fruitinfo['indate'], '%Y%m%d').date()
        #         int(indate)
        #     except:
        #         print('숫자만 입력해주세요')
        #     else:
        #         if len(indate)==8:
        #             indateli.append(indate)
        #             fruitinfo['indate']=indateli
        #             break
        #         else:
        #             print('형식에 맞게 입력해주세요 (예 : 20180601)')

        # while True: # 우선은 입력할 때와 같은 값으로 입력해주고 추후에 입력하지 않아도 되도록 수정
        #     expirdateli=[]
        #     expirdate=input("유통기한(단위 : 일)을 입력하세요 : ")
        #     try:
        #         expirdate=int(expirdate)
        #     except:
        #         print('숫자만 입력해주세요')
        #     else:
        #         if expirdate >= 1:
        #             expirdateli.append(expirdate)
        #             fruitinfo['expirdate']=expirdateli
        #             break
        #         else:
        #             print('1일 이상만 입력 가능합니다')    

        # choice1 = input('삭제하려는 고객 정보의 이메일을 입력하세요.')


        # 입력받은 과일명에 일치하는 인덱스에 입력받은 수량만큼 깐다
        # 수량이 0이되면 리스트에서 제거한다
        outok = 0
        for i in self.fruitslist.index:
            while self.fruitslist['fruitname'][i] == outfruitname:
                # 과일명 일치 되었다
                # 수량 까자
                self.fruitslist.loc[self.fruitslist['fruitname']==outfruitname, count] = 
                self.fruitslist.loc[self.fruitslist['fruitname']==outfruitname, count] - outcount
                if self.fruitslist.loc[self.fruitslist['fruitname']==outfruitname, count] == 0:
                    # self.fruitslist[self.fruitslist['fruitname']==outfruitname].remove()
                    self.fruitslist.drop(self.fruitslist[self.fruitslist['fruitname']==outfruitname])


                print('{} 고객님의 정보가 삭제되었습니다.'.format(self.fruitslist[i]['name']))
                del self.fruitslist[i]
                print(self.fruitslist)
                delok = 1
                break
            
            if delok == 1:
                break

        if delok == 0:
                print('등록되지 않은 이메일입니다.')

    def exe(self,choice):
            if choice=='I':
                self.insertData()
                
            elif choice=='C':
                self.curSearch()

            elif choice=='U':
                self.updateData()
            
            elif choice=='O':
                self.OutData()
            
            elif choice=='Q':
                quit()

    def __init__(self):
        while True:
            self.exe(self.firstinput())

                
FruitsManager()


