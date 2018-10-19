from cms.controller import *
from cms.model import *
from cms.view import *

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
                get_inform(list_information, idx)  # 첫 고객 정보 조회
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