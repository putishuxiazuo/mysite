from django.contrib import admin
from .models import BlogType,Blog

# Register your models here.

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ("id","type_name")


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id',"title","blog_type",'ReadNum',"author","last_update_time")

'''
@admin.register(Read_Num)
class Read_NumAdmin(admin.ModelAdmin):
    list_display = ("read_num","blog")
'''
