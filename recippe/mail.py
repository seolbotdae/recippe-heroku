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
    '''
    수신, 발신한 특정 쪽지를 가져오는 메소드

    mailId: int

    return -> Mail
    '''
    def requestMail(self, mailId):
        mail_id = mailId
        try:
            mailTarget = Mail.objects.get(mail_id = mailId)
        
            result, code = self.sendResult("쪽지 열람 성공.", mailTarget)
        except:
            result, code = self.sendResult("쪽지 열람 실패.", mailTarget)

        return result, code 
    '''
    발신한 쪽지를 등록하는 메소드

    mail: Mail

    return -> int
    '''
    def insertMail(self, mail):
        try:
            serializer = MyMailListSerializer(mail)
            serializer.is_valid()
            serializer.save()
            code, result = self.sendResult("쪽지 추가 성공.", mail)
        except:
            code, result = self.sendResult("쪽지 추가 실패.", mail)

        return result, code

    '''
    특정 쪽지를 삭제하는 메소드

    nickname: String
    mailId: Mail

    return -> int
    '''
    def deleteMail(self, nickname, mailId):
        try:
            m = Mail.objects.filter(nickname = nickname, mail_id = mailId)
            m.delete()
            result, code = self.sendResult("쪽지 삭제 성공.", None)
        except:
            result, code = self.sendResult("쪽지 삭제 실패.", None)

    '''
    result: int
    mail: Mail

    return void -> 바꿔야함.
    '''
    def sendResult(self, result, mail):
        if result == "쪽지 열람 실패.":
            return 0, mail
        elif result == "쪽지 열람 성공.":
            return 1, mail
        elif result == "쪽지 추가 실패.":
            return 2, mail
        elif result == "쪽지 추가 성공.":
            return 3, mail
        elif result == "쪽지 삭제 실패.":
            return 4, mail
        elif result == "쪽지 삭제 성공.":
            return 5, mail
        else:
            return 6, mail
        