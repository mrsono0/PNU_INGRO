시각화자료를 웹페이지로 제공하기위한 FLASK 구성.

"""
GEV_API를 FLASK에 제공하기 위한 FLASK RE_

FLASK의 구조 Directory

===================================================
model      /__init__.py

static     /js/*.html
           /*.html

templates  /*.html

run py
=================================================== 형태임.

flask_cms readme.txt =======================================================================
[[ flas cms 구조 ]]
static : 정적 데이터가 위치하는 폴더. css, js, image, 업로드된 파일 등
        자동으로 url이 세팅됨
        http://ip:port/static/파일명

----------------------------------------
templates : render_template() 함수의 1번인자 파일이 위치한 폴더. html 이치
-----------------------------------------
service : db, 라우팅 등 phthon 코드 위치 한 곳
------------------------------------------
run.py : 프로그램 시작점
-----------------------------------------

세션 : 서버측에 저장하는 사용자의 정보
        서버 메모리(구현간단, 소량의 사용자 적합) 혹은 데이터베이스에 저장 관리 가능
        => 사용자가 로그인 되어 있음을 세션에 저장하여 체크 후 페이지 접근 등등에 활용
        이런 경우 데이터의 성격에 따라서는 페이지 요청 시 데이터를 보내지 않고
        세션을 접근해서 데이터를 획득하여 사용하는 경우도 있음.

쿠키 : 클라이언트 측에 저장하는 사용자의 정보
=============================================================================================
"""
# =============================================================================================
# Flask_cms 를 REVIEW 하면서 살펴보기.

from flask import Flask, url_for, request, render_template, redirect, jsonify, session, jsonify

from flask_cms.service.model import loginSql, select_tradeLastData as tradeList
from flask_cms.service.model import select_searchTradeCode as ssearch, insert_data, select_data
# flask 에서 필요한 Flask, url_for, request... 등등을 불러옴.
'''
# 리눅스상 프로그램 구동 구조를 위해 import 구조가 위에처럼 달라짐 
from service.model import loginSql
from service.model import select_tradeLastData as tradeList
from service.model import select_searchTradeCode as ssearch
from service.model import insert_data, select_data
'''
# ==================================================================================================
# service.model 폴더(파이썬코드가 위치한 곳)의 __init__.py 로 부터 만들어 놓은 함수를 모두 가져온다.

# __init__.py 의 구성.
# DB와 연동하는 함수들로 가득함.

# [run.py]
# run.py 의 구성내용은 주로 플라스크 페이지의 라우팅. 라우팅 된 페이지에서 작동할 함수들이 적혀있음.
app = Flask(__name__)
app.secret_key = 'sdfafdsfff'


@app.route('/')
def home():
    # 세션 체크
    if not 'user_id' in session: # 세션 객체안에 user_id가 있는지 없는지 체크를 하고 없으면
        return redirect( url_for('login'))  # login을 해야하는 페이지를 불러냄. 라우팅 페이지를 담는
    # 함수 이름을 입력하는 곳임. /login 페이지는 def login()을 갖고있음.
    return render_template('index.html', title='cms based flask')
    # 아이디가 있는 상황이면 templetes 의 sub 폴더에 있는 index.html 을 가져옴. title 값은 html 파일에
    # 받는 인자가 있는 모양임을 추정함

@app.route('/logout')
def logout():
    # 세션 제거
    if 'user_id' in session: session.pop('user_id')
    if 'user_name' in session: session.pop('user_name')
    # 홈페이지 이동
    return redirect( url_for('home'))

# 기존에 flask 의 모듈중 하나인 session 이라는 객체 속에 user_id 를 보유 하고있다가(로그인상태) 없애면(pop)
# 그것이 로그아웃의 논리로 만드는 session 객체. 세션을 비워버리고 나면 다시 home으로 오게함.
# home 은 다시 로그인을 요구함.

@app.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'GET':
                return render_template('login.html')
        else:
                uid = request.form.get('uid')
                upw = request.form.get('upw')
                print('테스트')
                if uid and upw:
                        row = loginSql(uid, upw)
                        if row:
                                # 4. 회원이 맞으면 ok -> 세션 생성(후처리) -> 서비스 이동
                                # 세션 생성
                                session['user_id'] = uid
                                session['user_name'] = row['name']
                                # 요청을 다른 url로 돌려줌

                                return redirect(url_for('home'))

                        else:
                                return render_template('alert.html', msg='회원이 아닙니다.')
                        # 4. 회원이 아니면 fail -> 경고 처리후 돌려보낸다.
                else:  # 비정상처리
                        # 2. 데이터가 없는 경우? => 경고 처리 후 돌려보냄.
                        return render_template('alert.html', msg='입력이 정확하지 않습니다.')
        return render_template('login.html')

