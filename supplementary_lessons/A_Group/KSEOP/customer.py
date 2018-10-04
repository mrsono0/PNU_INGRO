import pymysql as my

def insert_data():
    print('입력창 진입')
    name = input('이름을 입력하세요')
    age = input('나이를 입력하세요')
    gender = input('성별을 입력하세요')
    birth = input('생일을 입력하세요')
    conn = None
    try:
        conn = my.connect(
        host = 'localhost',
                user='root',
        password='sb0515',
        db='pythondb',
        charset='utf8',
        cursorclass=my.cursors.DictCursor
        )
        # 3. 쿼리 획득 및 수행 
        with conn.cursor() as cursor:
            sql ='''
                insert into customer_table(name, age, gender, birth)
                values( %s, %s, %s, %s );
                '''
            cursor.execute(sql, (name,age,gender,birth))
            # 최종 디비에 반영하기 위해 커밋 진행.
            conn.commit()
            # 결과 > Affected rows 획득. fetch계열없음.
            result = conn.affected_rows()             
                     
    except Exception as e:
        result = 0  
        print('에러 ->', e)
    
    if conn: # None 도 그 자체 불린은 false임.
        conn.close()
    #결과 리턴 : 튜플로 리턴 -> 리턴할 내용을 열거하면 된다.
    return print('삽입 종료')

def select_all_data():
    rows = None # 쿼리 결과.
    conn = None
    try:
        conn = my.connect(
        host = 'localhost',
                user='root',
        password='sb0515',
        db='pythondb',
        charset='utf8',
        cursorclass=my.cursors.DictCursor
        )
        # 3. 쿼리 획득 및 수행 
        with conn.cursor() as cursor:
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
    
    if conn: # None 도 그 자체 불린은 false임.
        conn.close()
    #결과 리턴
    return  rows ######################################

def select_all_data_sub():
    


def update_data():
    conn = None
    name = input('수정할 고객의 이름을 입력하시오')
    age = input('수정할 고객의 나이를 다시 입력하시오')
    birth = input('수정할 생년월일을 다시 입력하시오')
    try:
        conn = my.connect(
        host = 'localhost',
                user='root',
        password='sb0515',
        db='pythondb',
        charset='utf8',
        cursorclass=my.cursors.DictCursor
        )
        # 3. 쿼리 획득 및 수행 
        with conn.cursor() as cursor:
            sql ='''
                update customer_table set age =%s, birth =%s where name=%s
                '''
            # 3-3. 쿼리 수행
            cursor.execute(sql, (age, birth, name,))
            # 최종 디비에 반영하기 위해 커밋 진행.
            conn.commit()
            # 결과 > Affected rows 획득. fetch계열없음.
            result = conn.affected_rows()             
            

    except Exception as e:
        result = None
        print('에러 ->', e)
    
    if conn: # None 도 그 자체 불린은 false임.
        conn.close()
    #결과 리턴 : 튜플로 리턴 -> 리턴할 내용을 열거하면 된다.
    return result

def make_param(name, age, gender, birth):
    pass#name = input('')

def del_data():
    name = input('삭제할 고객의 이름을 입력하세요')
    rows = None # 쿼리 결과.
    conn = None
    try:
        conn = my.connect(
        host = 'localhost',
                user='root',
        password='sb0515',
        db='pythondb',
        charset='utf8',
        cursorclass=my.cursors.DictCursor
        )
        # 3. 쿼리 획득 및 수행 
        with conn.cursor() as cursor:
            # 3-2. sql 준비
            sql ='''
                delete from customer_table where name = %s
            '''
            # 3-3. 쿼리 수행
            cursor.execute(sql, (name,)) #sql이 적힌건 sql만 인자로 받기떄문
            # 3-4. 결과 처리 및 커서 닫기
            rows = cursor.fetchall() # 얘가 출력의 본질임.            
            conn.commit()           
    except Exception as e:
        rows = None
        print('에러 ->', e)
    
    if conn: # None 도 그 자체 불린은 false임.
        conn.close()
    #결과 리턴
    return  print('삭제완료')######################################

def func_select():
    read = input('수정 조회 입력 삭제 중 무엇을 선택하시겠습니까?:')
    if read == '입력':
        insert_data
    elif read == '수정':pass
    
    elif read == '조회':
        select_all_data
    elif read == '삭제':
        pass
    return func_select

    # 함수가 종료되기 직전 다시 함수를 쓸껀지 물어보는 함수 호출
    

'''
a = select_all_data()
b =
print(a[b])
'''
