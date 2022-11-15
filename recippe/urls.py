from django.urls import path, include

from .views import *

'''
221105 로그인 과정 위해 login/ 링크 추가, 
221107 이메일 과정 위해 fistcheck/, secondcheck/ 링크 추가, 
221105 자동로그인 해제 위해 cancelAutoLogin/ 링크 추가,
221106 최종 회원가입 위해 signup/ 링크 추가,
221107 비밀번호 변경 위해 changepw/ 링크 추가,
221109 냉장고 조회 위해 inquiryrefrigerator/ 링크 추가
221114 레시피 조회, 등록, 수정, 삭제 링크 추가
'''

urlpatterns = [
    # Authentication
    path("login/", LoginAPI.as_view()),
    path("logout/", LogoutAPI.as_view()),
    path("firstcheck/", EmailStartAPI.as_view()),
    path("secondcheck/", EmailFinalAPI.as_view()),
    path("signup/", SignUpAPI.as_view()),
    path("changepw/", ChangePwAPI.as_view()),
    path("changenickname/", ChangeNicknameAPI.as_view()),

    # RecipePost
    path("recipeboard/<int:page>/", RecipeListAPI.as_view()),
    path("recipe/<int:postId>/", RecipePostAPI.as_view()),
    path("recipeupload/", RecipePostAPI.as_view()),
    path("recipeupdate/", RecipeModifyAPI.as_view()),
    path("recipedelete/", RecipeDeleteAPI.as_view()),

    # Mypage
    path("inquiryrefrigerator/<str:nickname>/", InquiryRefrigeratorAPI.as_view()),
    path("addrefrigerator/", AddRefrigeratorAPI.as_view())
]