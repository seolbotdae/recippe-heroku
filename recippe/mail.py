from .models import *

from .serializers import *

'''
221117  쪽지함 기능 requestMailList 함수 추가 (추가된 use case)
'''

class ControlMailList_b():
    '''
    수신, 발신한 쪽지들을 가져오는 메소드

    page:int ->page:int, nickname:String 으로 바뀌어야 함.

    return type List<Mail>, count:int, 
    '''
    def requestMailList(self, page, nickname):
        print("내부 함수 : requestMailList Start")
        try:
            mails = Mail.objects.filter(nickname = nickname, sender_check = False) | Mail.objects.filter(receiver = nickname, receiver_check = False)
            mailList = mails[0+20*(page-1):20+20*(page-1)]
            result, mailList = self.sendResult("메일 조회 성공.", mailList)
            pageCnt = int(len(mails)/20) + 1
            print("내부 함수 : 메일 조회 성공")
        except:
            result, mailList = self.sendResult("메일 조회 실패.", None)
            pageCnt = 0
            print("내부 함수 : 메일 조회 실패")

        return result, mailList, pageCnt

    '''
    sendResult

    result:int
    mailList:List<Mail>

    return type void -> 바꿔야함
    '''
    def sendResult(self, result, mailList):
        if result == "메일 조회 실패.":
            print("sendResult : 메일 조회 실패")
            return 0, mailList
        elif result == "메일 조회 성공.":
            print("sendResult : 메일 조회 성공")
            return 1, mailList
        else:
            print("sendResult : 알 수 없는 오류")
            return 2, mailList
        

class ControlMail_b():
    pass