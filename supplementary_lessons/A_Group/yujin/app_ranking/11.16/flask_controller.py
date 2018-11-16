from flask import Flask, url_for, render_template, request, redirect

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    if request.method =='GET':
        return render_template('home2.html')
    else:
        # post 방식일 때는 request.form[] 나 request.form.get() 둘 다 오류 없음
        if request.form['rankType_r']:
            rankType_r = request.form['rankType_r']
            return redirect(url_for('aa'))
        elif request.form['rankType_w']:
            rankType_w = request.form['rankType_w']
            return redirect(url_for('bb'))



@app.route('/aa')
def aa():
    return 'rankType_r'


@app.route('/bb')
def bb():
    return 'rankType_w'


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



# if __name__ =='__main__':
#     app.run(debug=True)



