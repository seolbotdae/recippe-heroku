from .models import *
from .serializers import *


class ControlRecipeList_b():
    def requestRecipeList(self, page):
        try:
            # 기본 기준인 최근 순으로 데이터 가져옴
            posts = RecipePost.objects.order_by('upload_time').reverse()
            # 1페이지당 20개
            postlist = posts[0+15*(page-1):15+15*(page-1)]
            result, recipeList = self.sendResult("레시피 게시판 조회 성공", postlist)
            pageCnt = int(len(posts)/15) + 1
        except:
            result, recipeList = self.sendResult("레시피 게시판 조회 실패", None)
            pageCnt = 0

        return result, recipeList, pageCnt

    def queryRecipeList(self, searchType, categories, keywordType, keyword, page):
        # 검색 방법에 따라 다른 절차
        if searchType == "카테고리":
            try:
                # 카테고리들을 가져온 후 DB 에서 검색
                categories = categories.split("-")
                posts = RecipePost.objects.filter(category__in = categories).order_by('upload_time').reverse()
                postlist = posts[0+15*(page-1):15+15*(page-1)]
                result, recipeList = self.sendResult("레시피 게시글 검색 성공", postlist)
                pageCnt = int(len(posts)/15) + 1
            except:
                result, recipeList = self.sendResult("레시피 게시글 검색 실패", None)
                pageCnt = 0
        elif searchType == "타이핑":
            # 타이핑 검색 시 기준 선택 가능
            if keywordType == "요리 이름":
                try:
                    # 이름이 포함 + 최근순
                    posts = RecipePost.objects.filter(title__icontains=keyword).order_by('upload_time').reverse()
                    postlist = posts[0+15*(page-1):15+15*(page-1)]
                    result, recipeList = self.sendResult("레시피 게시글 검색 성공", postlist)
                    pageCnt = int(len(posts)/15) + 1
                except:
                    result, recipeList = self.sendResult("레시피 게시글 검색 실패", None)
                    pageCnt = 0
            elif keywordType == "작성자":
                try:
                    # 작성자가 작성함 + 최근순
                    posts = RecipePost.objects.filter(nickname=keyword).order_by('upload_time').reverse()
                    postlist = posts[0+15*(page-1):15+15*(page-1)]
                    result, recipeList = self.sendResult("레시피 게시글 검색 성공", postlist)
                    pageCnt = int(len(posts)/15) + 1
                except:
                    result, recipeList = self.sendResult("레시피 게시글 검색 실패", None)
                    pageCnt = 0
            elif keywordType == "재료":
                try:
                    # 재료를 포함함 + 최근순
                    ids = Recipe_Ingredients.objects.filter(name=keyword).values_list('post_id', flat=True)
                    posts = RecipePost.objects.filter(post_id__in = ids).order_by('upload_time').reverse()
                    postlist = posts[0+15*(page-1):15+15*(page-1)]
                    result, recipeList = self.sendResult("레시피 게시글 검색 성공", postlist)
                    pageCnt = int(len(posts)/15) + 1
                except:
                    result, recipeList = self.sendResult("레시피 게시글 검색 실패", None)
                    pageCnt = 0
        
        return result, recipeList, pageCnt
                
    def arrangeRecipeList(self, arrangeBy, page):
        # 정렬 기준에 따라 다른 처리
        if arrangeBy == "최근 순":
            try:
                posts = RecipePost.objects.filter().order_by('upload_time').reverse()
                postlist = posts[0+15*(page-1):15+15*(page-1)]
                result, recipeList = self.sendResult("레시피 게시글 정렬 성공", postlist)
            except:
                result, recipeList = self.sendResult("레시피 게시글 정렬 실패", None)
        elif arrangeBy == "좋아요 순":
            try:
                posts = RecipePost.objects.filter().order_by('like_count').reverse()
                postlist = posts[0+15*(page-1):15+15*(page-1)]
                result, recipeList = self.sendResult("레시피 게시글 정렬 성공", postlist)
            except:
                result, recipeList = self.sendResult("레시피 게시글 정렬 실패", None)
        elif arrangeBy == "조회수 순":
            try:
                posts = RecipePost.objects.filter().order_by('views').reverse()
                postlist = posts[0+15*(page-1):15+15*(page-1)]
                result, recipeList = self.sendResult("레시피 게시글 정렬 성공", postlist)
            except:
                result, recipeList = self.sendResult("레시피 게시글 정렬 실패", None)

        return result, recipeList

    def sendResult(self, result, recipeList=None):
        if result == "레시피 게시판 조회 실패":
            print(f"{result}, {0}")
            return 0, recipeList
        elif result == "레시피 게시판 조회 성공":
            print(f"{result}, {len(recipeList)}")
            return 1, recipeList
        elif result == "레시피 게시글 검색 실패":
            print(f"{result}, {0}")
            return 2, recipeList
        elif result == "레시피 게시글 검색 성공":
            print(f"{result}, {len(recipeList)}")
            return 3, recipeList
        elif result == "레시피 게시글 정렬 실패":
            print(f"{result}, {0}")
            return 4, recipeList
        elif result == "레시피 게시글 정렬 성공":
            print(f"{result}, {len(recipeList)}")
            return 5, recipeList

