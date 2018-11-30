from flask import Flask, url_for, render_template, request, redirect
from model import selectData, getFiles, selectDesc
from model_read import getData
import main_controller
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
            main_controller.Start.flask_write(rankType)
            return render_template('step2_write_25.html',rankType=rankType)
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
        genrerow =[]
        for row in rows:
            if row.startswith("genrepie"):
                genrerow.append(row)
        return render_template('step3_read_2.html', data=genrerow )

    elif visualType == '3':
        rows = selectDesc(rankType)
        rows = rows[:10]
        return render_template('step3_read_3.html',data=rows)

    elif visualType =='4':
        rows = getFiles(rankType)
        genrerow =[]
        for row in rows:
            if row.startswith("pricebar"):
                genrerow.append(row)
        return render_template('step3_read_2.html', data=genrerow )



@app.route('/image', methods=['GET'])
def image():
    filename = request.args.get('filename')
    return render_template('image.html',rankType=rankType,filename=filename)


if __name__ =='__main__':
    app.run(debug=True)





