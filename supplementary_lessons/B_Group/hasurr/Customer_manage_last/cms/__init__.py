
# 데이터 베이스 연결 처리
from cms.controller import input_manager, go
from cms.cms_database import DBManager
from cms.view import Viewer

config = {
    'DB_URL'      : 'localhost',
    'DB_USER'     : 'root',
    'DB_PASSWORD' : '12341234',
    'DB_DATABASE' : 'pythondb',
    'DB_CHARSET'  : 'utf8',
    'DB_LOGFLAG'  : 'False',
    'DB_PORT'     : 3306}


class App():
    dao = None
    veiwer = None
    im = None

    def __init__(self):
        db_url = "mysql+pymysql://%s:%s@%s:%s/%s?charset=%s" % (
            config['DB_USER'],
            config['DB_PASSWORD'],
            config['DB_URL'],
            config['DB_PORT'],
            config['DB_DATABASE'],
            config['DB_CHARSET'],
        )

        self.dao = DBManager.init( db_url , eval(config['DB_LOGFLAG']))
        DBManager.init_db()

        self.viewer = Viewer()
        self.im = input_manager.InputManager()

        # """
        # 테스트용 데이터 삽입
        # """
        # test_data = [
        #         {
        #             'name': '김길동',
        #             'gender': 'f',
        #             'email': 'a@a.com',
        #             'birth': '123456',
        #             'ident_num': '940915-1111111'},
        #         {
        #             'name': '홍길동',
        #             'gender': 'm',
        #             'email': 'd@d.com',
        #             'birth': '123456',
        #             'ident_num': '931204-1222222'
        #             }
        #         ]

        # a = connectDB.find_information(test_data[0]['name'],
        #     test_data[0]['ident_num'])
        
        # if not a:
        #     connectDB.insert_information(test_data[0]['name'],
        #     test_data[0]['gender'],
        #     test_data[0]['email'],
        #     test_data[0]['birth'],
        #     test_data[0]['ident_num']
        #     )


        # a = connectDB.find_information(test_data[1]['name'],
        # test_data[1]['ident_num'])
        # if not a:
        #     connectDB.insert_information(test_data[1]['name'],
        #     test_data[1]['gender'],
        #     test_data[1]['email'],
        #     test_data[1]['birth'],
        #     test_data[1]['ident_num']
        #     )

    def run(self):
        go.gogosing(self.viewer, self.im, self.dao)
        
                


    
    
