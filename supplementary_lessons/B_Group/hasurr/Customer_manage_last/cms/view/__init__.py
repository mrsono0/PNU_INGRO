

class Viewer():
    """
    유저 인터페이스 출력 클래스
    """

    # 고객 정보 조회 출력 함수
    def get_inform(self, information, index=0):
        print('')
        print('이    름 : ', information[index].get('name'))
        print('성    별 : ', information[index].get('gender'))
        print('이 메 일 : ', information[index].get('email'))
        print('출생년도 : ', information[index].get('birth'))
        print('')


    # 인트로 출력 함수
    def say_hello(self):
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


    def say_information_UI(self, flag=''):
        print('='*15, '고객 정보 %s' % flag, '='*15)


    def say_get_name_ident(self, flag=''):
        print('%s할 고객의 이름과 주민등록번호를 입력하세요' % flag)
        print('')


    def say_go_update(self):
        print('수정할 정보를 입력하세요.')


    def say_work_done(self):
        print('')
        print('='*15, '작업 완료 되었습니다.', '='*15)
        print('')


    def say_goodbye(self):
        print('\n이용해 주셔서 감사합니다.\n')


    def say_next_step(self, flag=''):
        if flag:
            flag = flag.lower()

        if flag == 'first':
            print("""
        P : 다음 고객 정보
        U : 정보 수정
        Z : 첫  화  면
            """)

        elif flag == 'last':
            print("""
        N : 이전 고객 정보
        U : 정보 수정
        Z : 첫  화  면
            """)

        else:
            print("""
        P : 다음 고객 정보
        N : 이전 고객 정보
        U : 정보 수정
        Z : 첫  화  면
            """)

    
    def say_validation(self, flag=''):
        print("올바른 %s입력이 아닙니다. 다시 시도해주세요" % flag) 


    def say_where_information(self, idx, length, flag=''):
        if flag:
            flag = flag.lower()

        if flag == 'last':
            print('\n**마지막 고객입니다. %s / %s**' % (idx, length))
        elif flag == 'first':
            print('\n**처음 고객입니다. %s / %s**' % (idx, length))
        else:
            print('\n**%s / %s**' % (idx, length))


    def show_customer_information(self, rows=list, idx=int):
        # rows : DB 에 적재된 모든 사용자 객체들이 담긴 리스트
        # idx : 보고자 하는 객체의 순서
        print(rows[idx])