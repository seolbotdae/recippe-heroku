from .models import *

from .serializers import *

'''
221116  없는 재료 보여주기 추가
'''

class ControlIngredients_b():
    def requestUnExistIngredients(self, nickname, postId):
        try:
            recipeIngredients = Recipe_Ingredients.objects.filter(post_id=postId).values_list('name', flat=True)
            refrigerator = Refrigerator.objects.filter(nickname=nickname).values_list('name', flat=True)
            ingredientsList = []

            print(recipeIngredients)
            print(refrigerator)

            for ingre in recipeIngredients:
                if ingre not in refrigerator:
                    ueIngre = Recipe_Ingredients.objects.get(post_id=postId, name=ingre)
                    ingredientsList.append(ueIngre)
            
            print(ingredientsList)

            result, ueIngredients = self.sendResult("없는 재료 가져오기 성공", ingredientsList)
        except:
            result, ueIngredients = self.sendResult("없는 재료 가져오기 실패", None)

        return result, ueIngredients

    def sendResult(self, result, unExistIngredients=None):
        if result == "없는 재료 가져오기 실패":
            print(result)
            return 0, unExistIngredients
        elif result == "없는 재료 가져오기 성공":
            print(result)
            return 1, unExistIngredients
