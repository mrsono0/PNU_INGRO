from flask import Flask, url_for, render_template, request, redirect
from model import selectData, getFiles
from model_read import getData
app = Flask(__name__)

rankType=None

@app.route('/',methods=['GET','POST'])
def home():
    global rankType
    if request.method =='GET':
        return render_template('home2.html')
    else:
        # post 방식일 때는 request.form[] 나 request.form.get() 둘 다 오류 없음
        if request.form.get('rankType_r'):
            rankType = request.form['rankType_r']
            if rankType in ('2','5'):
                return render_template('step2_read_25.html',rankType=rankType)
            else:
                return render_template('step2_read_134.html',rankType=rankType)
        else:
            rankType = request.form['rankType_w']
            if rankType in ('2','5'):
                return render_template('step2_write_25.html',rankType=rankType)
            else:
                return render_template('step2_write_134.html',rankType=rankType)
            # if id(option1/option2)가 체크되어 있으면=====================
            # 시각화 종류 선택 페이지 만들기 ===========================
            # 받아온 데이터 보여주고 확인하는 페이지 만들기 =============

@app.route('/visual', methods=['POST'])
def visual():
    visualType = request.form['visualType_r']
    if visualType == '1':
        rows = selectData(rankType)
        rows = rows[:10]
        if rankType in ('2','5'):
            return render_template('step3_read_1_25.html',data=rows)
        else:
            return render_template('step3_read_1_134.html',data=rows)
    elif visualType =='2':
        rows = getFiles(rankType)
        return render_template('step3_read_2.html', data=rows )

@app.route('/image', methods=['GET'])
def image():
    filename = request.args.get('filename')
    return render_template('image.html',rankType=rankType,filename=filename)



'''
if uid and upw: # 정상
    #3. 데이터가 정상이면 디비 조회
    row = loginSql(uid,upw)
    if row:
        #4. 회원이 맞으면 ok -> 세션생성(후처리) -> 서비스 이동
        # 요청을 다른 url로 돌려준다
        return redirect(url_for('home'))
    else:
    #4. 회원이 아니면 fail -> 경고 처리 후 돌려보낸다
        return render_template('err.html', msg='회원이 아니시잖아요!!')
    #return '정상응답'
else:#비정상처리
    #2. 데이터가 없는 경우? -> 경고 처리 돌려보낸다
    return render_template('err.html', msg='입력이 정확하지 않습니다.')
'''



if __name__ =='__main__':
    app.run(debug=True)

