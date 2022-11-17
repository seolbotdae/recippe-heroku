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
from .recipepost import *
from .report import *
from .ingredients import *
from .like import *
from .photopost import *

# Create your views here.

# json 파싱을 위한 header
import json

'''
221105  로그인 view 추가
221105  이메일 view 추가
221105  자동로그인 해제 view 추가
221106  이메일 인증 get 함수 추가
221106  최종 회원가입 view 추가
221107  비밀번호 변경 view 추가
221107  냉장고 조회 view 추가
221108  닉네임 변경 view 추가
221109  레시피 view 추가 (게시판 조회, 게시글 조회)
221109  냉장고 조회 view 추가 
221114  레시피 수정 view 추가 (게시글 수정)
221114  레시피 삭제 view 추가 (게시글 삭제)
221115  냉장고 추가 view 추가 
        냉장고 재료 삭제 view 추가 
        냉장고 재료 변경 view 추가
        사용자 작성 사진 게시글 view 추가
221116  사용자 작성 레시피 게시글 view 추가
        사용자 작성 레시피 검색 view 추가
        레시피 신고 view 추가
        레시피 없는 재료 보여주기 view 추가
        사용자 작성 레시피 정렬 view 추가
        사용자 좋아요 게시글 조회 view 추가
        사용자 댓글단 게시글 조회 view 추가
        레시피 남은 재료 계산하기 view 추가
        레시피 게시글 검색, 정렬 view 추가
        레시피 게시글 좋아요 view 추가
221117  레시피 댓글 추가, 수정, 삭제 view 추가
        레시피 댓글 신고 view 추가
        사진 게시판 view 추가
        사진 게시글 조회 view 추가
        사진 게시글 등록 view 추가
        사진 게시글 삭제, 좋아요, 정렬, 신고 view 추가
'''

class LoginAPI(APIView):
    def post(self, request):
        print(f"LoginAPI Start")
        data = json.loads(request.body)
        
        inputId = data['uid']
        inputPw = data['password']

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
        print(f"LogoutAPI Start")
        data = json.loads(request.body)

        print(f"CancleAutoLogin Class start")

        inputNickname = data['nickname']

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
        print(f"EmailStartAPI Start")
        data = json.loads(request.body)

        print(data['email'])

        emailVerification = ControlEmailVerification_b()
        uploadRes = emailVerification.startCheck(data)

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

        emailVerification = ControlEmailVerification_b()
        checkRes = emailVerification.finishCheck(data)

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

