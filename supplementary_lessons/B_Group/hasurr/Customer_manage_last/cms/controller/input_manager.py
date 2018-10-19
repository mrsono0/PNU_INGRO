import re
from cms.view import Viewer


"""
정보 입력 받는 함수
"""


viewer = Viewer()

class InputManager():
    name = None  # 사용자의 이름
    ident_num = None  # 사용자의 주민등록 번호
    gender = None  # 사용자의 성별
    email = None  # 사용자의 이메일
    birth = None  # 사용자의 생일
    user_input = None  # 다음단계 선택

    # 정보 입력 함수
    def set_name(self):
        name = ''
        while name is not True:
            name = input("이름 : ")
            if not re.match(r'[ㄱ-힣]', name):
                viewer.say_validation('이름')
            else:
                break
        return name


    def set_identnum(self):
        ident_num = None
        while ident_num is not True:
            ident_num = input("주민등록 번호를 입력하세요 (123456-1234567) :")
            if not re.match(
                    r'^(?:[0-9]{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[1,2][0-9]|3[0,1]))-[1-4][0-9]{6}$',
                    ident_num):
                viewer.say_validation('주민등록번호')
            else:
                break
        return ident_num


    def set_gender(self):
        gender = False
        while gender is not True:
            gender = input('성별 (M 또는 F) : ')
            if gender.upper() == 'M' or gender.upper() == 'F':
                break
            else:
                viewer.say_validation('성별')
        return gender


    def set_email(self):
        email = None
        while email is not True:
            email = input('이메일 (형식 : a@a.com) : ')
            if len(email) > 6:
                if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    viewer.say_validation('이메일')
                else:
                    break
        return email


    def set_birth(self):
        birth = None
        while birth is not True:
            birth = input('생년월일(ex. 940915) :')
            if len(birth) == 6:
                if not re.match(r"[0-9]", birth):
                    viewer.say_validation('생년월일')
                else:
                    break
            else:
                viewer.say_validation('생년월일')
        return birth


    # 다음 스텝 입력받는 함수
    def what_next_step(self, flag=''):
        if flag:
            flag = flag.lower()

        valid = False
        if flag.lower() == 'last':
            steps = ['N', 'U', 'Z']
        elif flag.lower() == 'first':
            steps = ['P', 'U', 'Z']
        else:
            steps = ['P', 'N', 'U', 'Z']

        while valid is False:
            u_i = input('입력 : ')
            user_input = u_i.upper()
            if user_input in steps:
                valid = True
                return user_input
            else:
                viewer.say_validation('스텝')

