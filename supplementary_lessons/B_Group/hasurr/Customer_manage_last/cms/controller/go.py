from cms.controller import connectDB

"""
실행 로직
"""

def gogosing(viewer, im, dao):

    while True:
        viewer.say_hello()  # 첫 화면 출력
        select = input("입력 : ")  # 할 일 입력 받음

        if select == '0':
            viewer.say_goodbye()  # 프로그램 종료
            break

        if select == "1":
            viewer.say_information_UI('입력')
            # 고객 정보 입력 받음
            name = im.set_name()
            gender = im.set_gender()
            email = im.set_email()
            birth = im.set_birth()
            ident_num = im.set_identnum()

            connectDB.insert_information(dao, name, gender, email, birth, ident_num)  # DB에 입력

            viewer.say_work_done()

        if select == '2':
            viewer.say_information_UI('조회')            
            rows = connectDB.select_information(dao)  # DB의 모든 데이터를 리스트로 가져옴
            idx = 0  # 모든 고객의 정보 중 하나씩 접근하기 위한 인덱스 선언
            while True:
                viewer.show_customer_information(rows, idx)  # 고객정보를 출력 

                if idx == 0:  # 첫화면의 다음스텝 입력받는 UI 출력
                    viewer.say_next_step('first')
                    viewer.say_where_information(idx+1, len(rows), 'first')
                    user_input = im.what_next_step('first')
                    if user_input.lower() == 'p':
                        idx += 1
                    elif user_input.lower() == 'u':
                        pass
                    elif user_input.lower() == 'z':
                        break

                elif idx == len(rows)-1:  # 마지막화면의 다음스텝 입력받는 UI 출력
                    viewer.say_next_step('last')
                    viewer.say_where_information(idx+1, len(rows), 'last')
                    user_input = im.what_next_step('last')
                    if user_input.lower() == 'n':
                        idx -= 1
                    elif user_input.lower() == 'u':
                        pass
                    elif user_input.lower() == 'z':
                        break

                else:  # 다음스텝 입력받는 화면 UI 출력
                    viewer.say_next_step()
                    viewer.say_where_information(idx+1, len(rows))
                    user_input = im.what_next_step()
                    if user_input.lower() == 'p':
                        idx += 1
                    if user_input.lower() == 'n':
                        idx -= 1
                    elif user_input.lower() == 'u':
                        pass
                    elif user_input.lower() == 'z':
                        break

        if select == '3':
            # 수정 UI 출력
            viewer.say_information_UI('수정')
            viewer.say_get_name_ident('수정')

            target_name = im.set_name()
            target_ident_num = im.set_identnum()

            # 입력 받은 고객 정보를 바탕으로 고객정보 찾기
            customer = connectDB.find_information(dao, target_name, target_ident_num)
            
            # 업데이트 진행
            viewer.say_go_update()
            name = im.set_name()
            ident_num = im.set_identnum()
            gender = im.set_gender()
            email = im.set_email()
            birth = im.set_birth()

            if customer:
                connectDB.update_information(dao, customer, name, ident_num, gender, email, birth)
                viewer.say_work_done()

        if select == '4':
            # 삭제 UI 출력
            viewer.say_information_UI('삭제')
            viewer.say_get_name_ident('삭제')

            name = im.set_name()
            ident_num = im.set_identnum()
            # 입력 받은 고객 정보를 바탕으로 고객정보 찾기
            customer = connectDB.find_information(dao, name, ident_num)

            # 삭제 진행
            if customer:
                connectDB.delete_information(dao, customer)
                viewer.say_work_done()