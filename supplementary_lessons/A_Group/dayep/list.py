'''
이름, 성별, 이메일, 출생년도 : 고객정보를 입력 받아야 해
자료 구조 : 딕셔너리
저장소 : 리스트
'''
customer={'name':'','sex':'',"email":'',"birthyear":''}
custlist=[]

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
    page=0

    if choice=="I":        
        customer={'name':'','sex':'',"email":'',"birthyear":''}
        customer['name']=str(input("이름입력^_^ : "))
        
        while True:
            customer['sex']=str(input("성별 입력 : "))
            if customer['sex'] in ('M','F','m','f'):
                break

        while True:
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

    elif choice=="C":
        page=len(custlist)-1
        print("현재 페이지 입니다")
        print(custlist[page])

    elif choice == 'P':
        page -= 1
        if page==0:
            print('첫페이지입니다.')
            print(custlist[page])
        elif page==(len(custlist)-1):
            print('마지막페이지입니다.')
            print(custlist[page])
        else:
            print('이전페이지입니다.')
            print(custlist[page])

    elif choice == 'N':
        page += 1
        if page==0:
            print('첫페이지입니다.')
            print(custlist[page])
        elif page==(len(custlist)-1):
            print('마지막페이지입니다.')
            print(custlist[page])
        else:
            print('다음페이지입니다.')
            print(custlist[page])


    elif choice=='D':
        pass

    elif choice=="U":
        pass

    elif choice=="Q":
        break
