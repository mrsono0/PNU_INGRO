####################### 컨트롤러


from gev_func import DBMgr
UI = DBMgr()


def func_select():
    onprogram = True
    while onprogram:
        read = input(' 조회할 데이터를 입력하세요.'
                     'S = 상위 20랭크 게임'
                     'D = 기간 중 순위 격차가 큰 게임'
                     'L = 상위 랭크 잔류기간이 긴 게임'
                     'R = 순위 와 평점이 모두 높은 게임')
        if read == 'S':
            UI.load_data()
        elif read == 'D':
            UI.gap_data()
        elif read == 'L':
            UI.long_live_data()
        elif read == 'R':
            UI.mixed_score()
        else:
            print('정확하게 다시 입력해주세요')
            continue
        while True:
            final = input('프로그램을 종료하시려면 Q를 수행목록 창으로 돌아가시려면 R을 눌러주세요')
            if final == 'Q':
                onprogram = False
                break
            elif final == 'R':
                break
            else:
                print('다시한번 정확하게 입력해주세요')

    return print('프로그램이 종료되었습니다 감사합니다')

if __name__ == '__main__':
    UI.load_data()
    func_select()
else:
    pass
