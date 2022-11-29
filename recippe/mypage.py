from .models import *

from .serializers import *



class ControlRefrigerator_b():
    def requestRefrigerator(self, nickname):
        try:
            # 요청받은 닉네임의 사용자가 등록한 식재료 DB 에서 가져옴
            ingredientsList = Refrigerator.objects.filter(nickname = nickname)
            
            for ingre in ingredientsList:
                if ingre.amount >= 1000:
                    if ingre.unit.unit == "ml":
                        afterAmount = ingre.amount / 1000
                        ingre.amount = afterAmount
                        ingre.unit = Units.objects.get(unit='l')
                    elif ingre.unit.unit == "g":
                        afterAmount = ingre.amount / 1000
                        ingre.amount = afterAmount
                        ingre.unit = Units.objects.get(unit='kg')
                    
            if ingredientsList.exists():
                result, code = self.sendResult("냉장고 조회 성공", ingredientsList)
            else:
                result, code = self.sendResult("냉장고에 식재료가 없음", None)
        except:
            result, code = self.sendResult("냉장고 조회 실패", None)

        return result, code

    def insertRefrigerator(self, refrigerator):
        userRequest = refrigerator
        inputUnit = userRequest['unit']
        if inputUnit == 'kg':
            changedAmount = userRequest['amount'] * 1000
            changedUnit = 'g'
        elif inputUnit == 'l':
            changedAmount = userRequest['amount'] * 1000
            changedUnit = 'ml'
        else: 
            changedAmount = userRequest['amount']
            changedUnit = userRequest['unit']

        try:
            # 받은 식재료 정보 생성 후 저장
            refriObject = Refrigerator.objects.create(amount = changedAmount,
                expiry_date = userRequest['expiry_date'],
                name = Ingredients.objects.get(name = userRequest['name']),
                nickname = User.objects.get(nickname = userRequest['nickname']),
                unit = Units.objects.get(unit = changedUnit))
                
            refriObject.save()

            result, code = self.sendResult("냉장고 재료 추가 성공", None)
        except:
            result, code = self.sendResult("냉장고 재료 추가 실패", None)

        return result, code

    def deleteRefrigerator(self, id):
        try:
            # id 를 갖는 재료 삭제
            deleteTarget = Refrigerator.objects.get(id = id)
            deleteTarget.delete()
            result, code = self.sendResult("냉장고 재료 삭제 성공", None)
        except:
            result, code = self.sendResult("냉장고 재료 삭제 실패", None)

        return result, code

    def updateRefrigerator(self, refrigerator):
        userRequest = refrigerator
        inputUnit = userRequest['unit']
        if inputUnit == 'kg':
            changedAmount = userRequest['amount'] * 1000
            changedUnit = 'g'
        elif inputUnit == 'l':
            changedAmount = userRequest['amount'] * 1000
            changedUnit = 'ml'
        else: 
            changedAmount = userRequest['amount']
            changedUnit = userRequest['unit']

        try:
            # 수정된 정보들로 업데이트
            test = Refrigerator.objects.get(id = refrigerator["id"])
            Refrigerator.objects.filter(id = refrigerator["id"]).update(
                name = Ingredients.objects.get(name= refrigerator['name']),
                unit = Units.objects.get(unit = changedUnit),
                amount = changedAmount,
                expiry_date = refrigerator["expiry_date"]
            )

            result, code = self.sendResult("냉장고 재료 변경 성공", None)
        except:
            result, code = self.sendResult("냉장고 재료 변경 실패", None)

        return result, code

    def sendResult(self, result, refrigerator):
        if result == "냉장고 조회 실패":
            print(result)
            return refrigerator, 0
        elif result == "냉장고에 식재료가 없음":
            print(result)
            return refrigerator, 1
        elif result == "냉장고 조회 성공":
            print(result)
            return refrigerator, 2
        elif result == "냉장고 재료 추가 실패":
            print(result)
            return refrigerator, 3
        elif result == "냉장고 재료 추가 성공":
            print(result)
            return refrigerator, 4
        elif result == "냉장고 재료 삭제 실패":
            print(result)
            return refrigerator, 5
        elif result == "냉장고 재료 삭제 성공":
            print(result)
            return refrigerator, 6
        elif result == "냉장고 재료 변경 실패":
            print(result)
            return refrigerator, 7
        elif result == "냉장고 재료 변경 성공":
            print(result)
            return refrigerator, 8

class ControlMyPhoto_b():
    def requestMyPhotoList(self, nickname):
        try:
            # 사용자의 닉네임으로 등록된 게시글 조회
            photoList = PhotoPost.objects.filter(nickname = nickname)
        
            result, code = self.sendResult("사용자 작성 사진 게시글 조회 성공", photoList)
        except:
            result, code = self.sendResult("사용자 작성 사진 게시글 조회 실패", None)

        return result, code 
    
    def sendResult(self, result, photoList):
        if result == "사용자 작성 사진 게시글 조회 실패":
            print(result)
            return photoList, 0
        elif result == "사용자 작성 사진 게시글 조회 성공":
            print(result)
            return photoList, 1

