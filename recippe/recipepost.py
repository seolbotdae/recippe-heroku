from rest_framework.generics import get_object_or_404

from .models import *

from .serializers import *

'''
221109  레시피 class 추가
221114  레시피 수정 함수 추가
221116  레시피 검색, 정렬 함수 추가
221117  레시피 게시판 댓글 작성 추가
        레시피 게시판 댓글 수정 추가
        레시피 게시판 댓글 삭제 추가
'''

class ControlRecipeList_b():
    def requestRecipeList(self, page):
        try:
            posts = RecipePost.objects.order_by('upload_time').reverse()
            postlist = posts[0+20*(page-1):20+20*(page-1)]
            result, recipeList = self.sendResult("레시피 게시판 조회 성공", postlist)
            pageCnt = int(len(posts)/20) + 1
        except:
            result, recipeList = self.sendResult("레시피 게시판 조회 실패", None)
            pageCnt = 0

        return result, recipeList, pageCnt

    def queryRecipeList(self, searchType, categories, keywordType, keyword, page):
        if searchType == "카테고리":
            try:
                categories = categories.split("-")
                posts = RecipePost.objects.filter(category__in = categories).order_by('upload_time').reverse()
                postlist = posts[0+20*(page-1):20+20*(page-1)]
                result, recipeList = self.sendResult("레시피 게시글 검색 성공", postlist)
                pageCnt = int(len(posts)/20) + 1
            except:
                result, recipeList = self.sendResult("레시피 게시글 검색 실패", None)
                pageCnt = 0
        elif searchType == "타이핑":
            if keywordType == "요리 이름":
                try:
                    posts = RecipePost.objects.filter(title__icontains=keyword).order_by('upload_time').reverse()
                    postlist = posts[0+20*(page-1):20+20*(page-1)]
                    result, recipeList = self.sendResult("레시피 게시글 검색 성공", postlist)
                    pageCnt = int(len(posts)/20) + 1
                except:
                    result, recipeList = self.sendResult("레시피 게시글 검색 실패", None)
                    pageCnt = 0
            elif keywordType == "작성자":
                try:
                    posts = RecipePost.objects.filter(nickname=keyword).order_by('upload_time').reverse()
                    postlist = posts[0+20*(page-1):20+20*(page-1)]
                    result, recipeList = self.sendResult("레시피 게시글 검색 성공", postlist)
                    pageCnt = int(len(posts)/20) + 1
                except:
                    result, recipeList = self.sendResult("레시피 게시글 검색 실패", None)
                    pageCnt = 0
            elif keywordType == "재료":
                try:
                    ids = Recipe_Ingredients.objects.filter(name=keyword).values_list('post_id', flat=True)
                    posts = RecipePost.objects.filter(post_id__in = ids).order_by('upload_time').reverse()
                    postlist = posts[0+20*(page-1):20+20*(page-1)]
                    result, recipeList = self.sendResult("레시피 게시글 검색 성공", postlist)
                    pageCnt = int(len(posts)/20) + 1
                except:
                    result, recipeList = self.sendResult("레시피 게시글 검색 실패", None)
                    pageCnt = 0
        
        return result, recipeList, pageCnt
                
    def arrangeRecipeList(self, arrangeBy, page):
        if arrangeBy == "최근 순":
            try:
                posts = RecipePost.objects.filter().order_by('upload_time').reverse()
                postlist = posts[0+20*(page-1):20+20*(page-1)]
                result, recipeList = self.sendResult("레시피 게시글 정렬 성공", postlist)
            except:
                result, recipeList = self.sendResult("레시피 게시글 정렬 실패", None)
        elif arrangeBy == "좋아요 순":
            try:
                posts = RecipePost.objects.filter().order_by('like_count').reverse()
                postlist = posts[0+20*(page-1):20+20*(page-1)]
                result, recipeList = self.sendResult("레시피 게시글 정렬 성공", postlist)
            except:
                result, recipeList = self.sendResult("레시피 게시글 정렬 실패", None)
        elif arrangeBy == "조회수 순":
            try:
                posts = RecipePost.objects.filter().order_by('views').reverse()
                postlist = posts[0+20*(page-1):20+20*(page-1)]
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
        try:
            post = RecipePost.objects.get(post_id = postId)
            result, recipePost = self.sendResult("레시피 게시글 조회 성공", post)
            current_views = post.views
            post.views = current_views+1
            RecipePost.save(post)
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

        if recipe.is_valid():
            recipe.save()
            posts = RecipePost.objects.filter(nickname=recipe.data['nickname']).order_by('upload_time').reverse()
            nr = posts[0]

            if newRecipe['Recipe_Ingredients'] != None:
                recipe_ingredients = newRecipe['Recipe_Ingredients']
                for ingre in recipe_ingredients:
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
            RecipePost.objects.filter(post_id=updatedRecipe['post_id']).update(title=updatedRecipe['title'])
            RecipePost.objects.filter(post_id=updatedRecipe['post_id']).update(category=updatedRecipe['category'])
            RecipePost.objects.filter(post_id=updatedRecipe['post_id']).update(degree_of_spicy=updatedRecipe['degree_of_spicy'])
            RecipePost.objects.filter(post_id=updatedRecipe['post_id']).update(description=updatedRecipe['description'])

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
    '''
    댓글 등록 메소드
    comment: Comment

    return int
    '''
    def insertComment(self, comment):
        print("내부 함수 : insertComment Start")
        try:            
            comment = CommentSerializer(data = comment)
            comment.is_valid()
            comment.save()

            code = self.sendResult("댓글 등록 성공.")
            print("내부 함수 : 댓글 등록 성공")
        except:
            code = self.sendResult("댓글 등록 실패.")
            print("내부 함수 : 댓글 등록 실패")
        
        return code


    '''
    게시글 정보 업데이트 메소드
    comment: Comment

    return int
    '''
    def updateComment(self, comment):
        print("내부 함수 : updateComment Start")
        try:            
            Comment.objects.filter(
                comment_id = comment['comment_id']
            ).update(comments = comment['comments'])

            code = self.sendResult("댓글 수정 성공.")
            print("내부 함수 : 댓글 수정 성공")
        except:
            code = self.sendResult("댓글 수정 실패.")
            print("내부 함수 : 댓글 수정 실패")
        
        return code

    '''
    댓글 삭제 메소드
    nickname: String
    commentId: int

    return int
    '''
    def deleteComment(self, nickname, commentId):
        print("내부 함수 : deleteComment Start")
        try:            
            d = Comment.objects.get(
                nickname = nickname,
                comment_id = commentId
            )
            
            d.delete()

            code = self.sendResult("댓글 삭제 성공.")
            print("내부 함수 : 댓글 삭제 성공")
        except:
            code = self.sendResult("댓글 삭제 실패.")
            print("내부 함수 : 댓글 삭제 실패")
        
        return code 

    '''
    sendResult
    result: int

    void-> 바꿈
    '''
    def sendResult(self, result):
        if result == "댓글 등록 실패.":
            print("sendResult : 댓글 등록 실패")
            return 0
        elif result == "댓글 등록 성공.":
            print("sendResult : 댓글 등록 성공")
            return 1
        elif result == "댓글 수정 실패.":
            print("sendResult : 댓글 수정 실패")
            return 2
        elif result == "댓글 수정 성공.":
            print("sendResult : 댓글 수정 성공")
            return 3
        elif result == "댓글 삭제 실패.":
            print("sendResult : 댓글 삭제 실패")
            return 4
        elif result == "댓글 삭제 성공.":
            print("sendResult : 댓글 삭제 성공")
            return 5
        else:
            return 6