class RecipeListAPI(APIView):
    def get(self, request, page):
        print(f"페이지 = {page}")

        recipeList = ControlRecipeList_b()
        requestRes, rlist, pageCnt = recipeList.requestRecipeList(page)

        serializer = RecipeListSerializer(rlist, many=True)

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
    def get(self, request, postId):
        print(f"게시글 번호 = {postId}")

        recipe = ControlRecipe_b()
        requestRes, recipePost = recipe.requestRecipe(postId)

        serializer = RecipeListSerializer(recipePost)

        if requestRes == 0:
            return Response(0, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif requestRes == 1:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(8, status=status.HTTP_502_BAD_GATEWAY)

    def post(self, request):
        newRecipe = json.loads(request.body)
        print(f"게시글 등록 정보 = {newRecipe}")

        insert = ControlRecipe_b()
        insertRes, recipe = insert.insertRecipe(newRecipe)
        
        serializer = RecipeListSerializer(recipe)
        if insertRes == 2:
            return Response(2, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif insertRes == 3:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(8, status=status.HTTP_502_BAD_GATEWAY)

class RecipeModifyAPI(APIView):
    def post(self, request):
        updatedRecipe = json.loads(request.body)
        print(f"수정된 게시글 정보 = {updatedRecipe}")

        update = ControlRecipe_b()
        updateRes, updateRecipe = update.updateRecipe(updatedRecipe)

        if updateRes == 4:
            return Response(4, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif updateRes == 5:
            return Response(updateRecipe, status=status.HTTP_200_OK)
        else:
            return Response(8, status=status.HTTP_502_BAD_GATEWAY)

class RecipeDeleteAPI(APIView):
    def post(self, request):
        deleteTarget = json.loads(request.body)
        print(f"삭제된 게시글 정보 = {deleteTarget}")

        delete = ControlRecipe_b()
        deleteRes = delete.deleteRecipe(deleteTarget['nickname'], deleteTarget['post_id'])

        if deleteRes == 6:
            return Response(6, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif deleteRes == 7:
            return Response(7, status=status.HTTP_200_OK)
        else:
            return Response(8, status=status.HTTP_502_BAD_GATEWAY)

class RecipeLikeAPI(APIView):
    def post(self, request):
        likeInfo = json.loads(request.body)
        print(f"좋아요 정보 = {likeInfo}")

        like = ControlLike_b()
        if likeInfo['task'] == "취소":
            likeRes = like.cancelLike(likeInfo['nickname'], likeInfo['postType'], likeInfo['postId'])
        elif likeInfo['task'] == "등록":
            likeRes = like.pressLike(likeInfo['nickname'], likeInfo['postType'], likeInfo['postId'])

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
        searchInfo = json.loads(request.body)
        print(f"검색 정보 = {searchInfo}")

        search = ControlRecipeList_b()
        searchRes, searchList, pageCnt = search.queryRecipeList(searchInfo['searchType'], searchInfo['categories'],
                                                        searchInfo['keywordType'], searchInfo['keyword'],
                                                        searchInfo['page'])

        if searchRes == 2:
            return Response(2, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif searchRes == 3:
            serializer = RecipeListSerializer(searchList, many=True)
            searchDict = {}
            searchDict['searchList'] = serializer.data
            searchDict['total_page'] = pageCnt
            return Response(searchDict, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_502_BAD_GATEWAY)

class RecipeSortAPI(APIView):
    def post(self, request):
        sortInfo = json.loads(request.body)
        print(f"정렬 정보 = {sortInfo}")
        
        sort = ControlRecipeList_b()
        sortRes, sortList = sort.arrangeRecipeList(sortInfo['arrangeBy'], sortInfo['page'])

        if sortRes == 4:
            return Response(4, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif sortRes == 5:
            serializer = RecipeListSerializer(sortList, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(6, status=status.HTTP_502_BAD_GATEWAY)

class RecipeReportAPI(APIView):
    def post(self, request):
        reportInfo = json.loads(request.body)
        print(f"레시피 게시글 삭제 정보 = {reportInfo}")

        report = ControlReport_b()
        reportRes = report.reportPost(reportInfo)

        if reportRes == 0:
            return Response(0, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif reportRes == 1:
            return Response(1, status=status.HTTP_200_OK)
        else:
            return Response(2, status=status.HTTP_502_BAD_GATEWAY)

class RecipeUnExistIngredientsAPI(APIView):
    def post(self, request):
        requestInfo = json.loads(request.body)
        print(f"없는 재료 보여주기 = {requestInfo}")

        ueIngre = ControlIngredients_b()
        ueIngreRes, ueIngreList = ueIngre.requestUnExistIngredients(requestInfo['nickname'], requestInfo['post_id'])

        if ueIngreRes == 0:
            return Response(0, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif ueIngreRes == 1:
            serializer = RecipeIngredientsSerializer(ueIngreList, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(4, status=status.HTTP_502_BAD_GATEWAY)

class RecipeDecreaseAPI(APIView):
    def post(self, request):
        requestInfo = json.loads(request.body)
        print(f"남은 재료 계산하기 = {requestInfo}")

        daIngre = ControlIngredients_b()
        daIngreRes = daIngre.decreaseAmmounts(requestInfo['nickname'], requestInfo['post_id'])

        if daIngreRes == 2:
            return Response(2, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif daIngreRes == 3:
            return Response(3, status=status.HTTP_200_OK)
        else:
            return Response(4, status=status.HTTP_502_BAD_GATEWAY)
   
class InquiryRefrigeratorAPI(APIView):
    def get(self, request, nickname):
        print("API : InquiryRefrigeraotrAPI Start")

        refrigerator = ControlRefrigerator_b()
        result, code = refrigerator.requestRefrigerator(nickname)

        if code == 0:
            print("API : 냉장고 조회 실패 응답")
            return Response(code, status=status.HTTP_401_UNAUTHORIZED)
        elif code == 1:
            print("API : 냉장고 식재료 없음 응답")
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 2:
            print("API : 냉장고 조회 성공 응답")
            serializers = InquiryRefrigeratorSerializer(data = result, many=True) 
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            print("API : 알 수 없는 오류 응답")
            return Response(code, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddRefrigeratorAPI(APIView):
    def post(self, request):
        print("API : AddRefrigeratorAPI Start")
        addTarget = json.loads(request.body)
       
        refrigerator = ControlRefrigerator_b()
        result, code = refrigerator.insertRefrigerator(refrigerator = addTarget)
       
        if code == 3:
            print("API : 냉장고 추가 실패 응답")
            return Response(code, status = status.HTTP_400_BAD_REQUEST)
        elif code == 4:
            print("API : 냉장고 추가 성공 응답")
            return Response(code, status = status.HTTP_200_OK)
        else:
            print("API : 알 수 없는 오류 응답")
            return Response(code, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteRefrigeratorAPI(APIView):
    def post(self, request):
        print(f"API : DeleteRefrigeratorAPI 실행")
        deleteTarget = json.loads(request.body)
        refriInstance = ControlRefrigerator_b()
        result, code = refriInstance.deleteRefrigerator(deleteTarget['id'],None,None)

        if code == 5:
            print("API : 냉장고 삭제 실패 응답")
            return Response(code, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif code == 6:
            print("API : 냉장고 삭제 성공 응답")
            return Response(code, status=status.HTTP_200_OK)
        else:
            print("서버 : 알 수 없는 오류 응답")
            return Response(code, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateRefrigeratorAPI(APIView):
    def post(self, request):
        print(f"API : UpdateRefrigeratorAPI 실행")
        updateTarget = json.loads(request.body)
        refriInstance = ControlRefrigerator_b()
        result, code = refriInstance.updateRefrigerator(updateTarget)

        if code == 7:
            print("API : 냉장고 변경 실패 응답")
            return Response(code, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif code == 8:
            print("API : 냉장고 변경 성공 응답")
            return Response(code, status=status.HTTP_200_OK)
        else:
            print("API : 알 수 없는 오류 응답")
            return Response(code, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InquiryMyPhotoPostsAPI(APIView):
    def get(self, request, nickname):
        print("API : InquiryMyPhotoPostsAPI Start")

        photoInstance = ControlMyPhoto_b()
        result, code = photoInstance.requestMyPhotoList(nickname = nickname)
        
        if code == 0:
            print("API : 사용자 사진 게시글 조회 실패 응답")
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 1:
            result = MyPhotoPostSerializer(data = result, many = True)
            result.is_valid()
            print("API : 사용자 사진 게시글 조회 성공 응답")
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            print("API : 알 수 없는 오류 응답")
            return Response(code, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InquiryMyRecipePostsAPI(APIView):
    def get(self, request, nickname):
        print("API : InquiryMyRecipePostAPI Start")

        recipeInstance = ControlMyRecipe_b()
        result, code = recipeInstance.requestMyRecipeList(nickname = nickname)

        if code == 0:
            print("API : 사용자 작성 레시피 조회 실패 응답")
            return Response(code, status=status.HTTP_400_BAD_REQUEST)
        elif code == 1:
            print("API : 사용자 작성 레시피 조회 성공 응답")
            result = RecipeListSerializer(data = result, many = True)
            result.is_valid()
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            print("API : 알 수 없는 오류 응답")
            return Response(code, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QueryMyRecipePostsAPI(APIView):
    def post(self, request):
        print("API : QueryMyRecipePostsAPI Start")
        queryTarget = json.loads(request.body)

        recipeInstance = ControlMyRecipe_b()
        result, code = recipeInstance.queryMyRecipeList(queryTarget['nickname'], queryTarget['keyword'])

        if code == 2:
            print("API : 사용자 작성 레시피 게시글 검색 실패 응답")
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 3:
            print("API : 사용자 작성 레시피 게시글 검색 성공 응답")
            recipePosts = RecipeListSerializer(data = result, many = True)
            recipePosts.is_valid()
            
            return Response(recipePosts.data, status=status.HTTP_200_OK)
        else:
            print("API : 알 수 없는 오류 응답")
            return Response(code, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ArrangeMyRecipePostsAPI(APIView):
    def post(self, request):
        print("API : ArrangeMyRecipePostsAPI Start")
        arrangeTarget = json.loads(request.body)

        recipeInstance = ControlMyRecipe_b()
        result, code = recipeInstance.arrangeMyRecipeList(arrangeTarget['nickname'], arrangeTarget['arrangeBy'])

        if code == 4:
            print("API : 사용자 작성 레시피 정렬 실패 응답")
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 5:
            print("API : 사용자 작성 레시피 정렬 성공 응답")
            result = RecipeListSerializer(data=result, many=True)
            result.is_valid()
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            print("API : 알 수 없는 오류 응답")
            return Response(code, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InquiryMyLikePostsAPI(APIView):
    def post(self, request):
        print("API : InquiryMyLikePostsAPI Start")
        inquiryTarget = json.loads(request.body)

        postsInstance = ControlPost_b()
        result, code = postsInstance.requestMyLikeList(inquiryTarget['nickname'], inquiryTarget['postType'])

        if code == 0:
            print("API : 사용자 좋아요 게시글 조회 실패 응답")
            return Response(code, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        elif code == 1:
            if inquiryTarget['postType'] == 1:
                result = RecipeListSerializer(data=result, many=True)
                print("API : 사용자 좋아요 레시피 게시글 조회 성공 응답")
                result.is_valid()
                return Response(result.data, status=status.HTTP_200_OK)
            elif inquiryTarget['postType'] == -1:
                result = MyPhotoPostSerializer(data=result, many=True)
                print("API : 사용자 좋아요 사진 게시글 조회 성공 응답")
                result.is_valid()
                return Response(result.data, status=status.HTTP_200_OK)
        else:
            print("API : 알 수 없는 오류 응답")
            return Response(code, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InquiryMyCommentPostsAPI(APIView):
    def get(self, request, nickname):
        print("API : InquiryMyCommentPostsAPI Start")
        
        postsInstance = ControlPost_b()
        result, code = postsInstance.requestMyCommentList(nickname)

        if code == 2:
            print("API : 사용자 댓글단 게시글 조회 실패 응답")
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 3:    
            result = RecipeListSerializer(data=result, many=True)
            result.is_valid()
            print("API : 사용자 댓글단 게시글 조회 성공 응답")
            return Response(result.data, status=status.HTTP_200_OK)
        else:
            print("API : 알 수 없는 오류 응답")
            return Response(code, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InsertCommentAPI(APIView):
    def post(self, request):
        print("API : InsertCommentAPI Start")
        insertTarget = json.loads(request.body)

        commentInstance = ControlComment_b()
        code = commentInstance.insertComment(insertTarget)
        
        if code == 0:
            print("API : 댓글 등록 실패 응답")
            return Response(code, status=status.HTTP_403_FORBIDDEN)
        elif code == 1:
            print("API : 댓글 등록 성공 응답")
            return Response(code, status=status.HTTP_200_OK)
        else:
            print("API : 알 수 없는 오류 응답")
            return Response(code, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateCommentAPI(APIView):
    def post(self, request):
        print("API : UpdateCommentAPI Start")
        updateTarget = json.loads(request.body)

        commentInstance = ControlComment_b()
        code = commentInstance.updateComment(updateTarget)
        
        if code == 2:
            print("API : 댓글 수정 실패 응답")
            return Response(code, status=status.HTTP_403_FORBIDDEN)
        elif code == 3:
            print("API : 댓글 수정 성공 응답")
            return Response(code, status=status.HTTP_200_OK)
        else:
            print("API : 알 수 없는 오류 응답")
            return Response(code, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteCommentAPI(APIView):
    def post(self, request):
        print("API : DeleteCommentAPI Start")
        deleteTarget = json.loads(request.body)
        commentInstance = ControlComment_b()
        code = commentInstance.deleteComment(deleteTarget['nickname'], deleteTarget['comment_id'])

        if code == 4:
            print("API : 댓글 삭제 실패 응답")
            return Response(code, status=status.HTTP_403_FORBIDDEN)
        elif code == 5:
            print("API : 댓글 삭제 성공 응답")
            return Response(code, status=status.HTTP_200_OK)
        else:
            print("API : 알 수 없는 오류 응답")
            return Response(code, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReportCommentAPI(APIView):
    def post(self, request):
        print("API : ReportCommentAPI Start")
        reportTarget = json.loads(request.body)
        reportInstance = ControlReport_b()
        code = reportInstance.reportComment(reportTarget)

        if code == 2:
            print("API : 댓글 신고 실패 응답")
            return Response(code, status=status.HTTP_404_NOT_FOUND)
        elif code == 3:
            print("API : 댓글 신고 성공 응답")
            return Response(code, status=status.HTTP_200_OK)
        else:
            print("알 수 없는 오류 응답")
            return Response(4, status=status.HTTP_500_INTERNAL_SERVER_ERROR)