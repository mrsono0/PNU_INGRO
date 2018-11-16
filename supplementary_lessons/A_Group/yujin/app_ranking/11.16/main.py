from model_write import *
from model_read import *
from view import *
import sys

# 콘솔창에서 디비에 적재할지 꺼낼지 여부 먼저 판단


class Start:
    # 수행할 기능 선택
    def consolever():
        whatExe=input(
        '''
            수행할 기능을 입력해주세요.
            r : DB 데이터 불러오기
            w : DB 데이터 적재
            q : 프로그램 종료
        ''')
        if whatExe=='q':
            quit()
        elif whatExe =='r':
            View.choiceOutput()
        elif whatExe =='w':  
            View.choiceInput()      


    def batchver_save():
        batch='batch'
        doc, load= Model.loading(Model,'1',batch)
        if load == 'ok':
            Model.makeDataFrame(Model,doc)
        else:pass
        doc, load=Model.loading(Model,'2',batch)
        if load == 'ok':
            Model.makeDataFrame(Model,doc)
        else:pass        
        doc, load=Model.loading(Model,'3',batch)                
        if load == 'ok':
            Model.makeDataFrame(Model,doc)
        else:pass        
        doc, load=Model.loading(Model,'4',batch)
        if load == 'ok':
            Model.makeDataFrame(Model,doc)
        else:pass        
        doc, load=Model.loading(Model,'5',batch)                
        if load == 'ok':
            Model.makeDataFrame(Model,doc)
        else:pass        

    def batchver_read():
        rankT=['1','2','3','4','5']
        for type in rankT:
            model_read.getData.initDB(type,'batch')
            model_read.getData.genreProp(type,'batch')
            model_read.getData.scoreDesc(type,'batch')
        for type in ['2','5']:
            model_read.getData.priceHist(type,'batch')






if __name__ == '__main__':
    if sys.argv[1] == '1':
        Start.batchver_save()
        Start.batchver_read()
        sys.exit()

    else:
        Start.consolever()














