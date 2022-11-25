from .models import *

from .serializers import *



class ControlMailList_b():
    def requestMailList(self, page, nickname):
        # 요청받은 닉네임이 보내거나 받은 메일을 해당 페이지에 맞게 조회
        try:
            # 발신자이면서 지운적없거나 수신자이면서 지운적없거나 (_check => 지웠다면 True)
            mails = Mail.objects.filter(nickname = nickname, sender_check = False) | Mail.objects.filter(receiver = nickname, receiver_check = False)
            mailList = mails[0+15*(page-1):15+15*(page-1)]
            result, mailList = self.sendResult("메일 조회 성공", mailList)
            pageCnt = int(len(mails)/15) + 1
        except:
            result, mailList = self.sendResult("메일 조회 실패", None)
            pageCnt = 0

        return result, mailList, pageCnt

    def sendResult(self, result, mailList):
        if result == "메일 조회 실패":
            print(result)
            return 0, mailList
        elif result == "메일 조회 성공":
            print(result)
            return 1, mailList
        else:
            print(result)
            return 2, mailList
        
class ControlMail_b():
    def requestMail(self, mailId):
        # 요청받은 Id 에 해당하는 쪽지 조회
        mail_id = mailId
        try:
            mailTarget = Mail.objects.get(mail_id = mail_id)

            result, code = self.sendResult("쪽지 열람 성공", mailTarget)
        except:
            result, code = self.sendResult("쪽지 열람 실패", mailTarget)

        return result, code 

    def insertMail(self, mail):
        try:
            # 쪽지 정보를 생성 후 저장
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

            result, code = self.sendResult("쪽지 추가 성공", mailObject)
        except:
            result, code = self.sendResult("쪽지 추가 실패", None)

        return result, code

    def deleteMail(self, nickname, mailId):
        print(mailId)
        # 요청받은 mailId 에 맞는 메일을 삭제
        # 이때 수신자 또는 발신자에 맞는 _check 데이터를 True 로 변경
        # 둘 다 True 가 되었다면 데이터 완전 삭제
        try:
            mailObject = Mail.objects.filter(mail_id = mailId)
            deleteTarget = mailObject[0]

            if deleteTarget.receiver == nickname:
                deleteTarget.receiver_check = True
                deleteTarget.save()
            elif deleteTarget.nickname == User.objects.get(nickname=nickname):
                deleteTarget.sender_check = True
                deleteTarget.save()

            # 둘 다 True 인지 확인
            mailObject = Mail.objects.get(mail_id = mailId)
            if mailObject.sender_check == True and mailObject.receiver_check == True:
                mailObject.delete()
            
            
            result, code = self.sendResult("쪽지 삭제 성공", None)
        except:
            result, code = self.sendResult("쪽지 삭제 실패", None)
        
        return result, code

    def sendResult(self, result, mail):
        if result == "쪽지 열람 실패":
            return mail, 0
        elif result == "쪽지 열람 성공":
            return mail, 1
        elif result == "쪽지 추가 실패":
            return mail, 2
        elif result == "쪽지 추가 성공":
            return mail, 3
        elif result == "쪽지 삭제 실패":
            return mail, 4
        elif result == "쪽지 삭제 성공":
            return mail, 5
        