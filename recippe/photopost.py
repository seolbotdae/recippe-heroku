from .models import *

from .serializers import *

'''
221117  사진 게시판 class 추가
'''

class ControlPhotoList_b():
    def requestPhotoList(self, page):
        try:
            posts = PhotoPost.objects.order_by('upload_time').reverse()
            postlist = posts[0+20*(page-1):20+20*(page-1)]
            result, photoList = self.sendResult("사진 게시판 조회 성공", postlist)
            result = result + int(len(posts)/20)
        except:
            result, photoList = self.sendResult("사진 게시판 조회 실패", None)

        return result, photoList

    def arrangePhotoList(self, arrangeBy, page):
        pass

    def sendResult(self, result, photoList=None):
        if result == "사진 게시판 조회 실패":
            print(f"{result}, {0}")
            return 0, photoList
        elif result == "사진 게시판 조회 성공":
            print(f"{result}, {len(photoList)}")
            return 1, photoList

class ControlPhoto_b():
    def requestPhoto(self, postId):
        try:
            post = PhotoPost.objects.filter(post_id = postId)
            print(post)
            result, photoPost = self.sendResult("사진 게시글 조회 성공", post)
            print(result, photoPost)
        except:
            result, photoPost = self.sendResult("사진 게시글 조회 실패", None)

        return result, photoPost

    def insertPhoto(self, newPhoto):
        pass

    def deletePhoto(self, nickname, postId):
        pass

    def sendResult(self, result, photoPost=None):
        if result == "사진 게시글 조회 실패":
            print(f"{result}, {0}")
            return 0, photoPost
        elif result == "사진 게시글 조회 성공":
            print(f"{result}, {len(photoPost)}")
            return 1, photoPost