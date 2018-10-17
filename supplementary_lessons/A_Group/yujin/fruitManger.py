import re
import pandas as pd
import numpy as np
from datetime import datetime

class FruitsManager:
    fruitslist=pd.DataFrame(columns=('fruitname','inprice','conut','indate','expirdate'))
    
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
            # if len(customer['fruitname'])<=30:
            #     break
            # else:
            #     print('30자 이내로 입력해주세요')
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
                # if fruitinfo['inprice'] in ('M','F'):
                #     break
                # else:
                #     print('M/m 또는 F/f 중 입력해주세요')

        while True: # 여기부터 list화 다시
                fruitinfo['count']=input("수량을 입력하세요 : ")
                try:
                    fruitinfo['count']=int(fruitinfo['count'])
                except:
                    print('숫자만 입력해주세요')
                else:
                    if fruitinfo['count'] >= 0:
                        fruitinfo['count']=list(fruitinfo['count'])
                        break
                    else:
                        print('0개 이상만 입력 가능합니다')                
                # idx=None
                # for i in range(0,len(self.custlist)):
                #     if self.fruitslist[i]['email'] == fruitinfo['email']:
                #         idx=i
                # if idx==None:
                #     regex = re.compile('@')
                #     golbang = regex.search(fruitinfo['email'])
                #     if golbang != None:
                #         break
                #     else :
                #         print('"@"를 포함한 정확한 이메일을 써주세요')
                #     break
                # else:
                #     print('이미 등록된 이메일입니다')       

        while True:
                fruitinfo['indate']=input("입고일을 입력해주세요 : (예 : 20180601)")    
                try:
                    #fruitinfo['indate']=datetime.strptime(fruitinfo['indate'], '%Y%m%d').date()
                    int(fruitinfo['indate'])

                except:
                    print('숫자만 입력해주세요')
                else:
                    if len(fruitinfo['indate'])==8:
                        fruitinfo['indate']=list(fruitinfo['indate'])
                        break
                    else:
                        print('형식에 맞게 입력해주세요 (예 : 20180601)')

        while True: 
                fruitinfo['expirdate']=input("유통기한(단위 : 일)을 입력하세요 : ")
                try:
                    fruitinfo['expirdate']=int(fruitinfo['expirdate'])
                except:
                    print('숫자만 입력해주세요')
                else:
                    if fruitinfo['expirdate'] >= 1:
                        fruitinfo['expirdate']=list(fruitinfo['expirdate'])
                        break
                    else:
                        print('1일 이상만 입력 가능합니다')    

        print(fruitinfo)
        df_fruitinfo=pd.DataFrame(fruitinfo)
        self.fruitslist=pd.concat([self.fruitslist,df_fruitinfo])
        # self.fruitslist.append(fruitinfo)
        print(self.fruitslist)
        # self.page += 1
        '''
    def curSearch(self):
        print("현재 페이지는 {}쪽 입니다".format(self.page + 1)) 
        print(self.custlist[self.page])

    def preSearch(self):
        if self.page <= 0:
            print('첫 번 째 페이지이므로 이전 페이지 이동이 불가합니다')
            print(self.custlist[self.page])
        else:
            self.page -= 1
            print("현재 페이지는 {}쪽 입니다".format(self.page + 1))
            print(self.custlist[self.page])

    def nextSearch(self):
        if self.page >= len(self.custlist)-1:
            print('마지막 페이지이므로 다음 페이지 이동이 불가합니다')
            print(self.custlist[self.page])
        else:
            self.page += 1
            print("현재 페이지는 {}쪽 입니다".format(self.page + 1))
            print(self.custlist[self.page])

    def deleteData(self):
        choice1 = input('삭제하려는 고객 정보의 이메일을 입력하세요.')
        delok = 0
        for i in range(0,len(self.custlist)):
            while self.custlist[i]['email'] == choice1:
                print('{} 고객님의 정보가 삭제되었습니다.'.format(self.custlist[i]['name']))
                del self.custlist[i]
                print(self.custlist)
                delok = 1
                break
            
            if delok == 1:
                break

        if delok == 0:
                print('등록되지 않은 이메일입니다.')
'''
    def exe(self,choice):
            if choice=='I':
                self.insertData()
                
            elif choice=='C':
                self.curSearch()
            
            elif choice=='P':
                self.preSearch()

            elif choice=='N':
                self.nextSearch()

            elif choice=='U':
                self.updateData()
            
            elif choice=='D':
                self.deleteData()
            
            elif choice=='Q':
                quit()

    def __init__(self):
        while True:
            self.exe(self.firstinput())

                
FruitsManager()

