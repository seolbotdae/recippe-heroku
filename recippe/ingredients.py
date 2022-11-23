from .models import *

from .serializers import *



class ControlIngredients_b():
    def requestUnExistIngredients(self, nickname, postId):
        try:
            # 레시피 재료의 이름들, 냉장고(사용자 보유 재료)의 이름들
            recipeIngredients = Recipe_Ingredients.objects.filter(post_id=postId).values_list('name', flat=True)
            refrigerator = Refrigerator.objects.filter(nickname=nickname).values_list('name', flat=True)
            ingredientsList = []
            
            # 레시피의 재료중 냉장고에 없는것만 리스트에 저장
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
            # 레시피 재료의 이름, 총 양들, 냉장고의 이름, 총 양들
            recipeIngredients = Recipe_Ingredients.objects.filter(post_id=postId).values_list('name', 'amount').order_by('name')
            refrigerator = Refrigerator.objects.filter(nickname=nickname).values_list('name', 'amount').order_by('name')

            # 재료 감산 후 업데이트
            for idx in range(len(recipeIngredients)):
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
