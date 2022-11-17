from .models import *

from .serializers import *

'''
221116  레시피 게시글 신고 추가
221117  레시피 게시판 댓글 신고 추가 
'''

class ControlReport_b():
    def reportPost(self, reportInfo):
        try:
            report = Report.objects.create(nickname=User.objects.get(nickname=reportInfo['reporter']), contents=reportInfo['contents'], 
                                            post_type=reportInfo['post_type'], post_id=reportInfo['post_id'])
            report.save()
            result = self.sendResult("게시글 신고 성공")
        except:
            result = self.sendResult("게시글 신고 실패")

        return result

    def reportComment(self, reportInfo):
        print("내부 함수 : reportComment start")
        try:
            report = Report.objects.create(nickname=User.objects.get(nickname=reportInfo['reporter']), contents=reportInfo['contents'], 
                                            post_type=reportInfo['post_type'], post_id=reportInfo['post_id'])
            report.save()
            result = self.sendResult("댓글 신고 성공.")
            print("내부 함수 : 댓글 신고 성공")
        except:
            result = self.sendResult("댓글 신고 실패.")
            print("내부 함수 : 댓글 신고 실패")

        return result
    
    def sendResult(self, result):
        if result == "게시글 신고 실패":
            print(result)
            return 0
        elif result == "게시글 신고 성공":
            print(result)
            return 1
        elif result == "댓글 신고 실패.":
            print("sendResult : 댓글 신고 실패")
            return 2
        elif result == "댓글 신고 성공.":
            print("sendResult : 댓글 신고 성공")
            return 3
