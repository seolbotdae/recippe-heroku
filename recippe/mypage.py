from .models import *

from .serializers import *

'''
221107 냉장고 조회 class 추가
221109 냉장고 조회 함수 작업중
'''

class ControlRefrigerator_b():
    def requestRefrigerator(self, nickname):
        refriData = Refrigerator.objects.filter(nickname = nickname)

        print(refriData)

        for i in range(len(refriData)):
            print(refriData[i].nickname)

        if len(refriData) == 0:
            result, code = self.sendResult("냉장고에 식재료가 없습니다.",refriData)
        else:
            result, code = self.sendResult("냉장고 조회 성공.", refriData)
        return result, code

    def insertRefrigerator(self, nickname, ingredient):
        pass
    def deleteRefrigerator(self, nickname, name):
        pass
    def updateRefrigerator(self, nickname, ingredient):
        pass
    def sendResult(self, result, refrigerator):
        if result == "냉장고에 식재료가 없습니다.":
            print("no food in refri")
            return refrigerator, result
        elif result == "냉장고 조회 성공.":
            print("yes food in refri")
            return refrigerator, result
        else:
            print("i don't know in refri")
            return refrigerator, 6

class ControlMyPhoto_b():
    pass

class ControlMyRecipe_b():
    pass

class ControlPost_b():
    pass

