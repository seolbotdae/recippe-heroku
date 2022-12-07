from .models import *

from .serializers import *



class ControlIngredients_b():
    def requestUnExistIngredients(self, nickname, postId):
        try:
            # 레시피 재료의 이름들, 냉장고(사용자 보유 재료)의 이름들
            recipeIngredients = Recipe_Ingredients.objects.filter(post_id=postId).values_list('name', flat=True)
            refrigerator = Refrigerator.objects.filter(nickname=nickname).values_list('name', flat=True)
            noExistList = []
            yesExistList = []
            
            # 레시피의 재료중 냉장고에 없는것만 리스트에 저장
            for ingre in recipeIngredients:
                if ingre not in refrigerator:
                    noExistList.append(ingre)
                else:
                    yesExistList.append(ingre)

            print(noExistList, yesExistList)
            
            # 없는 것만 모은 식재료중 레시피에서 요구하는 만큼 amount 가 남아있는지 확인
            realList = []
            for ingre in yesExistList:
                checkRefri = Refrigerator.objects.get(nickname=nickname, name=ingre)
                checkRecipe = Recipe_Ingredients.objects.get(post_id=postId, name=ingre)
                if checkRecipe.unit == 'T':
                    if checkRefri.amount < 15*checkRecipe.amount:
                        realList.append(checkRecipe)
                else:
                    if checkRefri.amount < checkRecipe.amount:
                        realList.append(checkRecipe)
            
            # 아까 없던 재료 그대로 다시 복사
            for ingre in noExistList:
                ri = Recipe_Ingredients.objects.get(post_id=postId, name=ingre)
                realList.append(ri)

            result, ueIngredients = self.sendResult("없는 재료 가져오기 성공", realList)
        except:
            result, ueIngredients = self.sendResult("없는 재료 가져오기 실패", None)

        return result, ueIngredients

    def decreaseAmmounts(self, nickname, postId):
        try:
            # 레시피 재료의 이름, 총 양들, 냉장고의 이름, 총 양들
            recipeIngredients = Recipe_Ingredients.objects.filter(post_id=postId)
            refrigerator = Refrigerator.objects.filter(nickname=nickname)

            print(recipeIngredients, refrigerator)

            # 재료 감산 후 업데이트
            for idx in range(len(recipeIngredients)):
                print(recipeIngredients[idx].unit, recipeIngredients[idx].name, recipeIngredients[idx].amount)
                if recipeIngredients[idx].unit == 'T':
                    targetRefri = Refrigerator.objects.get(nickname=nickname, name=recipeIngredients[idx].name)
                    print(targetRefri,"1")
                    Refrigerator.objects.filter(nickname=nickname, name=refrigerator[idx].name).update(amount=targetRefri.amount-(recipeIngredients[idx].amount*15))
                elif recipeIngredients[idx].unit == 'kg' or recipeIngredients[idx].unit == 'l':
                    targetRefri = Refrigerator.objects.get(nickname=nickname, name=recipeIngredients[idx].name)
                    print(targetRefri,"2")
                    Refrigerator.objects.filter(nickname=nickname, name=recipeIngredients[idx].name).update(amount=targetRefri.amount-(recipeIngredients[idx].amount*1000))
                else:
                    targetRefri = Refrigerator.objects.get(nickname=nickname, name=recipeIngredients[idx].name)
                    print(targetRefri,"3")
                    Refrigerator.objects.filter(nickname=nickname, name=recipeIngredients[idx].name).update(amount=targetRefri.amount-recipeIngredients[idx].amount)

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
