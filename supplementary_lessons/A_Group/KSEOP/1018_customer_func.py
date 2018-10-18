import pymysql as my
class DBMgr:
    def __init__(self):
        self.initDB()
    
    
    def initDB(self):
        self.conn = my.connect(
                    host = 'localhost',
                    user='root',
                    password='sb0515',
                    db='pythondb',
                    charset='utf8',
                    cursorclass=my.cursors.DictCursor
                    )
        return self.conn
    
    def freeDB(self):
        if self.conn:
            self.conn.close()

    def insert_data(self):
        while True:
            print('입력창 진입')
            # while True:
            name = input('이름을 입력하세요')
            age = input('나이를 입력하세요')
            gender = input('성별을 입력하세요')
            email = input('이메일을 입력하세요')
                ###############################################################################
                # if type(name) != str: 
                #     print('이름은 문자만 입력하여 주십시오')
                #     continue
                # elif type(age) != int:
                #     print('나이는 숫자만 입력하여 주십시오')
                #     continue
                # elif gender != 'M' or 'F':
                #     print('성별은 M 또는 F 만 입력하여 주십시오')
                #     continue
                # elif '@' and '.' not in email:
                #     print('이메일 형식이 잘못되었습니다..')
                #     continue
                # break
                ##############################################################################
            
            try:
                self.initDB()
                # 3. 쿼리 획득 및 수행 
                with self.conn.cursor() as cursor:
                    sql ='''
                        insert into customer_table(name, age, gender, email)
                        values( %s, %s, %s, %s );
                        '''
                    cursor.execute(sql, (name,age,gender,email))
                    # 최종 디비에 반영하기 위해 커밋 진행.
                    self.conn.commit()
                    # 결과 > Affected rows 획득. fetch계열없음.
                    result = self.conn.affected_rows()             
                            
            except Exception as e:
                result = 0 
                print('에러 ->', e)
                str(e)

                break
            if self.conn: # None 도 그 자체 불린은 false임.
                self.conn.close()
            #결과 리턴 : 튜플로 리턴 -> 리턴할 내용을 열거하면 된다.
            return print('삽입 종료')

    def select_all_data(self):
        rows = None # 쿼리 결과.
        
        try:
            self.initDB()
            # 3. 쿼리 획득 및 수행 
            with self.conn.cursor() as cursor:
                # 3-2. sql 준비
                sql ='''
                    select * from customer_table ; 
                '''
                # 3-3. 쿼리 수행
                cursor.execute(sql) #sql이 적힌건 sql만 인자로 받기떄문
                # 3-4. 결과 처리 및 커서 닫기
                rows = cursor.fetchall() # 얘가 출력의 본질임.

        except Exception as e:
            rows = None
            print('에러 ->', e)
        
        if self.conn: # None 도 그 자체 불린은 false임.
            self.conn.close()
        #결과 리턴
        page_num = 0
        print(rows[page_num])
        while True:
            ##첫번째 고객정보를 보여준 후  input을 보여줘야한다 첫번째 고객에서는 D가 없어야한다. 마지막 고객에서는 P가 없어야한다
            #DB에서 첫번째 고객정보를 받아온다.
            select_UpDown = input('다음 고객 정보를 조회하려면 N키를, 이전 고객을 조회하시려면 P키를, 조회를 종료하려면 Q키를 입력해주세요 :')
            if select_UpDown =='P':
                if page_num == 0 :
                    print('첫번째 고객 정보입니다.'.format(page_num+1))
                    print(rows[page_num])
                else: 
                    page_num -= 1
                    print('{}번째 고객 정보입니다.'.format(page_num+1))
                    print(rows[page_num])
                continue
            
            if select_UpDown =='N':
                if page_num == len(rows)-1:
                    print('마지막 고객정보 입니다.')
                    print(rows[page_num])
                else:
                    page_num += 1
                    print('{}번째 고객 정보입니다.'.format(page_num+1))
                    print(rows[page_num])
                continue
            
            elif select_UpDown =='Q':
                break     
            else:
                print('P와 D, Q중 정확하게 입력하여 주세요')
                continue

        return None

    def update_data(self):
        
        while True:    
            name = input('수정할 고객의 이름을 입력하시오')
            age = input('수정할 고객의 나이를 다시 입력하시오')
            birth = input('수정할 생년월일을 다시 입력하시오')############없으면 pass -> while True : break로 가자
            try:
                self.initDB()
                # 3. 쿼리 획득 및 수행 
                with self.conn.cursor() as cursor:
                    sql ='''
                        update customer_table set age =%s, birth =%s where name=%s
                        '''
                    # 3-3. 쿼리 수행
                    cursor.execute(sql, (age, birth, name,))
                    # 최종 디비에 반영하기 위해 커밋 진행.
                    self.conn.commit()
                    # 결과 > Affected rows 획득. fetch계열없음.
                    result = self.conn.affected_rows()             
                    

            except Exception as e:
                result = None
                print('에러 ->', e)
            
            if self.conn: # None 도 그 자체 불린은 false임.
                self.conn.close()
            #결과 리턴 : 튜플로 리턴 -> 리턴할 내용을 열거하면 된다.
            return result

    def del_data(self): #########고객 정보를 잘못입력할 경우에 대한 예외 처리가 없음
        name = input('삭제할 고객의 이름을 입력하세요')
        rows = None # 쿼리 결과.
        
        try:
            self.initDB()
            # 3. 쿼리 획득 및 수행 
            with self.conn.cursor() as cursor:
                # 3-2. sql 준비
                sql ='''
                    delete from customer_table where name = %s
                '''
                # 3-3. 쿼리 수행
                cursor.execute(sql, (name,)) #sql이 적힌건 sql만 인자로 받기떄문
                # 3-4. 결과 처리 및 커서 닫기
                rows = cursor.fetchall() # 얘가 출력의 본질임.            
                self.conn.commit()           
        except Exception as e:
            rows = None
            print('에러 ->', e)
        
        if self.conn: # None 도 그 자체 불린은 false임.
            self.conn.close()
        #결과 리턴
        print(rows)
        return rows 
        # print('삭제완료')######################################
