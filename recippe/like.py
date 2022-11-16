from .models import *

from .serializers import *

'''
221116  레시피 게시글 좋아요 함수 추가
'''

class ControlLike_b():
    def cancelLike(self, nickname, postType, postId):
        try:
            LikeInfo.objects.filter(post_type=postType, nickname=nickname, post_id=postId).delete()
            result = self.sendResult("레시피 게시글 '좋아요' 취소 성공")
        except:
            result = self.sendResult("레시피 게시글 '좋아요' 취소 실패")
        
        return result

    def pressLike(self, nickname, postType, postId):
        try:
            newLike = LikeInfo.objects.create(post_type=postType, nickname=User.objects.get(nickname=nickname), post_id=postId)
            newLike.save()
            result = self.sendResult("레시피 게시글 '좋아요' 등록 성공")
        except:
            result = self.sendResult("레시피 게시글 '좋아요' 등록 실패")

        return result

    def sendResult(self, result):
        if result == "레시피 게시글 '좋아요' 취소 실패":
            print(result)
            return 0
        if result == "레시피 게시글 '좋아요' 취소 성공":
            print(result)
            return 1
        if result == "레시피 게시글 '좋아요' 등록 실패":
            print(result)
            return 2
        if result == "레시피 게시글 '좋아요' 등록 성공":
            print(result)
            return 3
