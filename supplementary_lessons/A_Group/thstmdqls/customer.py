def customer(n):
    i = 1
    j = 1
    cus_people = []
     # n = input("입력하시겠습니까? : ")
    if n == "I":     # 입력 및 저장
        while i:
            i += 1
            name = input("이름을 입력하세요 : ")
            gender = input("성별을 입력하세요 : ")
            email = input("이메일을 입력하세요 : ")
            year = int(input("출생년도를 입력하세요 : "))

            cus_person = {"name":name, "gender":gender, "email":email, "year":year}
            cus_people.append(cus_person) # 빈 list에 고객 1명의 dict 추가
            decision = input("더 추가하시겠습니까?")
            if decision == "No":
                break
        x = input("조회하시겠습니까?")

    if x == "P" or "N":   # 조회
        print("총 고객입니다.", cus_people)
        while j:
            cus_num = int(input("현재 조회할 고객 번호 :"))
            print (cus_people[cus_num])
            who = input("이전 고객과 다음 고객 중 조회할 고객을 선택하세요\n조회할 고객이 없다면 Enter를 입력하세요 : ")
            if who == "P":
                print("이전 고객입니다.", cus_people[cus_num-1])
            elif who == "N":
                print("다음 고객입니다.", cus_people[cus_num+1])
            else:
                break
        y = input("이 고객을 수정하시겠습니까?")

    if y == "U":
        while i:
            a = int(input("바꿀 사람을 선택하세요 : "))
            print (cus_people[a])
            name1 = input("이름을 입력하세요 : ")
            gender2 = input("성별을 입력하세요 : ")
            email3 = input("이메일을 입력하세요 : ")
            year4 = int(input("출생년도를 입력하세요 :"))
            new_person = {"name": name1, "gender": gender2, "email": email3, "year": year4}

            cus_people[a].update(new_person)
            print (cus_people[a])
            decision = input("더 수정하시겠습니까?")
            if decision == "No":
                break
        z = input("삭제하시겠습니까?")
    if z == "D":
        w = int(input("삭제할 고객을 선택해주세요 : "))
        if w >= len(cus_people):
            print ("삭제 가능한 인원을 초과하였습니다.")
            print("현재 라재커피의 고객 현황입니다 : ", cus_people)
        else:
            del cus_people[w]
            print("현재 라재커피의 고객 현황입니다 : ", cus_people)
    else:
        print("현재 라재커피의 고객 현황입니다 : ", cus_people)
        
customer("I")
