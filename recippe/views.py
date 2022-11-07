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
'''

class LoginAPI(APIView):
    def post(self, request, format=None):
        print(request.data['uid'])

        inputId = request.data['uid']
        inputPw = request.data['password']

        controlLogin = ControlLogin_b()
        serializer = controlLogin.checkLogin(inputId, inputPw)

        if serializer == 0:
            return Response(0, status=status.HTTP_404_NOT_FOUND)
        elif serializer == 1:
            serializer = UserInfoSerializer(request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(2, status=status.HTTP_406_NOT_ACCEPTABLE)

class LogoutAPI(APIView):
    def post(self, request):
        print(f"CancleAutoLogin Class start")

        inputNickname = request.data['nickname']

        controlLogout = ControlLogout_b()
        result = controlLogout.cancelAutoLogin(inputNickname)

        if result == 1:
            return Response(result, status=status.HTTP_200_OK)
        elif result == 0:
            return Response(result,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return Response(2, status=status.HTTP_406_NOT_ACCEPTABLE)
            
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
                return Response(sendRes, status=status.HTTP_400_BAD_REQUEST)
        elif uploadRes == "이메일 등록 실패":
            return Response(5, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(6, status=status.HTTP_406_NOT_ACCEPTABLE)

class EmailFinalAPI(APIView):
    def post(self, request):
        print(f"email = {request.data['email']}, code = {request.data['code']}")

        emailVerification = ControlEmailVerification_b()
        checkRes = emailVerification.finishCheck(request)

        if checkRes == 2:
            return Response(checkRes, status=status.HTTP_400_BAD_REQUEST)
        elif checkRes == 3:
            return Response(checkRes, status=status.HTTP_400_BAD_REQUEST)
        elif checkRes == 4:
            return Response(checkRes, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_406_NOT_ACCEPTABLE)

class SignUpAPI(APIView):
    def post(self, request):
        print(request.data)

        signUp = ControlSignUp_b()
        overlapRes = signUp.checkOverlap(request.data['uid'], request.data['nickname'])

        if overlapRes == 0:
            return Response(0, status=status.HTTP_400_BAD_REQUEST)
        elif overlapRes == 1:
            return Response(1, status=status.HTTP_400_BAD_REQUEST)
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
            return Response(5, status=status.HTTP_406_NOT_ACCEPTABLE)

class ChangePwAPI(APIView):
    def post(self, request):
        print(request.data)

        changePw = ControlEdittingInfo_b()
        changePwRes = changePw.changePassword(request.data['nickname'], request.data['password'])

        if changePwRes == 0:
            return Response(0, status=status.HTTP_400_BAD_REQUEST)
        elif changePwRes == 1:
            return Response(1, status=status.HTTP_200_OK)
        else:
            return Response(2, status=status.HTTP_406_NOT_ACCEPTABLE)

