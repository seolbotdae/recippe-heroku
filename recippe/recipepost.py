from rest_framework.generics import get_object_or_404

from .models import *

from .serializers import *

'''
221109 레시피 class 추가
221114 레시피 수정 함수 추가
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
        recipe = RecipeListSerializer(data=newRecipe)
        print(recipe)

        if recipe.is_valid():
            recipe.save()
            posts = RecipePost.objects.filter(nickname=recipe.data['nickname']).order_by('upload_time').reverse()
            nr = posts[0]

            recipe_ingredients = newRecipe['Recipe_Ingredients']
            for ingre in recipe_ingredients:
                postid = nr.post_id
                ingre['post_id'] = postid
                ingre = RecipeIngredientsSerializer(data=ingre)
                if ingre.is_valid():
                    ingre.save()
                
            result, recipePost = self.sendResult("레시피 게시글 등록 성공", nr)
        else:
            result, recipePost = self.sendResult("레시피 게시글 등록 실패", None)

        return result, recipePost

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



        