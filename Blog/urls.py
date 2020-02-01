
from django.urls import path,re_path
from . import views

urlpatterns = [
    #localhost:8000/blog>>>主页
    path('',views.Blog_list,name = 'Blog_list'),
    #localhost:8000/blog/[0-9]+/>>>具体的博客内容
    re_path(r'^(?P<Blog_pk>[0-9]+)/$', views.Blog_detail,name="Blog_detail"),
    #localhost:8000/blog/type/[0-9]+/>>>不同分类下的博客汇总
    path('type/',views.Blogs_with_type,name="Blogs_with_type"),
    #localhost:8000/blog/date/year/month>>>不同日期下的博客
    path('date/<int:year>/<int:month>/',views.Blog_with_date,name='Blog_with_date'),
]