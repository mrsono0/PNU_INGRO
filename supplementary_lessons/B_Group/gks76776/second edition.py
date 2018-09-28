import re

def insert_inform():
    validation = False
    print('=====고객 정보 입력=====')
    # while validation != True:
    name = input("이름 : ")
    # if not re.match(r'[a-zA-Zㄱ-ㅎ]', name):
    #     print("올바른 이름입력이 아닙니다. 다시 시도해주세요")
    # else:
    #     vlaidation = True
    validation = False
    while validation != True:
        ident_num = input("주민등록 번호를 입력하세요 (123456-1234567) :")
        if not re.match(r'^(?:[0-9]{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[1,2][0-9]|3[0,1]))-[1-4][0-9]{6}$', ident_num):
            print('올바른 주민등록 번호가 아닙니다.')
        else:
            validation = True

    validation = False
    while validation != True:
        gender = input('성별 (M 또는 F)) : ')
        if gender.upper() == 'M' or gender.upper() == 'F':
            validation = True
        else:
            print("올바른 성별입력이 아닙니다. 다시 시도해주세요")

    validation = False
    while validation != True:
        email = input('이메일 (형식 : a@a.com) : ')
        if len(email) > 6:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                print("올바른 이메일이 아닙니다. 다시 시도해주세요")
            else:
                validation = True
    return name, gender, email, ident_num

def insert_inform_to_dict(name, gender, email, ident_num):
    customer_information['name'] = name
    customer_information['gender'] = gender
    customer_information['email'] = email
    customer_information['ident_num'] = ident_num
    list_customer_information.append(customer_information)
    return customer_information

def get_customer_number(cus_inf):
    custom_number = -1
    while custom_number== -1:
        name = input("고객의 이름 입력하세요 :")
        ident_num = input("고객의 주민등록 번호를 입력하세요 :")

        for i in range(0, len(cus_inf)):
            if cus_inf[i]['ident_num'] == ident_num and cus_inf[i]['name'] == name:
                custom_number=i
                break
        if custom_number==-1:
                print("고객정보가 없습니다. 이름과 정보를 다시 입력하십시오")
    return custom_number

def select_next_step():
    while True:
        print('P : 다음 고객 정보\n','N : 이전 고객 정보\n','U : 정보 수정\n','D : 정보 삭제\n','Q : 그만')
        u_i = input('입력 : ')
        user_input = u_i.upper()
        if user_input == 'P' or user_input == 'N' or user_input == 'U' or user_input == 'D' or user_input == 'Q':
            return user_input
            break
        else:
            print('입력이 틀렸습니다. 다시입력해 주세요.')

def show_inf(number):
    print('=====고객 정보 조회=====')
    print('이름    : ', list_customer_information[number]['name'])
    print('성별    : ', list_customer_information[number]['gender'])
    print('이메일  : ', list_customer_information[number]['email'])

'''start'''
a=[]
while True:
    print('=' * 50)
    print('고객관리 프로그램입니다.')
    print('=' * 50)
    print("고객의 정보는 이름, 성별, 이메일, 출생년도를 저장합니다.")
    print("할 일을 선택하십시오.(종료를 원한다면 0)")
    print("""
    1. 고객정보입력 
    2. 고객정보조회 및 수정
    3. 그만할려""")
    customer_information = {'name': '', 'ident_num': '123456-1234567', 'gender': 'M', 'email': 'a@a.com'}  # 딕셔너리 초기화
    select = input("입력 : ")
    index_costomer_list = -1

    if bool(a)==False:
        list_customer_information = []
    a=[1]

    if select == "1":
        name, gender, email, ident_num = insert_inform()
        insert_inform_to_dict(name, gender, email, ident_num)
        print('입력되었습니다.')

    elif select == '2':
        if list_customer_information:
            n = get_customer_number(list_customer_information)
            show_inf(n)
            next_step = select_next_step()
            while next_step != 'Q':
                if next_step == 'P':
                    n += 1
                    if n >= len(list_customer_information):
                        print("마지막 고객정보 입니다.")
                        n -= 1
                    else:
                        show_inf(n)  # 다음 조회

                elif next_step == 'N':
                    n -= 1
                    if n < 0:
                        print("처음 고객 정보입니다.")
                        n += 1
                    else:
                        show_inf(n)  # 이전 조회

                elif next_step == 'U':
                    print('수정할 정보를 입력하세요 :')
                    name, gender, email, ident_num = insert_inform()
                    list_customer_information[n] = insert_inform_to_dict(name, gender, email, ident_num)
                    print("수정된 고객의 정보입니다. :")
                    show_inf(n)

                elif next_step == 'D':
                    del list_customer_information[n]
                    break
        else:
            print('고객정보가 하나도 없습니다!')

    elif select == '3':
        break



