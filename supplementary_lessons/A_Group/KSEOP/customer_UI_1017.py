from customer2 import DBMgr
UI = DBMgr()
onprogram =True
while onprogram:
    read = input('수정(U) 조회(S) 입력(I) 삭제(D) 중 수행할 목록의 알파벳을 입력하세요:')
    if read == 'I':
        UI.insert_data()
    elif read == 'U':
        UI.update_data()
    elif read == 'S':
        UI.select_all_data()
    elif read == 'D':
        UI.del_data()
    while True:
        final = input('프로그램을 종료하시려면 Q를 수행목록 창으로 돌아가시려면 R을 눌러주세요' )
        if final =='Q':
            onprogram=False
            break
        elif final =='R':
            break
        else:
            ##### While 다시 수정하기
            print('다시한번 정확하게 입력해주세요')
    print('프로그램이 종료되었습니다 감사합니다')
    break

        # 함수가 종료되기 직전 다시 함수를 쓸껀지 물어보는 함수 호출10.11수정완료
        
if __name__ == '__main__' : 
    mgr =DBMgr()
    mgr.func_select()