class ControlMyRecipe_b():
    def requestMyRecipeList(self, nickname):
        try:
            # 사용자의 닉네임으로 등록된 게시글 조회
            recipePosts = RecipePost.objects.filter(nickname = nickname)

            result, code = self.sendResult("사용자 작성 레시피 게시글 조회 성공", recipePosts)
        except:
            result, code = self.sendResult("사용자 작성 레시피 게시글 조회 실패", None)
            
        return result, code

    def queryMyRecipeList(self, nickname, keyword):
        try:
            # 사용자의 닉네임으로 등록되어있으며, 키워드를 타이틀에 포함하는 게시글 검색
            recipePosts = RecipePost.objects.filter(nickname = nickname, title__icontains = keyword)

            result, code = self.sendResult("사용자 작성 레시피 게시글 검색 성공", recipePosts)
        except:
            result, code = self.sendResult("사용자 작성 레시피 게시글 검색 실패", None)
        
        return result, code

    def arrangeMyRecipeList(self, nickname, arrangeBy):
        # 정렬 기준에 따라 다른 처리 + 사용자의 닉네임으로 등록된 게시글들만을 조회
        if arrangeBy == "좋아요 순":
            try:
                orderedPosts = RecipePost.objects.filter(nickname = nickname).order_by('-like_count')
                result, code = self.sendResult("사용자 작성 레시피 정렬 성공", orderedPosts)
            except:
                result, code = self.sendResult("사용자 작성 레시피 정렬 실패", orderedPosts)
        elif arrangeBy == "최신글 순":
            try:
                orderedPosts = RecipePost.objects.filter(nickname = nickname).order_by('-upload_time')
                print(orderedPosts)
                result, code = self.sendResult("사용자 작성 레시피 정렬 성공", orderedPosts)
            except:
                result, code = self.sendResult("사용자 작성 레시피 정렬 실패", orderedPosts)
        elif arrangeBy == "조회수 순":
            try:
                orderedPosts = RecipePost.objects.filter(nickname = nickname).order_by('-views')
                result, code = self.sendResult("사용자 작성 레시피 정렬 성공", orderedPosts)
            except:
                result, code = self.sendResult("사용자 작성 레시피 정렬 실패", orderedPosts)
        else:
            result, code = self.sendResult("사용자 작성 레시피 정렬 실패", None)
    
        return result, code

    def sendResult(self, result, recipeList):
        if result == "사용자 작성 레시피 게시글 조회 실패":
            print(result)
            return recipeList, 0
        elif result == "사용자 작성 레시피 게시글 조회 성공":
            print(result)
            return recipeList, 1
        elif result == "사용자 작성 레시피 게시글 검색 실패":
            print(result)
            return recipeList, 2
        elif result == "사용자 작성 레시피 게시글 검색 성공":
            print(result)
            return recipeList, 3
        elif result == "사용자 작성 레시피 정렬 실패":
            print(result)
            return recipeList, 4
        elif result == "사용자 작성 레시피 정렬 성공":
            print(result)
            return recipeList, 5
            
class ControlPost_b():
    def requestMyLikeList(self, nickname, postType):
        # 레시피 좋아요 찾는 분기
        if postType == 1:
            try:
                postTarget = LikeInfo.objects.filter(nickname=nickname, post_type = postType)
                targetList = []

                for i in postTarget:
                    targetList.append(i.post_id)
                
                likeRecipes = RecipePost.objects.filter(post_id__in = targetList)
                result, code = self.sendResult("사용자 좋아요 게시글 조회 성공", likeRecipes)
            except:
                result, code = self.sendResult("사용자 좋아요 게시글 조회 실패", None)
        # 사진 좋아요 찾는 분기
        elif postType == 2:
            try:
                postTarget = LikeInfo.objects.filter(nickname=nickname, post_type = postType)
                targetList = []

                for i in postTarget:
                    targetList.append(i.post_id)

                likePhotos = PhotoPost.objects.filter(post_id__in = targetList)
                result, code = self.sendResult("사용자 좋아요 게시글 조회 성공", likePhotos)
            except:
                result, code = self.sendResult("사용자 좋아요 게시글 조회 실패", None)
        # 아무 분기도 아닌 경우
        else:
            result, code = self.sendResult("사용자 좋아요 게시글 조회 실패", None)
       
        return result, code

    def requestMyCommentList(self, nickname):
        try:
            # 댓글 작성한 시간을 역순으로 하여 조회
            postTarget = Comment.objects.filter(nickname=nickname).order_by("-comment_time").values("post_id")
            targetList = []

            for i in postTarget:
                targetList.append(i['post_id'])

            # 댓글들의 데이터에 포함된 post_id 로 댓글이 작성된 게시글 리스트들 조회
            commentPosts = RecipePost.objects.filter(post_id__in = targetList)
            
            result, code = self.sendResult("사용자 댓글단 게시글 조회 성공", commentPosts)
        except:
            result, code = self.sendResult("사용자 댓글단 게시글 조회 실패", None)

        return result, code

    def sendResult(self, result, postList):
        if result == "사용자 좋아요 게시글 조회 실패":
            print(result)
            return postList, 0
        elif result == "사용자 좋아요 게시글 조회 성공":
            print(result)
            return postList, 1
        elif result == "사용자 댓글단 게시글 조회 실패":
            print(result)
            return postList, 2
        elif result == "사용자 댓글단 게시글 조회 성공":
            print(result)
            return postList, 3