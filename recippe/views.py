from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *
from .authentication import *
from .mypage import *
from .recipepost import *
from .report import *
from .ingredients import *
from .like import *
from .mail import *
from .photopost import *
from .mail import *

# json 파싱을 위한 header
import json



'''
Authentication
'''
class LoginAPI(APIView):
    def post(self, request):
        print(f"LoginAPI Start")
        data = json.loads(request.body)
        
        inputId = data['uid']
        inputPw = data['password']

        # 로그인 시작
        controlLogin = ControlLogin_b()
        code, serializer = controlLogin.checkLogin(inputId, inputPw)

        # 결과 반환
        if code == 0:
            return Response(code, status=status.HTTP_400_BAD_REQUEST)
        elif code == 1:
            return Response(code, status=status.HTTP_400_BAD_REQUEST)
        elif code == 2:
            serializer = UserInfoSerializer(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(3, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutAPI(APIView):
    def post(self, request):
        print(f"LogoutAPI Start")
        data = json.loads(request.body)

        print(f"Cancel AutoLogin start")
        inputNickname = data['nickname']

        # 로그아웃 시작
        controlLogout = ControlLogout_b()
        code = controlLogout.cancelAutoLogin(inputNickname)

        # 결과 반환
        if code == 0:
            return Response(code, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif code == 1:
            return Response(code, status=status.HTTP_200_OK)
        else:
            return Response(2, status=status.HTTP_502_BAD_GATEWAY)
            
class EmailStartAPI(APIView):
    def post(self, request):
        print(f"EmailStartAPI Start")
        data = json.loads(request.body)

        print(data['email'])

        # 이메일 인증 시작
        emailVerification = ControlEmailVerification_b()
        uploadRes = emailVerification.startCheck(data)

        # 결과 반환
        if uploadRes == "이메일 등록 성공":
            sendRes = emailVerification.sendCode(data['email'], data['code'])
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
        print(f"EmailFinalAPI Start")
        data = json.loads(request.body)
        print(f"email = {data['email']}, code = {data['code']}")

        # 이메일 인증 마무리 시작
        emailVerification = ControlEmailVerification_b()
        checkRes = emailVerification.finishCheck(data)

        # 결과 반환
        if checkRes == 2:
            return Response(checkRes, status=status.HTTP_404_NOT_FOUND)
        elif checkRes == 3:
            return Response(checkRes, status=status.HTTP_400_BAD_REQUEST)
        elif checkRes == 4:
            return Response(checkRes, status=status.HTTP_200_OK)
        else:
            return Response(checkRes, status=status.HTTP_502_BAD_GATEWAY)

class SignUpAPI(APIView):
    def post(self, request):
        print(f"SignUpAPI Start")
        request = json.loads(request.body)

        # 회원가입 시작
        signUp = ControlSignUp_b()
        overlapRes = signUp.checkOverlap(request['uid'], request['nickname'])

        # 결과 반환
        if overlapRes == 0:
            return Response(overlapRes, status=status.HTTP_400_BAD_REQUEST)
        elif overlapRes == 1:
            return Response(overlapRes, status=status.HTTP_401_UNAUTHORIZED)
        elif overlapRes == 2:
            return Response(overlapRes, status=status.HTTP_402_PAYMENT_REQUIRED)
        elif overlapRes == 3:
            serializer = UserInfoSerializer(data=request)

            if serializer.is_valid():
                serializer.save()
                return Response(4, status=status.HTTP_200_OK)
            else:
                return Response(3, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(5, status=status.HTTP_502_BAD_GATEWAY)

class ChangePwAPI(APIView):
    def post(self, request):
        print(f"ChangePwAPI Start")
        request = json.loads(request.body)
        print(request)

        # 비밀번호 변경 시작    
        changePw = ControlEdittingInfo_b()
        changePwRes = changePw.changePassword(request['nickname'], request['password'])

        # 결과 반환
        if changePwRes == 0:
            return Response(changePwRes, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif changePwRes == 1:
            return Response(changePwRes, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_502_BAD_GATEWAY)

class ChangeNicknameAPI(APIView):
    def post(self, request):
        print(f"ChangeNicknameAPI Start")
        request = json.loads(request.body)

        # 닉네임 변경 시작
        nicknameEdit = ControlEdittingInfo_b()
        changeResult = nicknameEdit.changeNickname(request['nickname'], request['uid'])
        
        # 결과 반환
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

'''
RecipePost
'''
class RecipeListAPI(APIView):
    def get(self, request, page):
        print(f"RecipeListAPI Start")
        print(f"페이지 = {page}")

        # 레시피 게시판 조회 시작
        recipeList = ControlRecipeList_b()
        requestRes, rlist, pageCnt = recipeList.requestRecipeList(page)

        serializer = RecipeListSerializer(rlist, many=True)

        # 결과 반환
        if requestRes == 0:
            return Response(0, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif requestRes >= 1:
            recipeDict = {}
            recipeDict['recipeList'] = serializer.data
            recipeDict['total_page'] = pageCnt
            return Response(recipeDict, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_502_BAD_GATEWAY)

class RecipePostAPI(APIView):
    def get(self, request, postId, nickname):
        print(f"RecipePostAPI Start")
        print(f"게시글 번호 = {postId}")

        # 레시피 게시글 조회 시작
        recipe = ControlRecipe_b()
        requestRes, recipePost, likeInfo = recipe.requestRecipe(postId, nickname)

        serializer = RecipeListSerializer(recipePost)

        # 결과 반환
        if requestRes == 0:
            return Response(0, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif requestRes == 1:
            recipeInfo = {}
            recipeInfo['recipeInfo'] = serializer.data
            recipeInfo['likeInfo'] = likeInfo
            return Response(recipeInfo, status=status.HTTP_200_OK)
        else:
            return Response(8, status=status.HTTP_502_BAD_GATEWAY)

    def post(self, request):
        print(f"RecipePostAPI Start")
        newRecipe = json.loads(request.body)
        print(f"게시글 등록 정보 = {newRecipe}")

        # 레시피 게시글 등록 시작
        insert = ControlRecipe_b()
        insertRes, recipe = insert.insertRecipe(newRecipe)
        
        serializer = RecipeListSerializer(recipe)

        # 결과 반환
        if insertRes == 2:
            return Response(2, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif insertRes == 3:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(8, status=status.HTTP_502_BAD_GATEWAY)

class RecipeModifyAPI(APIView):
    def post(self, request):
        print(f"RecipeModifyAPI Start")
        updatedRecipe = json.loads(request.body)
        print(f"수정된 게시글 정보 = {updatedRecipe}")

        # 레시피 게시글 수정 시작
        update = ControlRecipe_b()
        updateRes, updateRecipe = update.updateRecipe(updatedRecipe)

        # 결과 반환
        if updateRes == 4:
            return Response(4, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif updateRes == 5:
            return Response(updateRecipe, status=status.HTTP_200_OK)
        else:
            return Response(8, status=status.HTTP_502_BAD_GATEWAY)

class RecipeDeleteAPI(APIView):
    def post(self, request):
        print(f"RecipeDeleteAPI Start")
        deleteTarget = json.loads(request.body)
        print(f"삭제된 게시글 정보 = {deleteTarget}")

        # 레시피 게시글 삭제 시작
        delete = ControlRecipe_b()
        deleteRes = delete.deleteRecipe(deleteTarget['nickname'], deleteTarget['post_id'])

        # 결과 반환
        if deleteRes == 6:
            return Response(6, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif deleteRes == 7:
            return Response(7, status=status.HTTP_200_OK)
        else:
            return Response(8, status=status.HTTP_502_BAD_GATEWAY)

class RecipeLikeAPI(APIView):
    def post(self, request):
        print(f"RecipeLikeAPI Start")
        likeInfo = json.loads(request.body)
        print(f"좋아요 정보 = {likeInfo}")

        # 레시피 게시글 좋아요 시작
        like = ControlLike_b()
        if likeInfo['task'] == "취소":
            likeRes = like.cancelLike(likeInfo['nickname'], likeInfo['postType'], likeInfo['postId'])
        elif likeInfo['task'] == "등록":
            likeRes = like.pressLike(likeInfo['nickname'], likeInfo['postType'], likeInfo['postId'])

        # 결과 반환
        if likeRes == 0:
            return Response(0, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif likeRes == 1:
            return Response(1, status=status.HTTP_200_OK)
        elif likeRes == 2:
            return Response(2, status=status.HTTP_501_NOT_IMPLEMENTED)
        elif likeRes == 3:
            return Response(3, status=status.HTTP_200_OK)
        else:
            return Response(8, status=status.HTTP_502_BAD_GATEWAY)

class RecipeQueryAPI(APIView):
    def post(self, request):
        print(f"RecipeQueryAPI Start")
        searchInfo = json.loads(request.body)
        print(f"검색 정보 = {searchInfo}")

        # 레시피 게시판 검색 시작
        search = ControlRecipeList_b()
        searchRes, searchList, pageCnt = search.queryRecipeList(searchInfo['searchType'], searchInfo['categories'],
                                                        searchInfo['keywordType'], searchInfo['keyword'],
                                                        searchInfo['page'])

        # 결과 반환
        if searchRes == 2:
            return Response(2, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif searchRes == 3:
            serializer = RecipeListSerializer(searchList, many=True)
            searchDict = {}
            searchDict['recipeList'] = serializer.data
            searchDict['total_page'] = pageCnt
            return Response(searchDict, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_502_BAD_GATEWAY)

class RecipeSortAPI(APIView):
    def post(self, request):
        print(f"RecipeSortAPI Start")
        sortInfo = json.loads(request.body)
        print(f"정렬 정보 = {sortInfo}")
        
        # 레시피 게시판 정렬 시작
        sort = ControlRecipeList_b()
        sortRes, sortList = sort.arrangeRecipeList(sortInfo['arrangeBy'], sortInfo['page'])

        # 결과 반환
        if sortRes == 4:
            return Response(4, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif sortRes == 5:
            serializer = RecipeListSerializer(sortList, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_502_BAD_GATEWAY)

class RecipeReportAPI(APIView):
    def post(self, request):
        print(f"RecipeReportAPI Start")
        reportInfo = json.loads(request.body)
        print(f"레시피 게시글 삭제 정보 = {reportInfo}")

        # 레시피 게시글 신고 시작
        report = ControlReport_b()
        reportRes = report.reportPost(reportInfo)

        # 결과 반환
        if reportRes == 0:
            return Response(0, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif reportRes == 1:
            return Response(1, status=status.HTTP_200_OK)
        else:
            return Response(2, status=status.HTTP_502_BAD_GATEWAY)

class RecipeUnExistIngredientsAPI(APIView):
    def get(self, request, nickname, post_id):
        print(f"RecipeUnExistIngredientsAPI Start")
        print(f"없는 재료 보여주기 = {nickname, post_id}")

        # 없는 재료 보여주기 시작
        ueIngre = ControlIngredients_b()
        ueIngreRes, ueIngreList = ueIngre.requestUnExistIngredients(nickname, post_id)

        # 결과 반환
        if ueIngreRes == 0:
            return Response(0, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif ueIngreRes == 1:
            serializer = RecipeIngredientsSerializer(ueIngreList, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(4, status=status.HTTP_502_BAD_GATEWAY)

class RecipeDecreaseAPI(APIView):
    def get(self, request, nickname, post_id):
        print(f"RecipeDecreaseAPI Start")
        print(f"남은 재료 계산하기 = {nickname, post_id}")

        # 남은 재료 계산하기 시작
        daIngre = ControlIngredients_b()
        daIngreRes = daIngre.decreaseAmmounts(nickname, post_id)

        # 결과 반환
        if daIngreRes == 2:
            return Response(2, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif daIngreRes == 3:
            return Response(3, status=status.HTTP_200_OK)
        else:
            return Response(4, status=status.HTTP_502_BAD_GATEWAY)

'''
MyPage
'''   
class InquiryRefrigeratorAPI(APIView):
    def get(self, request, nickname):
        print("InquiryRefrigeraotrAPI Start")

        # 냉장고 재료 조회 시작
        refrigerator = ControlRefrigerator_b()
        result, code = refrigerator.requestRefrigerator(nickname)

        # 결과 반환
        if code == 0:
            return Response(code, status=status.HTTP_401_UNAUTHORIZED)
        elif code == 1:
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 2:
            serializers = InquiryRefrigeratorSerializer(data = result, many=True) 
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(9, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddRefrigeratorAPI(APIView):
    def post(self, request):
        print("AddRefrigeratorAPI Start")
        addTarget = json.loads(request.body)
       
        # 냉장고 재료 추가 시작
        refrigerator = ControlRefrigerator_b()
        result, code = refrigerator.insertRefrigerator(refrigerator = addTarget)
       
        # 결과 반환
        if code == 3:
            return Response(code, status = status.HTTP_400_BAD_REQUEST)
        elif code == 4:
            return Response(code, status = status.HTTP_200_OK)
        else:
            return Response(9, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteRefrigeratorAPI(APIView):
    def post(self, request):
        print("DeleteRefrigeratorAPI Start")
        deleteTarget = json.loads(request.body)

        # 냉장고 재료 삭제 시작
        refriInstance = ControlRefrigerator_b()
        result, code = refriInstance.deleteRefrigerator(deleteTarget['id'])

        # 결과 반환
        if code == 5:
            return Response(code, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif code == 6:
            return Response(code, status=status.HTTP_200_OK)
        else:
            return Response(9, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateRefrigeratorAPI(APIView):
    def post(self, request):
        print("UpdateRefrigeratorAPI 실행")
        updateTarget = json.loads(request.body)

        # 냉장고 재료 수정 시작
        refriInstance = ControlRefrigerator_b()
        result, code = refriInstance.updateRefrigerator(updateTarget)

        # 결과 반환
        if code == 7:
            return Response(code, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif code == 8:
            return Response(code, status=status.HTTP_200_OK)
        else:
            return Response(9, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InquiryMyPhotoPostsAPI(APIView):
    def get(self, request, nickname):
        print("InquiryMyPhotoPostsAPI Start")

        # 사용자가 작성한 요리 사진 게시글 조회 시작
        photoInstance = ControlMyPhoto_b()
        result, code = photoInstance.requestMyPhotoList(nickname = nickname)
        
        # 결과 반환
        if code == 0:
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 1:
            result = MyPhotoPostSerializer(data = result, many = True)
            result.is_valid()
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            return Response(2, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InquiryMyRecipePostsAPI(APIView):
    def get(self, request, nickname):
        print("InquiryMyRecipePostAPI Start")

        # 사용자가 작성한 레시피 게시글 조회 시작
        recipeInstance = ControlMyRecipe_b()
        result, code = recipeInstance.requestMyRecipeList(nickname = nickname)

        # 결과 반환
        if code == 0:
            return Response(code, status=status.HTTP_400_BAD_REQUEST)
        elif code == 1:
            result = RecipeListSerializer(data = result, many = True)
            result.is_valid()
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QueryMyRecipePostsAPI(APIView):
    def post(self, request):
        print("QueryMyRecipePostsAPI Start")
        queryTarget = json.loads(request.body)

        # 사용자가 작성한 레시피 게시글 검색 시작
        recipeInstance = ControlMyRecipe_b()
        result, code = recipeInstance.queryMyRecipeList(queryTarget['nickname'], queryTarget['keyword'])

        # 결과 반환
        if code == 2:
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 3:
            recipePosts = RecipeListSerializer(data = result, many = True)
            recipePosts.is_valid()
            return Response(recipePosts.data, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ArrangeMyRecipePostsAPI(APIView):
    def post(self, request):
        print("ArrangeMyRecipePostsAPI Start")
        arrangeTarget = json.loads(request.body)

        # 사용자가 작성한 레시피 게시글 정렬 시작
        recipeInstance = ControlMyRecipe_b()
        result, code = recipeInstance.arrangeMyRecipeList(arrangeTarget['nickname'], arrangeTarget['arrangeBy'])

        # 결과 반환
        if code == 4:
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 5:
            result = RecipeListSerializer(data=result, many=True)
            result.is_valid()
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InquiryMyLikePostsAPI(APIView):
    def get(self, request, nickname, postType):
        print("InquiryMyLikePostsAPI Start")

        # 사용자가 좋아요를 누른 게시글 조회 시작
        postsInstance = ControlPost_b()
        result, code = postsInstance.requestMyLikeList(nickname, postType)

        # 결과 반환 + postType 에 따라 다른 게시글 종류
        if code == 0:
            return Response(code, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        elif code == 1:
            if postType == 1:
                result = RecipeListSerializer(data=result, many=True)
                result.is_valid()
                return Response(result.data, status=status.HTTP_200_OK)
            elif postType == -1:
                result = MyPhotoPostSerializer(data=result, many=True)
                result.is_valid()
                return Response(result.data, status=status.HTTP_200_OK)
        else:
            return Response(4, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InquiryMyCommentPostsAPI(APIView):
    def get(self, request, nickname):
        print("InquiryMyCommentPostsAPI Start")
        
        # 사용자가 작성한 댓글 게시글 리스트 조회 시작
        postsInstance = ControlPost_b()
        result, code = postsInstance.requestMyCommentList(nickname)

        # 결과 반환
        if code == 2:
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 3:    
            result = RecipeListSerializer(data=result, many=True)
            result.is_valid()
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            return Response(4, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

'''
Comment
'''
class InsertCommentAPI(APIView):
    def post(self, request):
        print("InsertCommentAPI Start")
        insertTarget = json.loads(request.body)

        # 댓글 작성 시작
        commentInstance = ControlComment_b()
        code = commentInstance.insertComment(insertTarget)
        
        # 결과 반환
        if code == 0:
            return Response(code, status=status.HTTP_403_FORBIDDEN)
        elif code == 1:
            return Response(code, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateCommentAPI(APIView):
    def post(self, request):
        print("UpdateCommentAPI Start")
        updateTarget = json.loads(request.body)

        # 댓글 수정 시작
        commentInstance = ControlComment_b()
        code = commentInstance.updateComment(updateTarget)
        
        # 결과 반환
        if code == 2:
            return Response(code, status=status.HTTP_403_FORBIDDEN)
        elif code == 3:
            return Response(code, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteCommentAPI(APIView):
    def post(self, request):
        print("DeleteCommentAPI Start")
        deleteTarget = json.loads(request.body)

        # 댓글 삭제 시작
        commentInstance = ControlComment_b()
        code = commentInstance.deleteComment(deleteTarget['nickname'], deleteTarget['comment_id'])

        # 결과 반환
        if code == 4:
            return Response(code, status=status.HTTP_403_FORBIDDEN)
        elif code == 5:
            return Response(code, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReportCommentAPI(APIView):
    def post(self, request):
        print("ReportCommentAPI Start")
        reportTarget = json.loads(request.body)

        # 댓글 신고 시작
        reportInstance = ControlReport_b()
        code = reportInstance.reportComment(reportTarget)

        # 결과 반환
        if code == 2:
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 3:
            return Response(code, status=status.HTTP_200_OK)
        else:
            return Response(4, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

'''
PhotoPost
'''
class PhotoListAPI(APIView):
    def get(self, request, page):
        print("PhotoListAPI Start")
        print(f"페이지 = {page}")

        # 사진 게시판 조회 시작
        photoList = ControlPhotoList_b()
        requestRes, plist, pageCnt = photoList.requestPhotoList(page)

        serializer = MyPhotoPostSerializer(plist, many=True)

        # 결과 반환
        if requestRes == 0:
            return Response(0, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif requestRes == 1:
            photoDict = {}
            photoDict['photoList'] = serializer.data
            photoDict['total_page'] = pageCnt
            return Response(photoDict, status=status.HTTP_200_OK)
        else:
            return Response(4, status=status.HTTP_502_BAD_GATEWAY)

    def post(self, request):
        print("PhotoListAPI Start")
        sortInfo = json.loads(request.body)
        print(f"정렬 정보 = {sortInfo}")
        
        # 사진 게시판 정렬 시작
        sort = ControlPhotoList_b()
        sortRes, sortList = sort.arrangePhotoList(sortInfo['arrangeBy'], sortInfo['page'])

        # 결과 반환
        if sortRes == 2:
            return Response(4, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif sortRes == 3:
            serializer = MyPhotoPostSerializer(sortList, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(4, status=status.HTTP_502_BAD_GATEWAY)

class PhotoPostAPI(APIView):
    def get(self, request, postId, nickname):
        print("PhotoPostAPI Start")
        print(f"게시글 번호 = {postId}")

        # 사진 게시글 조회 시작
        photo = ControlPhoto_b()
        requestRes, photoPost, likeInfo = photo.requestPhoto(postId, nickname)

        # 결과 반환
        if requestRes == 0:
            return Response(0, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif requestRes == 1:
            photoInfo = {}
            photoInfo['photoInfo'] = photoPost
            photoInfo['likeInfo'] = likeInfo
            return Response(photoInfo, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_502_BAD_GATEWAY)

    def post(self, request):
        print("PhotoPostAPI Start")
        photoInfo = json.loads(request.body)
        print(f"사진 게시글 정보 = {photoInfo}")

        # 사진 게시글 등록 시작
        photo = ControlPhoto_b()
        insertRes, newPhoto = photo.insertPhoto(photoInfo)

        # 결과 반환
        if insertRes == 2:
            return Response(2, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif insertRes == 3:
            return Response(newPhoto.data, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_502_BAD_GATEWAY)

    def delete(self, request):
        print("PhotoPostAPI Start")
        deleteTarget = json.loads(request.body)
        print(f"삭제할 게시글 정보 = {deleteTarget}")

        # 사진 게시글 삭제 시작
        delete = ControlPhoto_b()
        deleteRes = delete.deletePhoto(deleteTarget['nickname'], deleteTarget['post_id'])

        # 결과 반환
        if deleteRes == 4:
            return Response(4, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif deleteRes == 5:
            return Response(5, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_502_BAD_GATEWAY)

class PhotoLikeAPI(APIView):
    def post(self, request):
        print("PhotoLikeAPI Start")
        likeInfo = json.loads(request.body)
        print(f"좋아요 정보 = {likeInfo}")

        # 사진 게시글 좋아요 시작
        like = ControlLike_b()
        if likeInfo['task'] == "취소":
            likeRes = like.cancelLike(likeInfo['nickname'], likeInfo['postType'], likeInfo['postId'])
        elif likeInfo['task'] == "등록":
            likeRes = like.pressLike(likeInfo['nickname'], likeInfo['postType'], likeInfo['postId'])

        # 결과 반환
        if likeRes == 4:
            return Response(4, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif likeRes == 5:
            return Response(5, status=status.HTTP_200_OK)
        elif likeRes == 6:
            return Response(6, status=status.HTTP_501_NOT_IMPLEMENTED)
        elif likeRes == 7:
            return Response(7, status=status.HTTP_200_OK)
        else:
            return Response(8, status=status.HTTP_502_BAD_GATEWAY)

class PhotoReportAPI(APIView):
    def post(self, request):
        print("PhotoReportAPI Start")
        reportInfo = json.loads(request.body)
        print(f"사진 게시글 삭제 정보 = {reportInfo}")

        # 사진 게시글 신고 시작
        report = ControlReport_b()
        reportRes = report.reportPost(reportInfo)

        # 결과 반환
        if reportRes == 0:
            return Response(0, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif reportRes == 1:
            return Response(1, status=status.HTTP_200_OK)
        else:
            return Response(2, status=status.HTTP_502_BAD_GATEWAY)

'''
Mail
'''
class MailBoxAPI(APIView):
    def get(self, request, nickname, page):
        print("MailBoxAPI Start")

        # 쪽지함 조회 시작
        mailInstance = ControlMailList_b()
        result, mailList, pageCnt = mailInstance.requestMailList(page, nickname)

        serializer = MyMailListSerializer(mailList, many = True)

        # 결과 반환
        if result == 0:
            return Response(0, status=status.HTTP_404_NOT_FOUND)
        elif result == 1:
            mailDict = {}
            mailDict['mailList'] = serializer.data
            mailDict['total_page'] = pageCnt
            return Response(mailDict, status=status.HTTP_200_OK)
        else:
            return Response(2, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InquiryMailAPI(APIView):
    def get(self, request, mail_id):
        print("InquiryMailAPI Start")
        
        # 쪽지 조회 시작
        mailInstance = ControlMail_b()
        result, code= mailInstance.requestMail(mail_id) 

        # 결과 반환
        if code == 0:
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 1:
            result = MyMailListSerializer(result)
            print(result.data)
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InsertMailAPI(APIView):
    def post(self, request):
        print("InsertMailAPI Start")
        request = json.loads(request.body)

        # 쪽지 전송 시작
        mailInstance = ControlMail_b()
        result, code = mailInstance.insertMail(request)
        
        # 결과 반환
        if code == 2:
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 3:
            serializer = MyMailListSerializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteMailAPI(APIView):
    def post(self, request):
        print("DeleteMailAPI Start")
        request = json.loads(request.body)

        # 쪽지 삭제 시작
        mailInstance = ControlMail_b()
        result, code = mailInstance.deleteMail(request['nickname'], request['mail_id'])

        # 결과 반환
        if code == 4:
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 5:
            return Response(code, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_500_INTERNAL_SERVER_ERROR)