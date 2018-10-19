# import regular expression module for input validattion
import re


"""
정보 입력 받는 함수
"""


# 정보 입력 함수
def set_name():
    name = ''
    while name is not True:
        name = input("이름 : ")
        if not re.match(r'[a-zA-Zㄱ-힣]', name):
            print("올바른 이름입력이 아닙니다. 다시 시도해주세요")
        else:
            break
    return name


def set_identnum():
    ident_num = None
    while ident_num is not True:
        ident_num = input("주민등록 번호를 입력하세요 (123456-1234567) :")
        if not re.match(
                r'^(?:[0-9]{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[1,2][0-9]|3[0,1]))-[1-4][0-9]{6}$',
                ident_num):
            print('올바른 주민등록 번호가 아닙니다.')
        else:
            break
    return ident_num


def set_gender():
    gender = False
    while gender is not True:
        gender = input('성별 (M 또는 F) : ')
        if gender.upper() == 'M' or gender.upper() == 'F':
            break
        else:
            print("올바른 성별입력이 아닙니다. 다시 시도해주세요")
    return gender


def set_email():
    email = None
    while email is not True:
        email = input('이메일 (형식 : a@a.com) : ')
        if len(email) > 6:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                print("올바른 이메일이 아닙니다. 다시 시도해주세요")
            else:
                break
    return email


def set_birth():
    birth = None
    while birth is not True:
        birth = input('생년월일(ex. 940915) :')
        if len(birth) == 6:
            if not re.match(r"[0-9]", birth):
                print('올바른 생년월일이 아닙니다. 다시 시도해주세요.')
            else:
                break
        else:
            print('올바른 생년월일 입력이 아닙니다. 다시 시도해주세요.')
    return birth


# 다음 스텝 입력받는 함수
def what_next_step():
    valid = False
    while valid is False:
        print('**%s / %s**' % (idx + 1, len(list_information)))
        print('P : 다음 고객 정보')
        print('N : 이전 고객 정보')
        print('U : 정보 수정')
        print('Z : 첫  화  면')
        u_i = input('입력 : ')
        user_input = u_i.upper()
        steps = ['P', 'N', 'U', 'Z']
        if user_input in steps:
            valid = True
            return user_input
        else:
            print('입력이 틀렸습니다. 다시입력해 주세요.')


def what_next_step_last():
    valid = False
    while valid is False:
        print('**마지막 고객입니다. %s / %s**' % (idx + 1, len(list_information)))
        print('N : 이전 고객 정보')
        print('U : 정보 수정')
        print('Z : 첫  화  면')
        u_i = input('입력 : ')
        user_input = u_i.upper()
        steps = ['N', 'U', 'Z']
        if user_input in steps:
            valid = True
            return user_input
        else:
            print('입력이 틀렸습니다. 다시입력해 주세요.')


def what_next_step_first():
    valid = False
    while valid is False:
        print('**처음 고객입니다. %s / %s**' % (idx + 1, len(list_information)))
        print('P : 다음 고객 정보')
        print('U : 정보 수정')
        print('Z : 첫  화  면')
        u_i = input('입력 : ')
        user_input = u_i.upper()
        steps = ['P', 'U', 'Z']
        if user_input in steps:
            valid = True
            return user_input
        else:
            print('입력이 틀렸습니다. 다시입력해 주세요.')


"""
기능함수
"""


# 입력받은 정보 딕셔너리에 넣는 함수
def insert_inform_to_dict(name, gender, email, birth, ident_num):
    dict_information = {}
    dict_information['name'] = name
    dict_information['gender'] = gender
    dict_information['email'] = email
    dict_information['birth'] = birth
    dict_information['ident_num'] = ident_num
    return dict_information



# 고객 수정 - 지금 열람중인 정보 바꾸기
def adjust_inform(idx):
    print('수정할 정보를 입력하세요 :')
    name = set_name()
    gender = set_gender()
    email = set_email()
    birth = set_birth()
    ident_num = set_identnum()

    list_information[idx] = insert_inform_to_dict(name,
                        gender, email, birth, ident_num)


# 고객 수정 - 입력받은 주민번호와 일치하는 정보 찾아바꾸기
def modify_inform(name, ident_num):
    iscorrect_ident = False            
    for i in range(0, len(list_information)):
        iscorrect_ident = False
        if ident_num in list_information[i]['ident_num']:
            iscorrect_ident = True

        if iscorrect_ident is True:
            print('%s 고객의 수정입니다.' % name)
            adjust_inform(i)
            print("수정된 고객의 정보입니다.")
            get_inform(i)
            break
    if iscorrect_ident is False:
        print('\n없는 고객정보입니다.\n')


