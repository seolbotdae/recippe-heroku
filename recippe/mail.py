from .models import *

from .serializers import *

'''
221117  쪽지함 기능 requestMailList 함수 추가 (추가된 use case)
221118  쪽지 열람, 보내기, 삭제 추가
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
            mailTarget = Mail.objects.get(mail_id = mail_id)

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
            print(mail)
            mailObject = Mail.objects.create(
                mail_id = None,
                receiver = mail['receiver'],
                title = mail['title'],
                contents = mail['contents'],
                send_time = mail['send_time'],
                sender_check = mail['sender_check'],
                receiver_check = mail['receiver_check'],
                nickname = User.objects.get(nickname = mail['nickname'])
            )
            print(mailObject)

            mailObject.save()

            result, code = self.sendResult("쪽지 추가 성공.", mailObject)
        except:
            result, code = self.sendResult("쪽지 추가 실패.", None)

        return result, code

    '''
    특정 쪽지를 삭제하는 메소드

    nickname: String
    mailId: Mail

    return -> int
    '''
    def deleteMail(self, nickname, mailId):
        try:
            mailObject = Mail.objects.get(mail_id = mailId)

            if mailObject.receiver == nickname:
                Mail.objects.update(mail_id = mailId, receiver_check = True)
            elif mailObject.nickname == nickname:
                Mail.objects.update(mail_id = mailId, sender_check = True)

            
            mailObject = Mail.objects.get(mail_id = mailId)
            if mailObject.sender_check == True and mailObject.receiver_check == True:
                mailObject.delete()
            
            
            result, code = self.sendResult("쪽지 삭제 성공.", None)
        except:
            result, code = self.sendResult("쪽지 삭제 실패.", None)
        
        return result, code
    '''
    result: int
    mail: Mail

    return void -> 바꿔야함.
    '''
    def sendResult(self, result, mail):
        if result == "쪽지 열람 실패.":
            return mail, 0
        elif result == "쪽지 열람 성공.":
            return mail, 1
        elif result == "쪽지 추가 실패.":
            return mail, 2
        elif result == "쪽지 추가 성공.":
            return mail, 3
        elif result == "쪽지 삭제 실패.":
            return mail, 4
        elif result == "쪽지 삭제 성공.":
            return mail, 5
        else:
            return mail, 6
        