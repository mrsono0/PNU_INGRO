custlist = [{'name': 'AA', 'sex': 'M', 'email': 'AA', 'birthyear': '1111'},
 {'name': 'BB', 'sex': 'F', 'email': 'BB', 'birthyear': '2222'},
 {'name': 'CCC', 'sex': 'M', 'email': 'CCC', 'birthyear': '3333'}]


while True:
    choice1=input('''수정하시려면 이메일을 입력하세요.''')
    choice2=input('''
    다음 중에서 바꾸고싶은 정보를 골라주세요 :
    name, sex, birthyear
    (바꾸고 싶은 게 없으면 Q)
    ''')
    idx=0
    for i in range(0,len(custlist)):
        if custlist[i]['email'] == choice1:
            idx=i

    if choice2 in ('name','sex','birthyear'):
        custlist[idx][choice2]=input('바꾸려는 {}을 입력하세요.'.format(choice2))
        # print(custlist[idx][choice2])
    else:
        break


# while True:
#             choice1=input('''수정하시려면 이메일을 입력하세요.''')
#             for i in range(0,len(custlist)):
#                 if custlist[i]['email'] != choice1:
#                     print('{}고객님의 정보는 없습니다.'.format(choice1))
#                     break
