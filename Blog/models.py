from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from read_account.models import ReadNum



class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return "{0}".format(self.type_name)


class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    content =RichTextUploadingField()
    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{0}".format(self.title)

    def ReadNum(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct,object_id=self.pk)
            return readnum.read_num
        except:
            return 0



'''
class Read_Num(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING)
'''


