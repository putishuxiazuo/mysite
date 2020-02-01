from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .models import Comment
from Blog.models import Blog

# Create your views here.
def update_comment(request):
    user = request.user
    text = request.POST.get('text','')
    object_id = int(request.POST.get('object_id',''))
    content_type = request.POST.get('content-type','')
    #查询当前Blog对象
    current_model_class = ContentType.objects.get(model = content_type).model_class()
    model_object = current_model_class.objects.get(pk = object_id)
    #创建Comment实例（对象）
    comment = Comment()
    comment.user = user
    comment.text = text
    comment.content_object = model_object
    comment.save()
    refer = request.META.get('HTTP_REFERER', '/')
    return redirect(refer)
