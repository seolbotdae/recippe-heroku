from .models import *

from .serializers import *

'''
221116  없는 재료 보여주기 추가
        남은 재료 계산하기 추가
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
                    print(ueIngre)
                    ingredientsList.append(ueIngre)
            
            print(ingredientsList)

            result, ueIngredients = self.sendResult("없는 재료 가져오기 성공", ingredientsList)
        except:
            result, ueIngredients = self.sendResult("없는 재료 가져오기 실패", None)

        return result, ueIngredients

    def decreaseAmmounts(self, nickname, postId):
        try:
            recipeIngredients = Recipe_Ingredients.objects.filter(post_id=postId).values_list('name', 'amount').order_by('name')
            refrigerator = Refrigerator.objects.filter(nickname=nickname).values_list('name', 'amount').order_by('name')

            print(recipeIngredients)
            print(refrigerator)

            for idx in range(len(refrigerator)):
                Refrigerator.objects.filter(nickname=nickname, name=refrigerator[idx][0]).update(amount=refrigerator[idx][1]-recipeIngredients[idx][1])

            result = self.sendResult("남은 재료 계산하기 성공")
        except:
            result = self.sendResult("남은 재료 계산하기 실패")

        return result

    def sendResult(self, result, unExistIngredients=None):
        if result == "없는 재료 가져오기 실패":
            print(result)
            return 0, unExistIngredients
        elif result == "없는 재료 가져오기 성공":
            print(result)
            return 1, unExistIngredients
        elif result == "남은 재료 계산하기 실패":
            print(result)
            return 2
        elif result == "남은 재료 계산하기 성공":
            print(result)
            return 3
