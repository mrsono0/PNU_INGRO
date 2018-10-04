custlist = [{'name': 'AA', 'sex': 'M', 'email': 'AA', 'birthyear': '1111'},
 {'name': 'BB', 'sex': 'F', 'email': 'BB', 'birthyear': '2222'},
 {'name': 'CCC', 'sex': 'M', 'email': 'CCC', 'birthyear': '3333'}]


choice1=input('''삭제하려는 이메일을 입력하세요.''')
idx=0
for i in range(0,len(custlist)):
    if custlist[i]['email'] == choice1:
        idx=i
        print('{}고객님의 정보가 삭제됐습니다.'.format(custlist[idx]['name']))
        del custlist[idx]

        # print(custlist)
        break
    else:
        print('{}고객님의 정보는 없습니다.'.format(choice1))
        print('데이터가 없습니다.')
        break



# del custlist[0]

# print(custlist)
