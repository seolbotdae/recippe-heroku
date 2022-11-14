from rest_framework.generics import get_object_or_404

from .models import *

from .serializers import *

'''
221109 레시피 class 추가
'''

class ControlRecipeList_b():
    def requestRecipeList(self, page):
        try:
            posts = RecipePost.objects.order_by('upload_time').reverse()
            postlist = posts[0+20*(page-1):20+20*(page-1)]
            result, recipeList = self.sendResult("레시피 게시판 조회 성공", postlist)
        except:
            result, recipeList = self.sendResult("레시피 게시판 조회 실패", None)

        return result, recipeList

    def sendResult(self, result, recipeList):
        if result == "레시피 게시판 조회 실패":
            print(f"{result}, {0}")
            return 0, recipeList
        elif result == "레시피 게시판 조회 성공":
            print(f"{result}, {len(recipeList)}")
            return 99, recipeList

class ControlRecipe_b():
    def requestRecipe(self, postId):
        print(postId)
        try:
            post = RecipePost.objects.get(post_id = postId)
            result, recipePost = self.sendResult("레시피 게시글 조회 성공", post)
            current_views = post.views
            post.views = current_views+1
            RecipePost.save(post)
        except:
            result, recipePost = self.sendResult("레시피 게시글 조회 실패", None)

        return result, recipePost

    def insertRecipe(self, newRecipe):
        newRecipe = RecipeListSerializer(data=newRecipe)
        print(newRecipe)
        if newRecipe.is_valid():
            newRecipe.save()
            posts = RecipePost.objects.filter(nickname=newRecipe.data['nickname']).order_by('upload_time').reverse()
            newRecipe = posts[0]
            result, recipePost = self.sendResult("레시피 게시글 등록 성공", newRecipe)
        else:
            result, recipePost = self.sendResult("레시피 게시글 등록 실패", None)

        return result, recipePost

    def sendResult(self, result, recipePost):
        if result == "레시피 게시글 등록 실패":
            print(f"{result}, {recipePost}")
            return 0, recipePost
        elif result == "레시피 게시글 등록 성공":
            print(f"{result}, {0}")
            return 99, recipePost


        