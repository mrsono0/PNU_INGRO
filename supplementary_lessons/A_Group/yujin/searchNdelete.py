custlist=[]
page=-1


while True:
    choice=input('''
    다음 중에서 하실 일을 골라주세요 :
    I - 고객 정보 입력
    C - 현재 고객 정보 조회
    P - 이전 고객 정보 조회
    N - 다음 고객 정보 조회
    U - 고객 정보 수정
    D - 고객 정보 삭제
    Q - 프로그램 종료
    ''')  

    if choice=="I":        
        customer={'name':'','sex':'',"email":'',"birthyear":''}
        customer['name']=str(input("이름입력^_^ : "))
         
        while True:
             customer['sex']=str(input("성별 입력 : "))
             if customer['sex'] in ('M','F','m','f'):
                 break
 
        while True: # 중복되지 않게 입력
             customer['email']=str(input("이메일 입력 : "))
             break

        while True:
             customer['birthyear']=input("출생년도 입력 : ")
             if len(customer['birthyear']) == 4:
                 int(customer['birthyear'])
                 break

        print(customer)
        custlist.append(customer)
        print(custlist)
        page += 1

    elif choice=="C":
        print("현재 페이지는 {}쪽 입니다".format(page + 1)) 
        print(custlist[page])

    elif choice == 'P':
        if page <= 0:
            print('첫번 째 페이지입니다')
            print(custlist[page])
        else:
            page -= 1
            print("현재 페이지는 {}쪽 입니다".format(page + 1))
            print(custlist[page])
            
    elif choice == 'N':
        if page >= len(custlist)-1:
            print('마지막 페이지입니다')
            print(custlist[page])
        else:
            page += 1
            print("현재 페이지는 {}쪽 입니다".format(page + 1))
            print(custlist[page])

    elif choice=='D':
        choice1 = input('삭제하려는 이메일을 입력하세요.')
        delok = 0
        idx=0
        for i in range(0,len(custlist)):
            while custlist[i]['email'] == choice1:
                idx=i
                print('{}고객님의 정보가 삭제되었습니다.'.format(custlist[idx]['name']))
                del custlist[idx]
                print(custlist)
                delok = 1
                break
            
            if delok == 1:
                break

        if delok == 0:
                print('등록되지 않은 이메일입니다.')

    elif choice=="U": 
        while True:
            choice1=input('''수정하시려면 이메일을 입력하세요.''') # 이메일 존재 여부 체크 필요
            choice2=input('''
            다음 중에서 바꾸고싶은 정보를 골라주세요 :
            name, sex, birthyear
            (바꾸고 싶은 게 없으면 exit)
            ''')
            idx=0
            for i in range(0,len(custlist)):
                if custlist[i]['email'] == choice1:
                    idx=i
            if choice2 in ('name','sex','birthyear'):
                custlist[idx][choice2]=input('바꾸려는 {}을 입력하세요.'.format(choice2))
                # 바꾼 뒤 자동으로 exit 되는게 필요
            else: 
                break

    elif choice=="Q":
        break
