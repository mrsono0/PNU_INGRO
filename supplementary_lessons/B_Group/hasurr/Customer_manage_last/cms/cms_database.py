from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBManager():
    __engine = None
    __session = None

    @staticmethod
    def init(db_url, db_log_flag=True):
        DBManager.__engine = create_engine(db_url, echo=db_log_flag)
        DBManager.__session = scoped_session(sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=DBManager.__engine
        ))

        return DBManager.__session

    @staticmethod
    def init_db():
        # 테이블이 없으면 생성 => model 에서 작성함
        # 클래스가 table, 객체 하나하나가 row
        from cms.model import member
        from cms.model import Base

        Base.metadata.create_all(bind=DBManager.__engine)

