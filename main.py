import func as sf

print('-- 레스토랑 예약 관리 시스템 --')

if sf.db_connect() == False:
    exit(1)

while(True):
    try:
        try:
            print('1. 전체 목록 조회\n2. 고객 정보 조회\n3. 신규 고객 입력\n4. '
                  '고객 정보 수정\n5. 고객 정보 삭제\n6. 가격 계산\n7. 프로그램 종료')
            action = int(input('실행할 메뉴 번호 입력>'))
            # 여기서 try구문과 continue를 활용하여 잘못된 메뉴 입력을 처리할 수 있다.
            if action >= 1 and action <= 7:
                pass
            else:
                print('1 ~ 7 사이의 번호를 입력해주십시오')
            if action == 1:
                print('예약자 전체 목록 조회 화면')
                print(f'{"고객 ID":^10} {"고객 성함":^8} {"고객 연락처":^8}'
                      f' {"인원수":^10} {"특이사항":^15} {"예약메뉴"}')
                sf.show_customer()

            elif action == 2:
                print("조회하고자하는 손님의 이름과 핸드폰 번호를 입력해주세요")
                name = input("손님 성함: ")
                phone = input("손님 핸드폰 번호(00000000000): ")
                # phone 번호 입력 시 길이 확인
                if len(phone) == 11:
                    row = sf.check_customer(name, phone)
                    if row == None:
                        print("없는 고객입니다.")
                    else:
                        print("검색하신 고객의 정보는 다음과 같습니다.")
                        print(f'{"고객 ID":^10} {"고객 성함":^8} {"고객 연락처":^8}'
                              f' {"인원수":^10} {"특이사항":^15} {"예약메뉴"}')
                        print(
                            f'''{row["id"]:^15}{row["name"]:10}{row["phone"]:10}{row["num"]:^15}{row["comment"]:^15}{row["menu"]}''')
                else:
                    print("핸드폰 번호가 올바르지 않은 형식입니다.")

            elif action == 3:
                print("신규 고객 입력")
                print('예약자님의 정보를 입력해주세요.')
                name = input("예약자님의 성함: ")
                phone = input("손님 핸드폰 번호(00000000000): ")
                # phone 번호 입력 시 길이 확인
                if len(phone) != 11:
                    print("핸드폰 번호가 올바르지 않은 형식입니다.")
                    continue
                # check_customer의 정보란에 중복값이 없으면 add_customer 실행
                # 실행 오류: True가 아니라 None이여야 중복값인지 확인할 수 있음
                if sf.check_customer(name, phone) != None:
                    print("이미 있는 정보입니다. 다시 시도해주세요.")
                    # 여기서 중복 값이 뜨지 않으면 다음 단계로!
                else:
                    num = int(input("인원을 입력해주세요: "))
                    # 실행 오류: 일단, 오류라기보다는 되지만 부족한 부분
                    # 여기서 num이 int가 아닌 경우 어떤 메시지를 보여줄지 따로 설정하지 않았으나,
                    # 알아서 메뉴를 제대로 선택하라는 메시지를 호출하고 있다.
                    if num < 1 or num > 4:
                        print("인원은 1명부터 4명까지 가능합니다.")
                        continue
                    else:
                        menu = input("lunch or dinner?: ")
                        # 여기서 lunch나 dinner외의 다른 선택지는 오류처리
                        if menu != 'lunch' and menu != 'dinner':
                            print("잘못입력하셨습니다.")
                        else:
                            comment = input("알레르기 등 특이사항을 입력하세요(100자): ")
                            # 이때 comment 길이가 100자 이하
                            if len(comment) > 100:
                                print("100자 이하로 입력해주세요.")
                            else:
                                if sf.add_customer(name, phone, num, comment, menu) == True:
                                    print("신규 입력이 완료되었습니다.")
                                else:
                                    print("오류 발생, 다시 시도해주세요.")

            elif action == 4:
                print('고객 정보 수정')
                # show_customer() 호출
                print(f'{"고객 ID":^10} {"고객 성함":^8} {"고객 연락처":^8}'
                      f' {"인원수":^10} {"특이사항":^15} {"예약메뉴"}')
                sf.show_customer()
                # 수정할 고객의 이름과 전화번호를 입력
                print("수정할 고객의 성함과 핸드폰 번호를 입력하세요.")
                update_info = {}
                update_info['name'] = input("수정할 고객의 성함: ")
                update_info['phone'] = input("수정할 고객의 핸드폰번호(00000000000): ")
                if len(update_info['phone']) != 11:
                    print("핸드폰 번호가 잘못된 형식입니다.")
                # 실행 오류: 핸드폰 유효성 검사 이후에도 정보 확인을 한다. 필요없는 기능
                # else 구문 삽입과 들여쓰기 조정을 통해 해결
                # check_customer로 유효성 검사
                else:
                    if sf.check_customer(update_info['name'], update_info['phone']) == None:
                        print("없는 정보입니다.")
                    # 위에서 기존 정보가 있으면
                    # update_customer() 호출 후 수정
                    else:
                        print("수정할 인원, 메뉴, 특이사항을 입력하시오.")
                        update_info['num'] = int(input("인원을 입력하시오: "))
                        # 인원 유효성 검사
                        if update_info['num'] >= 1 and update_info['num'] <= 4:
                            update_info['menu'] = input("lunch or dinner?: ")
                            if update_info['menu'] == 'lunch' or update_info['menu'] == 'dinner':
                                update_info['comment'] = input("알레르기 등 특이사항을 입력하세요(100자): ")
                                if len(update_info['comment']) > 100:
                                    print("100자 이하만 입력 가능합니다.")
                                else:
                                    if sf.update_customer(update_info) == True:
                                        print("업데이트 완료")
                                    else:
                                        print("오류 발생, 업데이트 실패")
                            else:
                                print("메뉴를 제대로 입력해 주세요.")
                        else:
                            print("인원수는 1명부터 4명까지 가능합니다.")
                            continue

            elif action == 5:
                print('고객 정보 삭제')
                # show_customer() 호출
                print(f'{"고객 ID":^10} {"고객 성함":^8} {"고객 연락처":^8}'
                      f' {"인원수":^10} {"특이사항":^15} {"예약메뉴"}')
                sf.show_customer()
                print("삭제할 고객의 이름과 핸드폰 번호를 입력하시오.")
                delete_info={}
                delete_info['name'] = input("삭제할 고객의 이름을 입력하세요:")
                delete_info['phone'] = input("삭제할 고객의 핸드폰번호(00000000000): ")
                if len(delete_info['phone']) != 11:
                    print("핸드폰 번호가 잘못된 형식입니다.")
                # check_customer를 통해 유효성 확인
                if sf.check_customer(delete_info['name'],delete_info['phone']) != None:
                    # 있는 정보임이 확인되면 삭제
                    if sf.delete_customer(delete_info) == True:
                        print("삭제 완료")
                    else:
                        print("오류 발생, 삭제 실패")
                else:
                    print("없는 정보입니다.")

            elif action == 6:
                print('가격 계산')
                # show_customer() 호출
                print(f'{"고객 ID":^10} {"고객 성함":^8} {"고객 연락처":^8}'
                      f' {"인원수":^10} {"특이사항":^15} {"예약메뉴"}')
                sf.show_customer()
                print("금액을 계산할 고객의 이름과 전화번호를 입력하세요: ")
                name = input("고객 성함: ")
                phone = input("고객 전화번호(00000000000): ")
                if len(phone) != 11:
                    print("핸드폰 번호가 잘못된 형식입니다.")
                if sf.check_customer(name,phone) == None:
                   print("없는 정보입니다.")
                else:
                    print(sf.cal_price(name, phone))

            elif action == 7:
                print('프로그램 종료')
                sf.db_close()
                break

        except ValueError:
            print("메뉴를 제대로 선택해주십시오")
    except KeyboardInterrupt:
        print("프로그램을 종료합니다.")
        sf.db_close()
        break