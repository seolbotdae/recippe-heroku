from django.urls import path, include

from .views import *


urlpatterns = [
    # Authentication
    path("login/", LoginAPI.as_view()),
    path("logout/", LogoutAPI.as_view()),
    path("firstcheck/", EmailStartAPI.as_view()),
    path("secondcheck/", EmailFinalAPI.as_view()),
    path("signup/", SignUpAPI.as_view()),
    path("changepw/", ChangePwAPI.as_view()),
    path("changenickname/", ChangeNicknameAPI.as_view()),

    # PhotoPost
    path("photoboard/<int:page>/", PhotoListAPI.as_view()),
    path("photo/<int:postId>/<str:nickname>/", PhotoPostAPI.as_view()),
    path("uploadphoto/", PhotoPostAPI.as_view()),
    path("deletephoto/", PhotoPostAPI.as_view()),
    path("sortphoto/", PhotoListAPI.as_view()),
    path("likephoto/", PhotoLikeAPI.as_view()),
    path("reportphoto/", PhotoReportAPI.as_view()),

    # RecipePost
    path("recipeboard/<int:page>/", RecipeListAPI.as_view()),
    path("recipe/<int:postId>/<str:nickname>/", RecipePostAPI.as_view()),
    path("uploadrecipe/", RecipePostAPI.as_view()),
    path("updaterecipe/", RecipeModifyAPI.as_view()),
    path("deleterecipe/", RecipeDeleteAPI.as_view()),
    path("likerecipe/", RecipeLikeAPI.as_view()),
    path("queryrecipe/", RecipeQueryAPI.as_view()),
    path("sortrecipe/", RecipeSortAPI.as_view()),
    path("reportrecipe/", RecipeReportAPI.as_view()),
    path("unexistingredients/<str:nickname>/<int:post_id>/", RecipeUnExistIngredientsAPI.as_view()),
    path("decreaseamount/<str:nickname>/<int:post_id>/", RecipeDecreaseAPI.as_view()),

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

    # MyLikePost
    path("inquirymylikeposts/<str:nickname>/<int:postType>/", InquiryMyLikePostsAPI.as_view()),
    path("inquirymycommentposts/<str:nickname>/", InquiryMyCommentPostsAPI.as_view()),
    
    # Comment
    path("addcomment/", InsertCommentAPI.as_view()),
    path("updatecomment/", UpdateCommentAPI.as_view()),
    path("deletecomment/", DeleteCommentAPI.as_view()),
    path("reportcomment/", ReportCommentAPI.as_view()),

    # Mail
    path("inquiremaillist/<str:nickname>/<int:page>/", MailBoxAPI.as_view()),
    path("inquiremail/<int:mail_id>/", InquiryMailAPI.as_view()),
    path("insertmail/", InsertMailAPI.as_view()),
    path("deletemail/", DeleteMailAPI.as_view()),
]