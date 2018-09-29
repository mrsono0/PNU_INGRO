# 고객 정보 관리 시스템 RFP
# 주요 내용 지금 까지 배운 내용을 토대로 고객의 정보를 관리하는 프로그램을 만듭니다. 
# 고객의 정보를 관리하는 프로그램에서 사용하는 고객 정보를 저장하는 자료구조는 자신 있는 것을 이용합니다.
# 요구사항 - 데이타 고객의 정보는 이름, 성별, 이메일, 출생년도가 있습니다. 고객의 정보를 입력받아 본인이 선택한 자료구조에 저장해야 합니다.
# 이름은 문자열로 저장하며, 성별은 남자는 M, 여자는 F로 저장합니다. 이메일은 문자열로 저장하며, 태어난 연도는 정수로 저장합니다.
# 요구사항 - 기능 고객 관리 프로그램은 고객의 정보를 저장, 조회, 수정, 삭제할 수 있는 기능이 있어야 합니다. 
# 고객 정보를 파일에 저장하는 기능을 구현하지 않아도 됩니다. “I”를 눌러 고객의 정보를 입력받도록 하며, 저장된 고객 정보는 “P” 또는 “N”을 눌러 이전 고객정보 또는 다음 고객정보를 조회할 수 있어야 합니다.
# 조회한 고객 정보는 “U”를 눌러 새로운 정보로 수정할 수 있어야 합니다. “D”를 누르면 조회한 고객 정보를 삭제해야 합니다. 프로그램의 종료는 “Q”를 누릅니다.
# 객체지향 개념을 적용하여 확장성을 고려한 애플리케이션이 되도록 해야 합니다.

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
        customer['name']=str(input("이름입력 : "))
         
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




