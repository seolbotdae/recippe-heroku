from django.urls import path, include

from .views import *

'''
221105 로그인 과정 위해 login/ 링크 추가, 
221107 이메일 과정 위해 fistcheck/, secondcheck/ 링크 추가, 
221105 자동로그인 해제 위해 cancelAutoLogin/ 링크 추가,
221106 최종 회원가입 위해 signup/ 링크 추가,
221107 비밀번호 변경 위해 changepw/ 링크 추가,
'''

urlpatterns = [
    path("login/", LoginAPI.as_view()),
    path("logout/", LogoutAPI.as_view()),
    path("firstcheck/", EmailStartAPI.as_view()),
    path("secondcheck/", EmailFinalAPI.as_view()),
    path("signup/", SignUpAPI.as_view()),
    path("changepw/", ChangePwAPI.as_view()),
    path("changenickname/", ChangeNicknameAPI.as_view()),
]