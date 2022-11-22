from .models import *

from .serializers import *

'''
221117  사진 게시판 class 추가
        사진 게시글 조회 추가
        사진 게시글 등록 추가
        사진 게시글 삭제, 좋아요, 정렬, 신고 추가
'''

class ControlPhotoList_b():
    def requestPhotoList(self, page):
        try:
            posts = PhotoPost.objects.order_by('upload_time').reverse()
            postlist = posts[0+20*(page-1):20+20*(page-1)]
            result, photoList = self.sendResult("사진 게시판 조회 성공", postlist)
            pageCnt = int(len(posts)/20) + 1
        except:
            result, photoList = self.sendResult("사진 게시판 조회 실패", None)
            pageCnt = 0

        return result, photoList, pageCnt

    def arrangePhotoList(self, arrangeBy, page):
        if arrangeBy == "최근 순":
            try:
                posts = PhotoPost.objects.filter().order_by('upload_time').reverse()
                postlist = posts[0+20*(page-1):20+20*(page-1)]
                result, photoList = self.sendResult("사진 게시글 정렬 성공", postlist)
            except:
                result, photoList = self.sendResult("사진 게시글 정렬 실패", None)
        elif arrangeBy == "좋아요 순":
            try:
                posts = PhotoPost.objects.filter().order_by('like_count').reverse()
                postlist = posts[0+20*(page-1):20+20*(page-1)]
                result, photoList = self.sendResult("사진 게시글 정렬 성공", postlist)
            except:
                result, photoList = self.sendResult("사진 게시글 정렬 실패", None)

        return result, photoList

    def sendResult(self, result, photoList=None):
        if result == "사진 게시판 조회 실패":
            print(f"{result}, {0}")
            return 0, photoList
        elif result == "사진 게시판 조회 성공":
            print(f"{result}, {len(photoList)}")
            return 1, photoList
        elif result == "사진 게시글 정렬 실패":
            print(f"{result}, {0}")
            return 2, photoList
        elif result == "사진 게시글 정렬 성공":
            print(f"{result}, {len(photoList)}")
            return 3, photoList

class ControlPhoto_b():
    def requestPhoto(self, postId, nickname):
        try:
            post = PhotoPost.objects.get(post_id = postId)
            serializer = MyPhotoPostSerializer(post)
            result, photoPost = self.sendResult("사진 게시글 조회 성공", serializer.data)
            isLiked = LikeInfo.objects.filter(post_id = postId, nickname = nickname, post_type=-1)
            print(isLiked)
            if len(isLiked) == 0:
                likeInfo = False
            else: likeInfo = True
        except:
            result, photoPost = self.sendResult("사진 게시글 조회 실패", None)
            likeInfo = False

        return result, photoPost, likeInfo

    def insertPhoto(self, newPhoto):
        photo = MyPhotoPostSerializer(data=newPhoto)
        if photo.is_valid():
            photo.save()
            result, newPhoto = self.sendResult("사진 게시글 등록 성공", photo) 
        else:
            result, newPhoto = self.sendResult("사진 게시글 등록 실패", None)
        
        return result, newPhoto

    def deletePhoto(self, nickname, postId):
        try:
            deleteTarget = PhotoPost.objects.get(nickname=nickname, post_id=postId)
            deleteTarget.delete()
            likeInfos = LikeInfo.objects.filter(post_id=postId, post_type=-1)
            likeInfos.delete()
            reports = Report.objects.filter(post_id=postId, post_type=2)
            reports.delete()

            result = self.sendResult("사진 게시글 삭제 성공")
        except:
            result = self.sendResult("사진 게시글 삭제 실패")

        return result

    def sendResult(self, result, photoPost=None):
        if result == "사진 게시글 조회 실패":
            print(f"{result}, {0}")
            return 0, photoPost
        elif result == "사진 게시글 조회 성공":
            print(f"{result}, {len(photoPost)}")
            return 1, photoPost
        elif result == "사진 게시글 등록 실패":
            print(f"{result}, {0}")
            return 2, photoPost
        elif result == "사진 게시글 등록 성공":
            print(f"{result}, {photoPost}")
            return 3, photoPost
        elif result == "사진 게시글 삭제 실패":
            print(f"{result}, {0}")
            return 4
        elif result == "사진 게시글 삭제 성공":
            print(f"{result}, {0}")
            return 5
