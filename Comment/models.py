from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Comment(models.Model):
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    #写评论的用户
    user = models.ForeignKey(User,related_name = 'comments',on_delete=models.DO_NOTHING)


    content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    root = models.ForeignKey('self', related_name = 'root_comment',null=True, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey('self',related_name = 'parent_comment',null=True,on_delete=models.DO_NOTHING)
    #回复上一级评论的的用户
    reply_to = models.ForeignKey(User,related_name = 'replies', null=True,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text

