from .models import *

from .serializers import *


class ControlReport_b():
    def reportPost(self, reportInfo):
        try:
            # 게시글 신고 정보 생성 후 저장
            report = Report.objects.create(nickname=User.objects.get(nickname=reportInfo['reporter']), contents=reportInfo['contents'], 
                                            post_type=reportInfo['post_type'], post_id=reportInfo['post_id'])
            report.save()
            result = self.sendResult("게시글 신고 성공")
        except:
            result = self.sendResult("게시글 신고 실패")

        return result

    def reportComment(self, reportInfo):
        try:
            # 댓글 신고 정보 생성 후 저장
            report = Report.objects.create(nickname=User.objects.get(nickname=reportInfo['reporter']), contents=reportInfo['contents'], 
                                            post_type=reportInfo['post_type'], post_id=reportInfo['post_id'])
            report.save()
            result = self.sendResult("댓글 신고 성공")
        except:
            result = self.sendResult("댓글 신고 실패")

        return result
    
    def sendResult(self, result):
        if result == "게시글 신고 실패":
            print(result)
            return 0
        elif result == "게시글 신고 성공":
            print(result)
            return 1
        elif result == "댓글 신고 실패":
            print(result)
            return 2
        elif result == "댓글 신고 성공":
            print(result)
            return 3
