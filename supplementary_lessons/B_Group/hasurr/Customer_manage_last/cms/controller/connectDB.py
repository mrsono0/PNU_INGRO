from cms.model.member import Member

"""
dao : scoped_session 객체
member 는 Member 의 객체
"""

def select_information(dao):
    rows = dao.query(Member).order_by("code").all()
    return rows


def insert_information(dao, name, gender, email, birth, ident_num):
    member = dao.query(Member).filter_by(name=name,
        ident_num=ident_num,
        email=email).first()
    if member:
        pass
    else:
        member = Member(name, gender, email, birth, ident_num)
        dao.add( member )                                                                       
        dao.commit()


def delete_information(dao, member):
    if member:
        dao.delete(member)
        dao.commit()


def update_information(dao, member, name, ident_num, gender, email, birth):
    # 수정 -> 처리
    if member:
        member.name = name
        member.gender = gender
        member.email = email
        member.birth = birth
        member.ident_num = ident_num
        dao.commit()


def find_information(dao, name, ident_num):
    member = dao.query(Member).filter_by(name=name, ident_num=ident_num).first()
    if member:
        return member
    else:
        pass