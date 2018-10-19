from cms.model import Base
from sqlalchemy import Column, Integer, String

class Member(Base):
    # 테이블명
    __tablename__ = 'tbl_customer_manage'
    code = Column(String(11), primary_key=True, unique=True, autoincrement=False)
    name = Column(String(50), unique=False)
    gender = Column(String(50), unique=False)
    email =Column(String(50), unique=True)
    birth = Column(String(50), unique=False)
    ident_num = Column(String(50), unique=True)


    def __init__(self, name, gender, email, birth, ident_num):
        self.name = name
        self.gender = gender
        self.email = email
        self.birth = birth
        self.ident_num = ident_num


    def __repr__(self):
        return """< Member %s %s %s %s %s >
        """ % (self.name, self.gender, self.email,
        self.birth, self.ident_num)
        
    def __str__(self):
        return '''
        회원번호 : %s
        이름 : %s
        성별 : %s
        이메일 :%s
        출생년도 : %s
        주민등록번호 : %s''' % (self.code, self.name, self.gender,
                            self.email, self.birth, self.ident_num)

