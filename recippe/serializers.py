from dataclasses import field
from re import search
from rest_framework import serializers
from .models import Ingredients, Units, User,  PhotoPost, RecipePost, Mail, LikeInfo, Comment, Refrigerator, Recipe_Ingredients, Report, TempEmail

'''
221105 유저 serializer 추가
221105 이메일인증 serializer 추가
221108 레시피게시판 serializer 추가
221109 냉장고조회 serializer 추가
'''

class ResultSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField()
    fields = ('code')


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname', 'uid', 'password', 'email', 'auto_login')

class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempEmail
        fields = ('email', 'code')

class InquiryRefrigeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refrigerator
        fields = ('name', 'nickname', 'unit', 'amount', 'expiry_date')

class RecipeIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe_Ingredients
        fields = ('name', 'post_id', 'unit', 'amount')

class RecipeListSerializer(serializers.ModelSerializer):
    Recipe_Ingredients = RecipeIngredientsSerializer(many=True, read_only=True)
    class Meta:
        model = RecipePost
        fields = ('post_id', 'nickname', 'title', 'category', 'degree_of_spicy', 'description', 'views', 'like_count', 'comment_count', 'upload_time', 'Recipe_Ingredients')