# 고객 정보 삭제 함수
def del_infrom(name, ident_num):
    iscorrect_ident = False

    for i in range(0, len(list_information)):
        iscorrect_ident = False
        if ident_num in list_information[i].values():
            iscorrect_ident = True

        if iscorrect_ident is True:    
            print('\n%s 님은 삭제 되었습니다.\n' % name)
            del list_information[i]
            break
    if iscorrect_ident is False:
        print('\n없는 고객 정보입니다.\n')
        

"""
출력 함수
"""


# 고객 정보 조회 출력 함수
def get_inform(index=0):
    print('')
    print('이    름 : ', list_information[index].get('name'))
    print('성    별 : ', list_information[index].get('gender'))
    print('이 메 일 : ', list_information[index].get('email'))
    print('출생년도 : ', list_information[index].get('birth'))
    print('')


# 인트로 출력 함수
def say_hello():
    print('='*50)
    print('{:^40}'.format('고객 관리 프로그램'))
    print('='*50)
    print("고객의 정보는 이름, 성별, 이메일, 출생년도를 저장합니다.")
    print("할 일을 선택하십시오.")
    print("""
    1. 고객정보입력
    2. 고객정보조회
    3. 고객정보수정
    4. 고객정보삭제
    0. 프로그램종료
                """)


# 고객 정보 출력 - 다음 고객 정보
def next_information(idx):
    idx += 1
    get_inform(idx)
    return idx


# 고객 정보 출력 - 이전 고객 정보
def previous_information(idx):
    idx -= 1
    get_inform(idx)
    return idx


"""
프로그램 시작
"""


if __name__ == '__main__':
    # 모든 고객 정보 담을 리스트 선언
    # 테스트용 데이터
    list_information = [
        {
            'name': '강화수',
            'ident_num': '940915-1111111',
            'gender': 'f',
            'email': 'a@a.com',
            'birth': '123456'},
        {
            'name': '홍길동',
            'ident_num': '931204-1222222',
            'gender': 'm',
            'email': 'd@d.com',
            'birth': '123456'}
        ]

    while True:
        idx = 0
        # 인덱스 초기화
        information = {
                'name': '',
                'ident_num': '',
                'gender': '',
                'email': '',
                'birth': ''
        }  # 각 고객 정보를 담을 딕셔너리 초기화

        say_hello()
        select = input("입력 : ")
        if select == '0':
            print('\n이용해 주셔서 감사합니다.\n')
            break
        if select == "1":
            print('='*15, '고객 정보 입력', '='*15)
            name = set_name()
            gender = set_gender()
            email = set_email()
            birth = set_birth()
            ident_num = set_identnum()

            information = insert_inform_to_dict(
                name, gender, email, birth, ident_num)
            # 입력 받은 정보 딕셔너리 형태로 저장
            list_information.append(information)
            # 전체 고객 정보 리스트에 입력받은 고객의 딕셔너리 추가
            print('\n%s 고객님의 정보가 입력되었습니다.\n' % name)

        if select == '2':
            if not list_information:
                print('\n고객정보가 하나도 없습니다!\n')
            else:
                print('==========고객 정보 조회==========')
                get_inform(idx)  # 첫 고객 정보 조회
                while True:
                    # 고객 정보의 인덱스에 따라 다른 선택지를 가진 인터페이스 제공
                    if idx == len(list_information)-1:
                        next_step = what_next_step_last()
                    elif idx <= 0:
                        next_step = what_next_step_first()
                    else:
                        next_step = what_next_step()

                    # 선택에 따른 함수 수행
                    if next_step == 'P':
                        idx = next_information(idx)

                    if next_step == 'N':
                        idx = previous_information(idx)

                    if next_step == 'U':
                        adjust_inform(idx)
                        print("수정된 고객의 정보입니다.")
                        get_inform(idx)

                    if next_step == 'Z':
                        break

        if select == '3':
            if list_information:
                print('='*15, '고객 정보 수정', '='*15)
                print('수정할 고객의 이름과 주민등록번호를 입력.')
                name = set_name()
                ident_num = set_identnum()
                modify_inform(name, ident_num)
            else:
                print('\n고객정보가 하나도 없습니다!\n')

        if select == '4':
            if list_information:
                print('='*15, '고객 정보 삭제', '='*15)
                print('삭제할 고객의 이름과 주민등록번호를 입력.')
                name = set_name()
                ident_num = set_identnum()
                del_infrom(name, ident_num)
            else:
                print('\n고객정보가 하나도 없습니다!\n')