from dataclasses import field
from re import search
from rest_framework import serializers
from .models import Ingredients, Units, User,  PhotoPost, RecipePost, Mail, LikeInfo, Comment, Refrigerator, Recipe_Ingredients, Report, TempEmail


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
        fields = ('id', 'name', 'nickname', 'unit', 'amount', 'expiry_date')

class RecipeIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe_Ingredients
        fields = ('id', 'name', 'post_id', 'unit', 'amount')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment_id', 'nickname', 'post_id', 'comments', 'comment_time')

class RecipeListSerializer(serializers.ModelSerializer):
    Recipe_Ingredients = RecipeIngredientsSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = RecipePost
        fields = ('post_id', 'nickname', 'title', 'category', 'degree_of_spicy', 'description', 'views', 'like_count', 'comment_count', 'upload_time', 'Recipe_Ingredients', 'comments')

class MyPhotoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoPost
        fields = ('post_id', 'photo_link', 'like_count', 'upload_time', 'nickname')

class MyLikePhotoPostSerializer(serializers.ModelSerializer):
    photo = MyPhotoPostSerializer(many=True, read_only=True)
    class Meta:
        model = LikeInfo
        fields = ('like_id', 'post_type', 'nickname', 'post_id', 'photo')

class MyLikeRecipePostSerializer(serializers.ModelSerializer):
    recipe = RecipeListSerializer(many=True, read_only=True)
    class Meta:
        model = LikeInfo
        fields = ('like_id', 'post_type', 'nickname', 'post_id', 'recipe')

class MyMailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = ('mail_id', 'nickname', 'receiver', 'title', 'contents', 'send_time', 'sender_check', 'receiver_check')