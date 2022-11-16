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
221116  사용자 작성 레시피 게시글 조회 완료.
        사용자 레시피 게시글 검색 완료

'''

class ControlRefrigerator_b():
    '''
    냉장고 조회 함수

    parameter       nickname:String 
    return type     List<Refrigerator>
    로 변경해야함.  
    '''
    def requestRefrigerator(self, nickname):
        print("내부 함수 : request Refrigerator start")
        try:
            ingredientsList = Refrigerator.objects.filter(nickname = nickname)

            if ingredientsList.exists():
                result, code = self.sendResult("냉장고 조회 성공.", ingredientsList)
                print("내부 함수 : 냉장고 조회 성공")
            else:
                result, code = self.sendResult("냉장고에 식재료가 없습니다.", None)
                print("내부 함수 : 냉장고 식재료 없음")
        except:
            result, code = self.sendResult("냉장고 조회 실패.", None)
            print("내부 함수 : 냉장고 조회 실패")
        return result, code

    def insertRefrigerator(self, refrigerator):
        print(f"내부 함수 : insert Refrigerator start")
        userRequest = refrigerator

        try:
            refriObject = Refrigerator.objects.create(amount = userRequest['amount'],
                expiry_date = userRequest['expiry_date'],
                name = Ingredients.objects.get(name = userRequest['name']),
                nickname = User.objects.get(nickname = userRequest['nickname']),
                unit = Units.objects.get(unit = userRequest['unit']))
                
            refriObject.save()

            result, code = self.sendResult("냉장고 재료 추가 성공.", None)
            print("내부 함수 : 냉장고 정보 추가 성공")
        except:
            result, code = self.sendResult("냉장고 재료 추가 실패.", None)
            print("내부 함수 : 냉장고 정보 추가 실패")
        return result, code

    '''
    냉장고 삭제 함수

    parameter       id:Integer
    return type     None
    로 변경해야함.
    '''
    def deleteRefrigerator(self, id, nickname, name):
        print("내부 함수 : deleteRefrigerator Start")
        try:
            deleteTarget = Refrigerator.objects.get(id = id)
            deleteTarget.delete()
            result, code = self.sendResult("냉장고 재료 삭제에 성공했습니다.", None)
            print("내부 함수 : 냉장고 재료 삭제 성공")
        except:
            result, code = self.sendResult("냉장고 재료 삭제에 실패했습니다.", None)
            print("내부 함수 : 냉장고 재료 삭제 실패")

        return result, code
    '''
    냉장고 변경 함수

    parameter       refrigerator:Refrigerator
    return type     None
    로 변경해야함.
    '''
    def updateRefrigerator(self, refrigerator):
        print("내부 함수 : updateRefrigerator Start")
        try:
            test = Refrigerator.objects.get(id = refrigerator["id"])
            Refrigerator.objects.filter(id = refrigerator["id"]).update(
                name = Ingredients.objects.get(name= refrigerator['name']),
                unit = Units.objects.get(unit = refrigerator["unit"]),
                amount = refrigerator["amount"],
                expiry_date = refrigerator["expiry_date"]
            )

            result, code = self.sendResult("냉장고 재료 변경 성공.", None)
            print("내부 함수 : 냉장고 재료정보 변경 성공")
        except:
            result, code = self.sendResult("냉장고 재료 변경 실패.", None)
            print("내부 함수: 냉장고 재료정보 변경 실패")

        return result, code

    def sendResult(self, result, refrigerator):
        if result == "냉장고 조회 실패.":
            print("sendResult : 냉장고 조회 실패")
            return refrigerator, 0
        elif result == "냉장고에 식재료가 없습니다.":
            print("sendResult : 냉장고 식재료 없음")
            return refrigerator, 1
        elif result == "냉장고 조회 성공.":
            print("sendResult : 냉장고 조회 성공")
            return refrigerator, 2

        elif result == "냉장고 재료 추가 실패.":
            print("sendResult : 냉장고 재료 추가 실패")
            return refrigerator, 3
        elif result == "냉장고 재료 추가 성공.":
            print("sendResult : 냉장고 재료 추가 성공")
            return refrigerator, 4

        elif result == "냉장고 재료 삭제에 실패했습니다.":
            print("sendResult : 냉장고 재료 삭제 실패")  
            return refrigerator, 5
        elif result == "냉장고 재료 삭제에 성공했습니다.":
            print("sendResult : 냉장고 재료 삭제 성공")
            return refrigerator, 6

        elif result == "냉장고 재료 변경 실패.":
            print("sendResult : 냉장고 재료 변경 실패")
            return refrigerator, 7
        elif result == "냉장고 재료 변경 성공.":
            print("sendResult : 냉장고 재료 변경 성공")
            return refrigerator, 8
        
        else:
            print("sendResult : 알 수 없는 오류")
            return refrigerator, 9

class ControlMyPhoto_b():
    def requestMyPhotoList(self, nickname):
        print("내부 함수 : requestMyPhotoList Start")

        try:
            photoList = PhotoPost.objects.filter(nickname = nickname)
        
            result, code = self.sendResult("사용자 작성 사진 게시글 조회 성공.", photoList)
            print("내부 함수 : 사용자 작성 사진 게시글 조회 성공")
        except:
            result, code = self.sendResult("사용자 작성 사진 게시글 조회 실패.", None)
            print("내부 함수 : 사용자 작성 사진 게시글 조회 실패.")

        return result, code 
    
    def sendResult(self, result, photoList):
        if result == "사용자 작성 사진 게시글 조회 실패.":
            print("sendResult : 사진게시글 조회 실패 응답")
            return photoList, 0
        elif result == "사용자 작성 사진 게시글 조회 성공.":
            print("sendResult : 사용자 작성 사진 게시글 조회 성공")
            return photoList, 1
        else:
            print("sendResult : 뭔 일인교..?")
            return photoList, 2

class ControlMyRecipe_b():
    '''
    return type     List<RecipePost>
    parameter       nickname:String
    시퀀스 12
    '''
    def requestMyRecipeList(self, nickname):
        print("내부 함수 : requestMyRecipeList Start")

        try:
            recipePosts = RecipePost.objects.filter(nickname = nickname)

            result, code = self.sendResult("사용자 작성 레시피 게시글 조회 성공.", recipePosts)
            print("내부 함수 : 사용자 작성 레시피 게시글 조회 성공")
        except:
            result, code = self.sendResult("사용자 작성 레시피 게시글 조회 실패.", None)
            print("내부 함수: 사용자 작성 레시피 게시글 조회 실패")
            
        return result, code

    '''
    return type     List<RecipePost>
    parameter       nickname:String, keyword:String
    시퀀스 13
    '''
    def queryMyRecipeList(self, nickname, keyword):
        print("내부 함수 : queryMyRecipeList Start")

        try:
            recipePosts = RecipePost.objects.filter(nickname = nickname, title = keyword)

            result, code = self.sendResult("사용자 작성 레시피 게시글 검색 성공.", recipePosts)
            print("내부 함수 : 사용자 작성 레시피 검색 성공")
        except:
            result, code = self.sendResult("사용자 작성 레시피 게시글 검색 실패.", None)
            print("내부 함수 : 사용자 작성 레시피 검색 실패")
        
        return result, code
    
    '''
    return type     List<RecipePost>
    parameter       nickname:String, arrangeBy:String
    시퀀스 14
    정렬 기준 : 좋아요 순, 최신글 순, 시간 대비 누적 조회수 순
    '''
    def arrangeMyRecipeList(self, nickname, arrangeBy):
        print("내부 함수 : arrangeMyRecipeList Start")
        if arrangeBy == "좋아요 순":
            try:
                orderedPosts = RecipePost.objects.filter(nickname = nickname).order_by('-like_count')
                result, code = self.sendResult("사용자 작성 레시피 정렬 성공.", orderedPosts)
                print("내부 함수 : 사용자 작성 레시피 좋아요 순 정렬 성공")
            except:
                result, code = self.sendResult("사용자 작성 레시피 정렬 실패.", orderedPosts)
                print("내부 함수 : 사용자 작성 레시피 좋아요 순 정렬 실패")
        elif arrangeBy == "최신글 순":
            try:
                orderedPosts = RecipePost.objects.filter(nickname = nickname).order_by('-upload_time')
                print(orderedPosts)
                result, code = self.sendResult("사용자 작성 레시피 정렬 성공.", orderedPosts)
                print("내부 함수 : 사용자 작성 레시피 최신글 순 정렬 성공")
            except:
                result, code = self.sendResult("사용자 작성 레시피 정렬 실패.", orderedPosts)
                print("내부 함수 : 사용자 작성 레시피 최신글 순 정렬 실패")
        elif arrangeBy == "조회수 순":
            try:
                orderedPosts = RecipePost.objects.filter(nickname = nickname).order_by('-views')
                result, code = self.sendResult("사용자 작성 레시피 정렬 성공.", orderedPosts)
                print("내부 함수 : 사용자 작성 레시피 조회수 순 정렬 성공")
            except:
                result, code = self.sendResult("사용자 작성 레시피 정렬 실패.", orderedPosts)
                print("내부 함수 : 사용자 작성 레시피 조회수 순 정렬 실패")
        else:
            result, code = self.sendResult("사용자 작성 레시피 정렬 실패.", None)
            print("내부 함수 : 사용자 작성 레시피 정렬 기준 오류")
    
        return result, code
    '''
    return type     response
    parameter       result:Integer, recipeList:List<RecipePost>
    '''
    def sendResult(self, result, recipeList):
        if result == "사용자 작성 레시피 게시글 조회 실패.":
            print("sendResult : 사용자 작성 레시피 게시글 조회 실패")
            return recipeList, 0
        elif result == "사용자 작성 레시피 게시글 조회 성공.":
            print("sendResult : 사용자 작성 레시피 게시글 조회 성공")
            return recipeList, 1
        
        elif result == "사용자 작성 레시피 게시글 검색 실패.":
            print("sendResult : 사용자 작성 레시피 게시글 검색 실패")
            return recipeList, 2
        elif result == "사용자 작성 레시피 게시글 검색 성공.":
            print("sendResult : 사용자 작성 레시피 게시글 검색 성공")
            return recipeList, 3

        elif result == "사용자 작성 레시피 정렬 실패.":
            print("sendResult : 사용자 작성 레시피 정렬 실패")
            return recipeList, 4
        elif result == "사용자 작성 레시피 정렬 성공.":
            print("sendResult : 사용자 작성 레시피 정렬 성공")
            return recipeList, 5

        else:
            print("sendResult : 알 수 없는 오류")
            return None, 6
            
class ControlPost_b():
    '''
    nickname: String
    postType: Int
    List<Post>
    '''
    def requestMyLikeList(nickname, postType):
        
        pass
    '''
    nickname: String
    List<RecipePost>
    '''
    def requestMyCommentList(nickname):
        pass
    '''
    result : int
    postList: List<Post>
    '''
    def sendResult(result, postList):
        pass

