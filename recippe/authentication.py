from rest_framework.generics import get_object_or_404
from django.core.mail import EmailMessage
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

# Gmail API 를 이용한 메일보내기
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



        

class ControlLogin_b():
    def checkLogin(self, id, pw):
        try:
            # DB 에서 id 로 등록된 유저 있는지 확인
            dbCheck = User.objects.get(uid=id)
            serializer = UserInfoSerializer(dbCheck)
            print("Userinfo : ", serializer)

            # 가져온 데이터의 pw 가 입력한 pw 와 같은지 확인
            if serializer.data['password'] == pw:
                code, serializer = self.sendResult("로그인 성공", dbCheck)
            else:
                code, serializer = self.sendResult("잘못된 비밀번호", None)
        except:
            # DB 에 id 로 등록된 유저 없음
            code, serializer = self.sendResult("존재하지 않는 아이디", None)
            
        return code, serializer

    def sendResult(self, result, userInfo=None):
        if result == "잘못된 비밀번호":
            print(result, userInfo)
            return 0, userInfo
        elif result == "존재하지 않는 아이디":
            print(result, userInfo)
            return 1, userInfo
        elif result == "로그인 성공":
            print(result, userInfo)
            return 2, userInfo

class ControlLogout_b():
    def cancelAutoLogin(self, nickname):
        # 입력된 nickname 을 닉네임으로 갖는 유저 정보 DB 에서 가져옴 
        dbCheck = get_object_or_404(User, nickname = nickname)
        print("자동로그인 해제")
        dbCheck.auto_login = 0 # 유저의 자동로그인 해제
        dbCheck.save()

        # 제대로 해제되었는지 확인
        dbCheck = get_object_or_404(User, nickname = nickname)
        print("해제 체크")
        if dbCheck.auto_login == 0:
            return self.sendResult("로그아웃 성공")
        else:
            return self.sendResult("로그아웃 실패")
        
    def sendResult(self, result):
        if result == "로그아웃 실패":
            print(result)
            return 0
        elif result == "로그아웃 성공":
            print(result)
            return 1

class ControlEmailVerification_b():
    def startCheck(self, request):
        # 6자리 난수 생성
        code = random.randrange(100000, 1000000)
        request['code'] = code
        print(request['code'])

        # 임시로 이메일과 난수코드 저장
        # 저장 전 이미 기존에 이메일 전송을 요청한 적이 있는지 확인
        tempEmail = TempEmail.objects.filter(email=request['email'])
        if len(tempEmail) == 0:
            # 요청한적 없다면 저장
            tempEmail = TempEmail.objects.create(email = request['email'], code = request['code'])
            TempEmail.save(tempEmail)
        else:
            # 요청한적 있다면 난수코드만 업데이트
            tempEmail.update(code=request['code'])

        # 제대로 저장됐는지 확인   
        if TempEmail.objects.get(email = request['email']).email == request['email']:
            return "이메일 등록 성공"
        else:
            return "이메일 등록 실패"
        
    def sendCode(self, email, code):
        # Gamil API 를 이용한 이메일 발송
        service = gmail_authenticate()
        message = create_message("레쉽피", email, "테스트", str(code))
        result =  send_message(service, "recippesg@gmail.com", message)
        if result is not None:
            result = self.sendResult("이메일 전송 성공")
        else: result = self.sendResult("이메일 전송 실패")
        return result

    def finishCheck(self, request):
        try:
            print(request['email'])
            # DB 에 저장했던 이메일과 난수코드 가져옴
            codeCheck = TempEmail.objects.get(email = request['email'])

            # 유저가 입력한 코드와 비교
            if codeCheck.code == request['code']:
                code = self.sendResult("이메일 인증 최종 완료")
                codeCheck.delete()

                deleteCheck = TempEmail.objects.filter(email=request['email'])
                if len(deleteCheck) > 0:
                    code = self.sendResult("알 수 없는 오류")
                return code
            else:
                code = self.sendResult("잘못된 코드")
                return code
        except:
            code = self.sendResult("존재하지 않는 이메일 입력")
            return code
            
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
        else:
            print("알 수 없는 오류")
            return 6

class ControlSignUp_b():
    def checkOverlap(self, id, nickname):
        # 입력된 아이디, 닉네임 별로 DB 에 저장되어있는 데이터 수집
        idCheck = User.objects.filter(uid=id)
        nickCheck = User.objects.filter(nickname=nickname)
        
        # 수집된 데이터의 크기에 따라 중복 확인
        if len(idCheck) > 0:
            if len(nickCheck) > 0: code = self.sendResult("아이디, 닉네임 모두 중복")
            else: code = self.sendResult("중복된 아이디")
        elif len(nickCheck) > 0:
            code = self.sendResult("중복된 닉네임")
        else:
            code = self.sendResult("중복되지 않은 아이디, 닉네임")

        return code

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
        # 기존 유저 정보 들고와서 비밀번호 변경 후 저장
        beforePw = User.objects.get(nickname=nickname)
        beforePw.password = pw
        beforePw.save()

        # 제대로 저장됐는지 확인
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
        
    def changeNickname(self, new_nickname, id):
        # 중복된 닉네임
        if self.checkOverlap(new_nickname) == 1:
            result = self.sendResult("중복되는 닉네임이 있습니다.")
        # 중복되지 않음
        elif self.checkOverlap(new_nickname) == 0:
            try:
                # 변경된 닉네임 저장
                userObject = User.objects.filter(uid = id)
                old_nickname = userObject[0].nickname

                user = User.objects.create(nickname=new_nickname, uid=userObject[0].uid, password=userObject[0].password, email=userObject[0].email, auto_login=userObject[0].auto_login)
                User.save(user)

                # 기존의 닉네임을 사용하던 기존의 데이터들도 모두 변경
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