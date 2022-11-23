from django.contrib import admin

from .models import *

'''
221105 User 관련 데이터 관리 admin 추가
221123 모든 데이터 관리 admin 추가
'''

# Register your models here.
admin.site.register(User)
admin.site.register(PhotoPost)
admin.site.register(RecipePost)
admin.site.register(Mail)
admin.site.register(LikeInfo)
admin.site.register(Comment)
admin.site.register(Refrigerator)
admin.site.register(Recipe_Ingredients)
admin.site.register(Report)
admin.site.register(TempEmail)
admin.site.register(Units)
admin.site.register(Ingredients)
