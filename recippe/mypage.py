from .models import *

from .serializers import *
# json 임포트
import json
'''
221107  냉장고 조회 class 추가
221109  냉장고 조회 함수 작업중
221114  냉장고 조회 함수 작업 완료
        냉장고 재료 추가 함수 작업중
221115  냉장고 재료 추가 함수 작업 완료.
        냉장고 재료 삭제 함수 작업 완료.
        냉장고 재료 변경 함수 작업 완료.
        사용자 작성 사진 게시글 조회 완료.
221116  사용자 작성 레시피 게시글 조회 작업중.
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
        userRequest = refrigerator

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

    '''
    냉장고 삭제 함수

    parameter       id:Integer
    return type     None
    로 변경해야함.
    '''
    def deleteRefrigerator(self, id, nickname, name):

        try:
            deleteTarget = Refrigerator.objects.get(id = id)
            deleteTarget.delete()
            result, code = self.sendResult("냉장고 재료 삭제에 성공했습니다.", None)
            print("식재료 삭제 성공")
        except:
            result, code = self.sendResult("냉장고 재료 삭제에 실패했습니다.", None)
            print("식재료 삭제 실패")

        return result, code
    '''
    냉장고 변경 함수

    parameter       refrigerator:Refrigerator
    return type     None
    로 변경해야함.
    '''
    def updateRefrigerator(self, refrigerator):
        try:
            test = Refrigerator.objects.get(id = refrigerator["id"])
            Refrigerator.objects.filter(id = refrigerator["id"]).update(
                name = Ingredients.objects.get(name= refrigerator['name']),
                unit = Units.objects.get(unit = refrigerator["unit"]),
                amount = refrigerator["amount"],
                expiry_date = refrigerator["expiry_date"]
            )

            print("서버 : 냉장고 재료정보 변경 성공")
            result, code = self.sendResult("냉장고 재료 변경 성공.", None)
        except:
            print("서버 : 냉장고 재료정보 변경 실패")
            result, code = self.sendResult("냉장고 재료 변경 실패.", None)

        return result, code

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

        elif result == "냉장고 재료 삭제에 성공했습니다.":
            print("냉장고 재료 삭제 성공")
            return refrigerator, 4
        elif result == "냉장고 재료 삭제에 실패했습니다.":
            print("냉장고 재료 삭제 실패")
            return refrigerator, 5

        elif result == "냉장고 재료 변경 성공.":
            print("냉장고 재료 변경 성공")
            return refrigerator, 7
        elif result == "냉장고 재료 변경 실패.":
            print("냉장고 재료 변경 실패")
            return refrigerator, 8
    
        else:
            print("뭔 일인겨..?")
            return refrigerator, 6

class ControlMyPhoto_b():
    def requestMyPhotoList(self, nickname):
        print("requestMyPhotoList 함수 실행")
        
        if PhotoPost.objects.filter(nickname = nickname).exists():
            print("서버 : 사용자 작성 사진 게시글 조회 성공")
            result, code = self.sendResult("사용자 작성 사진 게시글 조회 성공.",
                PhotoPost.objects.filter(nickname = nickname))
        elif len(PhotoPost.objects.filter(nickname = nickname)) == 0:
            print("서버 : 사용자가 작성한 가진 게시글이 없음.")
            result, code = self.sendResult("사용자 작성 사진 게시글 없음.",
                PhotoPost.objects.filter(nickname = nickname))
        else:
            print("서버 : 사용자 작성 사진 게시글 조회 실패.")
            result, code = self.sendResult("사용자 작성 사진 게시글 조회 실패.", None)

        return result, code 
    
    def sendResult(self, result, photoList):
        if result == "사용자 작성 사진 게시글 조회 성공.":
            print("사진게시글 조회 성공 응답")
            return photoList, 0
        elif result == "사용자 작성 사진 게시글 조회 실패.":
            print("사진게시글 조회 실패 응답")
            return photoList, 1
        elif result == "사용자 작성 사진 게시글 없음.":
            print("사용자 작성 사진 게시글 없음")
            return None, 2
        else:
            print("뭔 일인교..?")
            return photoList, 6

class ControlMyRecipe_b():
    '''
    return type     List<RecipePost>
    parameter       nickname:String
    시퀀스 12
    '''
    def requestMyRecipeList(self, nickname):
        print("requestMyRecipeList 함수 실행")

        if RecipePost.objects.filter(nickname = nickname).exists():
            print("서버 : 사용자 작성 레시피 게시글 조회 성공")
            result, code = self.sendResult("사용자 작성 레시피 게시글 조회 성공.",
                RecipePost.objects.filter(nickname = nickname))
        elif len(RecipePost.objects.filter(nickname = nickname)) == 0:
            print("서버 : 사용자가 작성한 레시피 게시글이 없음")
            result, code = self.sendResult("사용자 작성 레시피 게시글 없음.",
                RecipePost.objects.filter(nickname = nickname))
        else:
            print("서버 : 사용자 작성 레시피 게시글 조회 실패")
            result, code = self.sendResult("사용자 작성 레시피 게시글 조회 실패.", None)
        
        return result, code

    '''
    return type     List<RecipePost>
    parameter       nickname:String, keyword:String
    시퀀스 13
    '''
    def queryMyRecipeList(self, nickname, keyword):
        pass
    
    '''
    return type     List<RecipePost>
    parameter       nickname:String, arrangeBy:String
    시퀀스 14
    '''
    def arrangeMyRecipeList(self, nickname, arrangeBy):
        pass

    '''
    return type     response
    parameter       result:Integer, recipeList:List<RecipePost>
    '''
    def sendResult(self, result, recipeList):
        if result == "사용자 작성 레시피 게시글 조회 실패.":
            return recipeList, 1
        elif result == "사용자 작성 레시피 게시글 없음.":
            return recipeList, 2
        elif result == "사용자 작성 레시피 게시글 조회 성공.":
            return recipeList, 3
        else:
            return None, 0
            

class ControlPost_b():
    pass