class ControlRecipe_b():
    def requestRecipe(self, postId, nickname):
        print(postId)
        # 요청한 Id 에 맞는 레시피 게시글 조회
        try:
            post = RecipePost.objects.get(post_id = postId)
            result, recipePost = self.sendResult("레시피 게시글 조회 성공", post)
            # 조회수 1 증가
            current_views = post.views
            post.views = current_views+1
            RecipePost.save(post)
            # 사용자가 좋아요를 누른 게시글인지 확인
            isLiked = LikeInfo.objects.filter(post_id = postId, nickname = nickname, post_type=1)
            print(isLiked)
            if len(isLiked) == 0:
                likeInfo = False
            else: likeInfo = True
        except:
            result, recipePost = self.sendResult("레시피 게시글 조회 실패", None)
            likeInfo = True

        return result, recipePost, likeInfo

    def insertRecipe(self, newRecipe):
        recipe = RecipeListSerializer(data=newRecipe)
        print(recipe)

        # 레시피 게시글 저장
        if recipe.is_valid():
            recipe.save()
            posts = RecipePost.objects.filter(nickname=recipe.data['nickname']).order_by('upload_time').reverse()
            nr = posts[0]
            
            # 레시피 게시글을 저장할 때에는 레시피에 포함된 식재료들도(Recipe_Ingredients) 저장을 해주어야함
            if newRecipe['Recipe_Ingredients'] != None:
                recipe_ingredients = newRecipe['Recipe_Ingredients']
                for ingre in recipe_ingredients:
                    # 저장된 레시피 게시글의 Id 가져오기
                    postid = nr.post_id
                    ingre['post_id'] = postid
                    ingre = RecipeIngredientsSerializer(data=ingre)
                    if ingre.is_valid():
                        ingre.save()
                
            result, newRecipe = self.sendResult("레시피 게시글 등록 성공", nr)
        else:
            result, newRecipe = self.sendResult("레시피 게시글 등록 실패", None)

        return result, newRecipe

    def updateRecipe(self, updatedRecipe):
        try:
            # 레시피 게시글의 정보 업데이트
            RecipePost.objects.filter(post_id=updatedRecipe['post_id']).update(title=updatedRecipe['title'])
            RecipePost.objects.filter(post_id=updatedRecipe['post_id']).update(category=updatedRecipe['category'])
            RecipePost.objects.filter(post_id=updatedRecipe['post_id']).update(degree_of_spicy=updatedRecipe['degree_of_spicy'])
            RecipePost.objects.filter(post_id=updatedRecipe['post_id']).update(description=updatedRecipe['description'])

            # 기존의 재료들 삭제하고 새로 업데이트된 재료들을 저장
            Recipe_Ingredients.objects.filter(post_id=updatedRecipe['post_id']).delete()
            update_ingredients = updatedRecipe['Recipe_Ingredients']
            for uingre in update_ingredients:
                uingre = RecipeIngredientsSerializer(data=uingre)
                if uingre.is_valid():
                    uingre.save()
            
            result, updatedRecipe = self.sendResult("레시피 게시글 수정 성공", updatedRecipe)
        except:
            result, updatedRecipe = self.sendResult("레시피 게시글 수정 실패", None)
        
        return result, updatedRecipe

    def deleteRecipe(self, nickname, postId):
        try:
            # 레시피 게시글 정보 가져와서 삭제 + 관련된 좋아요, 신고 정보도 삭제 + 재료의 경우 자동으로 삭제됨
            deleteTarget = RecipePost.objects.get(nickname=nickname, post_id=postId)
            deleteTarget.delete()
            likeInfos = LikeInfo.objects.filter(post_id=postId, post_type=1)
            likeInfos.delete()
            reports = Report.objects.filter(post_id=postId, post_type=1)
            reports.delete()

            result = self.sendResult("레시피 게시글 삭제 성공")
        except:
            result = self.sendResult("레시피 게시글 삭제 실패")

        return result

    def sendResult(self, result, recipePost=None):
        if result == "레시피 게시글 조회 실패":
            print(f"{result}, {0}")
            return 0, recipePost
        elif result == "레시피 게시글 조회 성공":
            print(f"{result}, {recipePost}")
            return 1, recipePost
        elif result == "레시피 게시글 등록 실패":
            print(f"{result}, {0}")
            return 2, recipePost
        elif result == "레시피 게시글 등록 성공":
            print(f"{result}, {recipePost}")
            return 3, recipePost
        elif result == "레시피 게시글 수정 실패":
            print(f"{result}, {0}")
            return 4, recipePost
        elif result == "레시피 게시글 수정 성공":
            print(f"{result}, {recipePost}")
            return 5, recipePost
        elif result == "레시피 게시글 삭제 실패":
            print(f"{result}, {0}")
            return 6
        elif result == "레시피 게시글 삭제 성공":
            print(f"{result}, {0}")
            return 7

