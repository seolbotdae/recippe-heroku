from .models import *

from .serializers import *



class ControlLike_b():
    def cancelLike(self, nickname, postType, postId):
        try:
            # 좋아요 정보 가져와서 삭제
            LikeInfo.objects.filter(post_type=postType, nickname=nickname, post_id=postId).delete()
            if postType == 1: # 레시피 
                likes = LikeInfo.objects.filter(post_id=postId)
                RecipePost.objects.filter(post_id=postId).update(like_count=len(likes)) # 좋아요 수 업데이트
                resultMsg = "레시피 게시글 '좋아요' 취소 성공"
            elif postType == -1: # 사진 
                likes = LikeInfo.objects.filter(post_id=postId)
                PhotoPost.objects.filter(post_id=postId).update(like_count=len(likes)) # 좋아요 수 업데이트
                resultMsg = "사진 게시글 '좋아요' 취소 성공"
        except:
            if postType == 1:
                resultMsg = "레시피 게시글 '좋아요' 취소 실패"
            elif postType == -1:
                resultMsg = "사진 게시글 '좋아요' 취소 실패"
        
        result = self.sendResult(resultMsg)
        return result

    def pressLike(self, nickname, postType, postId):
        try:
            # 좋아요 정보 생성 후 등록
            newLike = LikeInfo.objects.create(post_type=postType, nickname=User.objects.get(nickname=nickname), post_id=postId)
            newLike.save()
            if postType == 1: # 레시피
                likes = LikeInfo.objects.filter(post_id=postId)
                RecipePost.objects.filter(post_id=postId).update(like_count=len(likes)) # 좋아요 수 업데이트
                resultMsg = "레시피 게시글 '좋아요' 등록 성공"
            elif postType == -1: # 사진
                likes = LikeInfo.objects.filter(post_id=postId)
                PhotoPost.objects.filter(post_id=postId).update(like_count=len(likes)) # 좋아요 수 업데이트
                resultMsg = "사진 게시글 '좋아요' 등록 성공"
        except:
            if postType == 1:
                resultMsg = "레시피 게시글 '좋아요' 등록 실패"
            elif postType == -1:
                resultMsg = "사진 게시글 '좋아요' 등록 실패"

        result = self.sendResult(resultMsg)
        return result

    def sendResult(self, result):
        if result == "레시피 게시글 '좋아요' 취소 실패":
            print(result)
            return 0
        elif result == "레시피 게시글 '좋아요' 취소 성공":
            print(result)
            return 1
        elif result == "레시피 게시글 '좋아요' 등록 실패":
            print(result)
            return 2
        elif result == "레시피 게시글 '좋아요' 등록 성공":
            print(result)
            return 3
        elif result == "사진 게시글 '좋아요' 취소 실패":
            print(result)
            return 4
        elif result == "사진 게시글 '좋아요' 취소 성공":
            print(result)
            return 5
        elif result == "사진 게시글 '좋아요' 등록 실패":
            print(result)
            return 6
        elif result == "사진 게시글 '좋아요' 등록 성공":
            print(result)
            return 7
