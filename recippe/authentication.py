from rest_framework.generics import get_object_or_404

from django.core.mail import EmailMessage
from django.db.models import Q

from .models import *

from .serializers import *

import random

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient import errors
from email.message import EmailMessage
import base64

def gmail_authenticate():
    SCOPES = ['https://mail.google.com/']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('./token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('./credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text):
    message = EmailMessage()
    message["From"] = sender
    message["To"] = to.split(",")
    message["Subject"] = subject
    message.set_content(message_text)
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf8')}
    
def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

'''
221105 로그인 class 추가
221105 이메일인증 class 추가
221105 로그아웃 class 추가
221106 이메일인증 finishCheck 추가, 이메일전송코드 추가
221106 최종 회원가입 class 추가
221107 비밀번호 변경 class 추가
'''

class ControlLogin_b():
    def checkLogin(self, id, pw):
        try:
            dbCheck = User.objects.get(uid=id)
            serializer = UserInfoSerializer(dbCheck)
            print(serializer)

            if serializer.data['password'] == pw:
                code, serializer = self.sendResult("로그인 성공", dbCheck)
            else:
                code, serializer = self.sendResult("로그인 실패_비번", dbCheck)
        except:
            code, serializer = self.sendResult("로그인 실패_아이디", None)
        return code, serializer

    def sendResult(self, result, userInfo=None):
        if result == "로그인 성공":
            print(result, userInfo)
            return 2, userInfo
        elif result == "로그인 실패_비번":
            print(result, userInfo)
            return 0, userInfo
        elif result == "로그인 실패_아이디":
            print(result, userInfo)
            return 1, userInfo

class ControlLogout_b():
    def cancelAutoLogin(self, nickname):
        # 앞의 nickname은 db의 nickname 뒤의 nickname은 매개변수 
        dbCheck = get_object_or_404(User, nickname = nickname)
        print("첫번째 디비 체크")
        dbCheck.auto_login = 0
        dbCheck.save()

        dbCheck = get_object_or_404(User, nickname = nickname)
        print("두번쨰 디비 체크")
        if dbCheck.auto_login == 0:
            return self.sendResult("자동로그인 해제 성공")
        else:
            return self.sendResult("자동로그인 해제 실패")
        
    def sendResult(self, result):
        if result == "자동로그인 해제 성공":
            print(result)
            return 1
        elif result == "자동로그인 해제 실패":
            print(result)
            return 0

class ControlEmailVerification_b():
    def startCheck(self, request):
        code = random.randrange(100000, 1000000)
        request.POST._mutable = True
        request.data['code'] = code
        serializer = EmailVerificationSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return "이메일 등록 성공"
        else:
            return "이메일 등록 실패"
        
    def sendCode(self, email, code):
        service = gmail_authenticate()
        message = create_message("레쉽피", email, "테스트", str(code))
        result =  send_message(service, "recippesg@gmail.com", message)
        if result is not None:
            result = self.sendResult("이메일 전송 성공")
        else: result = self.sendResult("이메일 전송 실패")
        return result

    def finishCheck(self, request):
        try:
            self.codeCheck = TempEmail.objects.get(email = request.data['email'])

            if self.codeCheck.code == request.data['code']:
                result = self.sendResult("이메일 인증 최종 완료")
                self.codeCheck.delete()
                return result
            else:
                result = self.sendResult("잘못된 코드")
                return result
        except:
            result = self.sendResult("존재하지 않는 이메일 입력")
            return result
            
    def sendResult(self, result):
        if result == "이메일 전송 실패":
            print(result)
            return 0
        elif result == "이메일 전송 성공":
            print(result)
            return 1
        elif result == "존재하지 않는 이메일 입력":
            print(result)
            return 2
        elif result == "잘못된 코드":
            print(result)
            return 3
        elif result == "이메일 인증 최종 완료":
            print(result)
            return 4

class ControlSignUp_b():
    def checkOverlap(self, id, nickname):
        idCheck = User.objects.filter(uid=id)
        nickCheck = User.objects.filter(nickname=nickname)

        if len(idCheck) > 0 and len(nickCheck) == 0:
            result = self.sendResult("중복된 아이디")
        elif len(idCheck) == 0 and len(nickCheck) > 0:
            result = self.sendResult("중복된 닉네임")
        elif len(idCheck) > 0 and len(nickCheck) > 0:
            result = self.sendResult("아이디, 닉네임 모두 중복")
        elif len(idCheck) == 0 and len(nickCheck) == 0:
            result = self.sendResult("중복되지 않은 아이디, 닉네임")

        return result

    def sendResult(self, result):
        if result == "중복된 아이디":
            print(result)
            return 0
        elif result == "중복된 닉네임":
            print(result)
            return 1
        elif result == "아이디, 닉네임 모두 중복":
            print(result)
            return 2
        elif result == "중복되지 않은 아이디, 닉네임":
            print(result)
            return 3

class ControlEdittingInfo_b():
    def changePassword(self, nickname, pw):
        beforePw = User.objects.get(nickname=nickname)
        beforePw.password = pw
        beforePw.save()

        afterPw = User.objects.get(nickname=nickname)
        if afterPw.password == pw:
            result = self.sendResult("비밀번호 변경 성공")
        else:
            result = self.sendResult("비밀번호 변경 실패")
        
        return result

    def checkOverlap(self, new_nickname):
        # 나오면 있는거
        try:
            codeCheck = User.objects.get(nickname = new_nickname)
            return 1
        # 안나오면 없는거
        except:
            return 0
        
    # 닉네임 중복시 -1 원래 닉네임과 동일 할 시 0 성공시 1
    def changeNickname(self, new_nickname, id):
        # 오류
        if self.checkOverlap(new_nickname) == 1:
            result = self.sendResult("중복되는 닉네임이 있습니다.")
        # 된거
        elif self.checkOverlap(new_nickname) == 0:
            try:
                userObject = User.objects.filter(uid = id)
                old_nickname = userObject[0].nickname

                user = User.objects.create(nickname=new_nickname, uid=userObject[0].uid, password=userObject[0].password, email=userObject[0].email, auto_login=userObject[0].auto_login)
                User.save(user)

                objectList = [Comment, LikeInfo, Mail, PhotoPost, RecipePost, Refrigerator, Report]
                try:
                    object = get_object_or_404(User, nickname = old_nickname)
                    for ol in objectList:
                        olList = ol.objects.filter(nickname=old_nickname)
                        if len(olList) > 0:
                            olList.update(nickname = new_nickname)
                    User.delete(object)
                    result = self.sendResult("닉네임 변경에 성공했습니다.")
                except:
                    result = self.sendResult("닉네임 변경에 실패했습니다.")
            except: 
                result = self.sendResult("데이터베이스 오류.")
        
        return result

    #  2-> 중복, 3-> 변경 실패, 4-> 디비 오류, 5->변경 성공
    def sendResult(self, result):
        if result == "비밀번호 변경 실패":
            return 0
        elif result == "비밀번호 변경 성공":
            return 1
        elif result == "중복되는 닉네임이 있습니다.":
            return 2
        elif result == "닉네임 변경에 실패했습니다.":
            return 3
        elif result == "데이터베이스 오류.":
            return 4
        elif result == "닉네임 변경에 성공했습니다.":
            return 5
