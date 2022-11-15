from .models import *

from .serializers import *
# json 임포트
import json
'''
221107 냉장고 조회 class 추가
221109 냉장고 조회 함수 작업중
221114 냉장고 조회 함수 작업 완료
221114 냉장고 재료 추가 함수 작업중
'''

class ControlRefrigerator_b():
    '''
    냉장고 조회 함수

    parameter       nickname:String 
    return type     List<Refrigerator>
    로 변경해야함.  
    '''
    def requestRefrigerator(self, nickname):
        ingredientsList = Refrigerator.objects.filter(nickname = nickname)

        print(ingredientsList)

        for i in range(len(ingredientsList)):
            print(ingredientsList[i].nickname)

        if ingredientsList.exists():
            result, code = self.sendResult("냉장고 조회 성공.", ingredientsList)
        else:
            result, code = self.sendResult("냉장고에 식재료가 없습니다.", None)
        return result, code

    def insertRefrigerator(self, refrigerator):
        print(f"insert Refrigerator start")
        userRequest = json.loads(refrigerator.body)

        try:
            refriObject = Refrigerator.objects.create(amount = userRequest['amount'],
                expiry_date = userRequest['expiry_date'],
                name = Ingredients.objects.get(name = userRequest['name']),
                nickname = User.objects.get(nickname = userRequest['nickname']),
                unit = Units.objects.get(unit = userRequest['unit']))
                
            refriObject.save()

            print("서버 : 냉장고 정보 추가 성공")
            result, code = self.sendResult("냉장고 재료 추가 성공.", None)
        except:
            print("서버 : 냉장고 정보 추가 실패")
            result, code = self.sendResult("냉장고 재료 추가 실패.", None)
        
        return result, code

    def deleteRefrigerator(self, nickname, name):
        pass
    
    def updateRefrigerator(self, nickname, ingredient):
        pass
    def sendResult(self, result, refrigerator):
        if result == "냉장고에 식재료가 없습니다.":
            print("no food in refri")
            return refrigerator, 0
        elif result == "냉장고 조회 성공.":
            print("yes food in refri")
            return refrigerator, 1
        elif result == "냉장고 재료 추가 성공.":
            print("냉장고 재료 추가 성공")
            return refrigerator, 2
        elif result == "냉장고 재료 추가 실패.":
            print("냉장고 재료 추가 실패")
            return refrigerator, 3
        else:
            print("i don't know in refri")
            return refrigerator, 6

class ControlMyPhoto_b():
    pass

class ControlMyRecipe_b():
    pass

class ControlPost_b():
    pass