# 로그인 페이지를 라우팅하는 함수임. GET과 POST 방식을 모두 사용함.
# 우선 GET 방식으로 접근을 해서 If 문을 거치면서 login.html 을 호출하게됨.
#   => login.html penal-body를 실행하는데 이때의 방식은 post이며 action 으로 login url 을 호출하여
# login() 을 한번 더 실행 시킴. 현재 html 구분의 penel-body 작동으로 인해 method가 post가 되었으므로
# else 문으로 넘어가게됨. 그리고 html이 input 클래스로 받아낸 uid와 upw를 uid와 upw에 받고
# 받은게 완료가 되면 __init__.py 의 loginSql() 을 거치면서 DB에 있는 정보인지를 거친 후
# 있는게 맞으면 해당 id와 DB에 저장된 해당 id가 담긴 row 한줄을 통째로 가져와서 row 에 담아서 반환함
# 그러면 row는 user_id 와 user_name을 가진 True 불린 값이 되면서 session 객체에 삽입되게됨.
# 세션이 딕셔너리인지 뭐 데이터프레임인지는 모르겠으나 하여튼 삽입됨. 아마 딕셔너리 일 것임.
# 이러면 세션 객체에 값이 추가되었으므로 if session 이 True 가 되므로 로그인을 한 것임. 그리고
# url_for('home')으로 홈페이지로가서 다시 홈페이지의 작업을 진행하게됨.

""" 업로드 페이지 구현. 시각활 저장한 이미지를 올릴 수 있는 페이지? """

@app.route('/upload', methods=['GET', 'POST'])
def upload():
        if request.method == 'GET':  # 검색 화면
                # index.html 카피해서 uploadForm.html 준비
                # index_sub.html 카피해서 uploadForm_sub.html 준비
                # uploadForm.html 내부에 uploadForm_sub.html include 수정.
                # render_template()처리
                return render_template('uploadForm.html')

# upload 페이지를 url 입력을 통해서 진입 or 하여간 upload 페이지로 진입을하면 처음에는 GET방식으로 진입해서
# uploadForm.html 을 따라가게됨.
""" uploadForm.html 일부내용
</head>
<body>
 <!-- Navigation -->
        {% include 'common/navi.html' %}
        {% include 'sub/uploadForm_sub.html' %}
        <!-- /#page-wrapper -->
    </div>
    <!-- /#wrapper -->
    {# common/foot.html에 아래 내용을 넣고 include 하시오 #}
    {% include 'common/foot.html' %}
"""
# 다른 디렉토리의 navi.html과 uploadForm_sub.html을 불러오게되는데
# navi 는 html 페이지의 스트럭쳐 모양새 자체를 다루는 껍데기 html로 추정되고
# uploadForm_sub.html이 실질적인 upload의 내용을 가짐.
""" uploadForm_sub.html 의 일부내용
<form action='upload' method='POST' enctype='multipart/form-data'> <!-- form action 은 데이터를 어디로 보낼것인가 지정하는 것-->
                                <input type='text' name='title'/>
                                <br/>
                                <textarea name='contents'></textarea>
                                <br/>
                                <input type='file' name='fileData'/>
                                <br/>
                                <input type='submit' value='업로드'/>
                            </form>
"""
# uploadFrom_sub 의 내용에서 다시 action 키워드를 통해 upload 함수를 불러오게 되고 , 이때의 접근은
# 이전의 사례들 처럼 POST 방식임. form action 을 통해 다시 upload.html 을 호출한다.

        else:   title = request.form.get('title')
                contents = request.form.get('contents')
                fileData = request.files['fileData']

                # uploadFrom_sub 의 input type 에서 입력된 각 변수들을 request.form.get, files 를 통해
                # 받아온다.

                import os

                checkPath = '%s\\static\\upload\\%s' % (os.getcwd(), session['user_id'])
                if not os.path.exists(checkPath):
                        os.mkdir(checkPath)

                # 사용자 uid 이름을 참조하여 디렉토리 생성(mkdir)함.
                # 디렉토리 체크해보면 static/upload/bu 있음.

                path = '%s\\static\\upload\\%s\\%s' % (os.getcwd(), session['user_id'], fileData.filename)
                # 저장 경로 생성
                fileData.save(path)
                # save(path) 이용해서 만든 가변경로에 파일 저장.

                downurl = '/static/upload/%s/%s' % (session['user_id'], fileData.filename)
                # 파일의 url 경로 생성.

                # 디비에 입력 (제목, 내용, 파일의 url 경로)
                if insert_data(title, contents, session['user_id'], downurl):

                # __init__.py의 insert_data() 참고. 데이터 베이스에 if 이후 적힌 순으로 저장되게됨.
                # return 값으로 affected rows, 즉 추가된 열을 반환하므로 정상적으로 업로드 된 것이 맞다면
                # 아래의 alert.html 에 msg 값으로 '업로드 성공을 넘겨주게 됨.
                        return render_template('alert.html', msg='업로드 성공', target_url='/scrapList')
                # 업로드가 성공하고 나면 scrapList html 연결 자동으로 sub 파일까지 연결됨.
                # scrapList_sub.html 에서는 업로드 되어왔던 내역들이 적힌 것으로 추정됨. for 문으로 title 들을
                # 가져옴.
                else:
                        return render_template('alert.html', msg='업로드 실패', )

                        # 신규 페이지 이식 => 기능을 추가하는 방법(메뉴 추가)


 ########### 11.28. search()를 왜 넘겼는지 모르겠으나, 아무튼 search()부터 재학습




