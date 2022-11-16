from django.urls import path, include

from .views import *

'''
221105  로그인 과정 위해 login/ 링크 추가, 
221107  이메일 과정 위해 fistcheck/, secondcheck/ 링크 추가, 
221105  자동로그인 해제 위해 cancelAutoLogin/ 링크 추가,
221106  최종 회원가입 위해 signup/ 링크 추가,
221107  비밀번호 변경 위해 changepw/ 링크 추가,
221109  냉장고 조회 위해 inquiryrefrigerator/ 링크 추가
221114  레시피 조회, 등록, 수정, 삭제 링크 추가
221115  냉장고 재료 삭제 링크 추가
        냉장고 재료 변경 링크 추가
        사용자 작성 사진 게시글 조회 링크 추가
221116  사용자 레시피 게시글 조회 링크 추가
        사용자 레시피 게시글 검색 링크 추가
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
    path("uploadrecipe/", RecipePostAPI.as_view()),
    path("updaterecipe/", RecipeModifyAPI.as_view()),
    path("deleterecipe/", RecipeDeleteAPI.as_view()),

    # Mypage
    path("inquiryrefrigerator/<str:nickname>/", InquiryRefrigeratorAPI.as_view()),
    path("addrefrigerator/", AddRefrigeratorAPI.as_view()),
    path("deleterefrigerator/", DeleteRefrigeratorAPI.as_view()),
    path("updaterefrigerator/", UpdateRefrigeratorAPI.as_view()),

    # MyPhotoPost
    path("inquirymyphotoposts/<str:nickname>/", InquiryMyPhotoPostsAPI.as_view()),

    # MyRecipePost
    path("inquirymyrecipeposts/<str:nickname>/", InquiryMyRecipePostsAPI.as_view()),
    path("querymyrecipeposts/", QueryMyRecipePostsAPI.as_view()),
    path("arrangemyrecipeposts/", ArrangeMyRecipePostsAPI.as_view()),
]