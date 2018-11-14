# 시각화를 시도하려하는데 matplotlib 활용 했던건 많이 까먹어서 다시 돌아보는 페이지.

# matplotlib 호출 및 내장
import matplotlib.pyplot as plt
%matplotlib inline

# 한글 처리하기 (plot에 한글이 안됨 원래)
import platform
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin':# 맥
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows': # 윈도우
    # 폰트 차후 확인
    fontPath = 'c:/Windows/Fonts/malgun.ttf'
    fontName = font_manager.FontProperties(fname=fontPath).get_name()
    rc('font', family=fontName )
else:
    print('알수없는 시스템. 미적용')
    
# 아주 단순한 Bar 모양 chart
plt.figure()
# 차트 모양 : barh : bar+ h (수평선 차트 드로잉)
data_result['소계'].plot( kind='barh', grid=True, figsize=(10,10))
plt.show()

# ===== DataFrame의 '소계' 컬럼을 이용해서 bar 모양 chart를 그림. 특별히 뭐 더 써줄건없음.

plt.figure()
#해당 컬러만 소트해서 시각화
data_result.sort_values(by='소계', ascending=True)['소계'].plot( kind='barh', grid=True, figsize=(10,10))
# 전체 data_result를 소트하고나서 특정 컬럼을 시각화
plt.show()

# ==== 위에거랑 똑같이 '소계' 컬럼을 이용해서 bar모양 chart 그린건데 대신 수치를 sorting해서
# 정렬된 바 그래프가 나옴.

# x축 인구수, y축 CCTV수는 분포도로 표현
plt.scatter(data_result['인구수'],data_result['소계'], s=50)
plt.xlabel('인구수')
plt.ylabel('CCTV')
plt.grid()
plt.show()

# ==== Scatter Plot으로 산점도 형태.
# plt.scatter(df명[x축이될col], df명[y축이될col], s=50) s는 뭔지 잘? 아마 점 크기인듯.
# label을 통해서 차트에 이름 넣을 수 있음.

fp1 = np.polyfit(data_result['인구수'], data_result['소계'], 1)
fp1

f1 = np.poly1d(fp1)

# ==== 입력대비 출력을 만족하는 1차함수를 생성함(poly1d) 

# 시각화
plt.scatter(data_result['인구수'],data_result['소계'], s=50)
# 인구대비 CCTV의 관계를 1차함수로 표현한 선
plt.plot(x, f1(x), ls='dashed', lw=3, color='g')
plt.xlabel('인구수')
plt.ylabel('CCTV')
plt.grid()
plt.show()

# == 아까의 산점도에서 grid가 추가되고, scatter이 아닌 plot이 추가가됨
# == plot의 내용으로는 x 축은 그냥 x , y축을 이전에 만든 f1(x) 로함.
# == f1 이라는 poly1d가 f1(x) 처럼 쓸 수 있게 만들어 주는 듯 함.

# ==== 이후는 colorbar() 로 컬러바추가, scatter plot 에 텍스트 추가하는법 정도
# ==== 텍스트 추가하는 방법은 plot 위치를 불러 온 것에 텍스트를 위치시키는 방법임.
