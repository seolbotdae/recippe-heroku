from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

from .models import User

from .serializers import *

from .authentication import *
from .mypage import *

# Create your views here.

'''
221105 로그인 view 추가
221105 이메일 view 추가
221105 자동로그인 해제 view 추가
221106 이메일 인증 get 함수 추가
221106 최종 회원가입 view 추가
221107 비밀번호 변경 view 추가
221107 냉장고 조회 view 추가
221108 닉네임 변경 view 추가 (작업중)
'''

class LoginAPI(APIView):
    def post(self, request):
        #print("type", type(request))
        #print(request.GET.get('uid'))
        #print(request.data['uid'])
        #upload

        inputId = request.data['uid']
        inputPw = request.data['password']
        #inputId = request.GET.get('uid')
        #inputPw = request.GET.get('password')

        controlLogin = ControlLogin_b()
        code, serializer = controlLogin.checkLogin(inputId, inputPw)

        if code == 0:
            return Response(0, status=status.HTTP_400_BAD_REQUEST)
        elif code == 1:
            return Response(1, status=status.HTTP_400_BAD_REQUEST)
        elif code == 2:
            serializer = UserInfoSerializer(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(3, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutAPI(APIView):
    def post(self, request):
        print(f"CancleAutoLogin Class start")

        inputNickname = request.data['nickname']

        controlLogout = ControlLogout_b()
        result = controlLogout.cancelAutoLogin(inputNickname)

        if result == 1:
            return Response(result, status=status.HTTP_200_OK)
        elif result == 0:
            return Response(result,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(2, status=status.HTTP_502_BAD_GATEWAY)
            
class EmailStartAPI(APIView):
    def post(self, request):
        print(request.data['email'])

        emailVerification = ControlEmailVerification_b()
        uploadRes = emailVerification.startCheck(request)

        if uploadRes == "이메일 등록 성공":
            sendRes = emailVerification.sendCode(request.data['email'], request.data['code'])
            if sendRes == 1:
                return Response(sendRes, status=status.HTTP_200_OK)
            elif sendRes == 0:
                return Response(sendRes, status=status.HTTP_501_NOT_IMPLEMENTED)
        elif uploadRes == "이메일 등록 실패":
            return Response(5, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(6, status=status.HTTP_502_BAD_GATEWAY)

class EmailFinalAPI(APIView):
    def post(self, request):
        print(f"email = {request.data['email']}, code = {request.data['code']}")

        emailVerification = ControlEmailVerification_b()
        checkRes = emailVerification.finishCheck(request)

        if checkRes == 2:
            return Response(checkRes, status=status.HTTP_404_NOT_FOUND)
        elif checkRes == 3:
            return Response(checkRes, status=status.HTTP_400_BAD_REQUEST)
        elif checkRes == 4:
            return Response(checkRes, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_502_BAD_GATEWAY)

class SignUpAPI(APIView):
    def post(self, request):
        print(request.data)

        signUp = ControlSignUp_b()
        overlapRes = signUp.checkOverlap(request.data['uid'], request.data['nickname'])

        if overlapRes == 0:
            return Response(0, status=status.HTTP_400_BAD_REQUEST)
        elif overlapRes == 1:
            return Response(1, status=status.HTTP_401_UNAUTHORIZED)
        elif overlapRes == 2:
            return Response(2, status=status.HTTP_400_BAD_REQUEST)
        elif overlapRes == 3:
            serializer = UserInfoSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(4, status=status.HTTP_200_OK)
            else:
                return Response(3, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(5, status=status.HTTP_502_BAD_GATEWAY)

class ChangePwAPI(APIView):
    def post(self, request):
        print(request.data)

        changePw = ControlEdittingInfo_b()
        changePwRes = changePw.changePassword(request.data['nickname'], request.data['password'])

        if changePwRes == 0:
            return Response(0, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif changePwRes == 1:
            return Response(1, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_502_BAD_GATEWAY)

#  2-> 중복, 3-> 변경 실패, 4-> 디비 오류, 5->변경 성공, 6->알수 없음
class ChangeNicknameAPI(APIView):
    def post(self, request):
        print(request.data)

        nicknameEdit = ControlEdittingInfo_b()
        changeResult = nicknameEdit.changeNickname(request.data['nickname'], request.data['uid'])
        
        if changeResult == 2:
            return Response(2, status=status.HTTP_400_BAD_REQUEST)
        elif changeResult == 3:
            return Response(3, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif changeResult == 4:
            return Response(4, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif changeResult == 5:
            return Response(5, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_502_BAD_GATEWAY)