from .models import *

from .serializers import *

import math

class ControlPhotoList_b():
    def requestPhotoList(self, page):
        try:
            # 사진 게시판 최근 순으로 조회
            posts = PhotoPost.objects.order_by('upload_time').reverse()
            postlist = posts[0+15*(page-1):15+15*(page-1)] # 1페이지당 20개
            result, photoList = self.sendResult("사진 게시판 조회 성공", postlist)
            pageCnt = math.ceil(len(posts)/15)
        except:
            result, photoList = self.sendResult("사진 게시판 조회 실패", None)
            pageCnt = 0

        return result, photoList, pageCnt

    def arrangePhotoList(self, arrangeBy, page):
        # 정렬 기준에 따라 다른 처리
        if arrangeBy == "최근 순":
            try:
                posts = PhotoPost.objects.filter().order_by('upload_time').reverse()
                postlist = posts[0+15*(page-1):15+15*(page-1)]
                result, photoList = self.sendResult("사진 게시글 정렬 성공", postlist)
                pageCnt = math.ceil(len(posts)/15)
            except:
                result, photoList = self.sendResult("사진 게시글 정렬 실패", None)
        elif arrangeBy == "좋아요 순":
            try:
                posts = PhotoPost.objects.filter().order_by('like_count').reverse()
                postlist = posts[0+15*(page-1):15+15*(page-1)]
                result, photoList = self.sendResult("사진 게시글 정렬 성공", postlist)
                pageCnt = math.ceil(len(posts)/15)
            except:
                result, photoList = self.sendResult("사진 게시글 정렬 실패", None)

        return result, photoList, pageCnt

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
            # postId 에 맞는 게시글과, 사용자가 좋아요를 누른 게시글인지 확인
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
        # 사진 게시글 정보 생성 후 저장
        photo = MyPhotoPostSerializer(data=newPhoto)
        if photo.is_valid():
            photo.save()
            result, newPhoto = self.sendResult("사진 게시글 등록 성공", photo) 
        else:
            result, newPhoto = self.sendResult("사진 게시글 등록 실패", None)
        
        return result, newPhoto

    def deletePhoto(self, nickname, postId):
        # 사용자의 게시글 중에서 postId 에 해당하는 게시글 삭제
        # 이때 게시글과 관련된 좋아요와 신고 정보도 같이 삭제
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