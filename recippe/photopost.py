from .models import *

from .serializers import *

'''
221117  사진 게시판 class 추가
        사진 게시글 조회 추가
        사진 게시글 등록 추가
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
            post = PhotoPost.objects.get(post_id = postId)
            serializer = MyPhotoPostSerializer(post)
            result, photoPost = self.sendResult("사진 게시글 조회 성공", serializer.data)
        except:
            result, photoPost = self.sendResult("사진 게시글 조회 실패", None)

        return result, photoPost

    def insertPhoto(self, newPhoto):
        photo = MyPhotoPostSerializer(newPhoto)
        print(photo)

        try:
            photo.save()
            result, newPhoto = self.sendResult("사진 게시글 등록 성공", photo) 
        except:
            result, newPhoto = self.sendResult("사진 게시글 등록 실패", None)
        
        return result, newPhoto

    def deletePhoto(self, nickname, postId):
        pass

    def sendResult(self, result, photoPost=None):
        if result == "사진 게시글 조회 실패":
            print(f"{result}, {0}")
            return 0, photoPost
        elif result == "사진 게시글 조회 성공":
            print(f"{result}, {len(photoPost)}")
            return 1, photoPost
        elif result == "사진 게시글 등록 실패":
            print(f"{result}, {len(photoPost)}")
            return 2, photoPost
        elif result == "사진 게시글 등록 성공":
            print(f"{result}, {len(photoPost)}")
            return 3, photoPost