class ControlComment_b():
    def insertComment(self, comment):
        try:            
            # 댓글 정보 생성 후 저장
            comment = CommentSerializer(data = comment)
            comment.is_valid()
            comment.save()
            comments = Comment.objects.filter(post_id=comment['post_id'])
            RecipePost.objects.filter(post_id=comment['post_id']).update(comment_count=len(comments)) # 좋아요 수 업데이트

            code = self.sendResult("댓글 등록 성공")
        except:
            code = self.sendResult("댓글 등록 실패")
        
        return code

    def updateComment(self, comment):
        try:            
            # 기존의 댓글 정보 DB 에서 가져온 후 내용 수정
            Comment.objects.filter(
                comment_id = comment['comment_id']
            ).update(comments = comment['comments'])

            code = self.sendResult("댓글 수정 성공")
        except:
            code = self.sendResult("댓글 수정 실패")
        
        return code

    def deleteComment(self, nickname, commentId):
        try:            
            # 기존 정보 가져온 후 삭제
            d = Comment.objects.get(
                nickname = nickname,
                comment_id = commentId
            )
            
            d.delete()

            code = self.sendResult("댓글 삭제 성공")
        except:
            code = self.sendResult("댓글 삭제 실패")
        
        return code 

    def sendResult(self, result):
        if result == "댓글 등록 실패":
            print(result)
            return 0
        elif result == "댓글 등록 성공":
            print(result)
            return 1
        elif result == "댓글 수정 실패":
            print(result)
            return 2
        elif result == "댓글 수정 성공":
            print(result)
            return 3
        elif result == "댓글 삭제 실패":
            return 4
        elif result == "댓글 삭제 성공":
            return 5