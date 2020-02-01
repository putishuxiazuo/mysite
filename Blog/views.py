from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from .models import BlogType,Blog
from django.contrib.contenttypes.models import ContentType
from read_account.models import ReadNum
from Comment.models import Comment
#统计各分类下博客的数量
def blog_count_by_type():
    '''

    :param request:
    :return:字典，各分类下博客的数量
    '''
    blog_count_by_type = {}
    blog_types = BlogType.objects.all()
    for blog_type in blog_types:
        blogs = Blog.objects.filter(blog_type = blog_type)
        #print(blogs)
        if blogs:
            blog_count_by_type[blog_type.type_name] = blogs.count()
        else:
            blog_count_by_type[blog_type.type_name] = 0
    return blog_count_by_type

# 主页，显示博客列表

def Blog_list(request):
    blog_lists = Blog.objects.all().order_by('-id')
    #print(blog_lists)
    paginator = Paginator(blog_lists,6)    #分页，以每6篇内容为一页
    page_num = request.GET.get('page',1)    #获取get方法传入的page参数
    page_content = paginator.get_page(page_num) #获取对应的页面!!!!
    current_page_num = page_content.number  #获取当前页面数
    #限定页面下方导航链接：以当前页面为中心，前后各显示两页，若当前页小于2，取第一页，
     #   若当前页后两页超范围，区最后一页
    #   !!!!分页算法
    page_range = list(range(max(current_page_num-2,1),min(current_page_num+3,paginator.num_pages+1)))
    #添加省略号
    if current_page_num-1 >= 4:
        page_range.insert(0, '...')
    if paginator.num_pages-current_page_num >= 4:
        page_range.append('...')
    #添加首页和尾页
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    page_of_blogs = page_content.object_list    #获取页面内容
    blog_types = blog_count_by_type()         #调用方法，返回blog_count_by_type
    #blog_types = BlogType.objects.all()
    blog_dates = Blog.objects.dates('created_time','year','DESC')
    return render(request,"bloglist.html",{"page_of_blogs":page_of_blogs,"blog_types":blog_types
                                           ,'page_content':page_content,'page_range':page_range,
                                           'blog_dates':blog_dates})

#显示各个博客的细节
def Blog_detail(request,Blog_pk):
    '''
    :param request:
    :param Blog_pk:表Blog的主键
    :return: 博客列表以及博客分类
    '''
    context = {}
    blog = get_object_or_404(Blog, pk=Blog_pk)
    #从Comment中筛选评论并显示
    blog_model_ct = ContentType.objects.get_for_model(Blog)
    comments = Comment.objects.filter(content_type=blog_model_ct,object_id=blog.pk,parent =None).order_by('-comment_time')
    context['comments'] = comments


    if not request.COOKIES.get('blog_{0}_read'.format(Blog_pk)):
        #判断ReadNum表是否存在read_num字段，若存在，数字加一，否则，创建该记录
        ct = ContentType.objects.get_for_model(Blog)
        if ReadNum.objects.filter(content_type = ct,object_id = blog.pk).count():
            readnum = ReadNum.objects.get(content_type = ct,object_id = blog.pk)
        else:
            readnum = ReadNum(content_type = ct,object_id = blog.pk)
        readnum.read_num += 1
        readnum.save()

    context['blog_list'] = blog
    #筛选出当前博客的上一条博文
    context['previous_blog'] = Blog.objects.filter(id__gt=blog.id).last()
    #print(Blog.objects.filter(created_time__gt=blog.created_time))
    # 筛选出当前博客的下一条博文
    context['next_blog'] = Blog.objects.filter(id__lt=blog.id).first()
    #print(Blog.objects.filter(created_time__lt=blog.created_time))
    response = render(request,"blog_detail.html",context)
    response.set_cookie('blog_{0}_read'.format(Blog_pk),'True')
    return response


#按分类显示相应博文
def Blogs_with_type(request):
    '''blog_type_pk：模型Blog_type记录的主键；
       blog_name:模型Blog_type对象；
       blog_type_lists:同一个分类的对象。'''
    blog_name = request.GET.get('type')
    blog_type= BlogType.objects.filter(type_name = blog_name)
    #blog_name = get_object_or_404(BlogType,pk=blog_type_pk)
    blog_types = BlogType.objects.all()
    blog_type_lists = Blog.objects.filter(blog_type = blog_type.first())
    return  render(request,'blog_with_type.html',{'page_of_blogs':blog_type_lists,
                                                  'blog_name':blog_name,"blog_types":blog_types})


def Blog_with_date(request,year,month):
    '''
    :param request:
    :param year:年份
    :param month: 月份
    :return:page_of_blogs》》》指定页面的内容
    blog_dates>>>按照年月输出的日期对象
    page_range>>>下方显示的页面导航范围
    page_content>>>获取对应的页面
    page_of_blogs>>>页面内容
    current_date>>>函数接收的日期
    '''
    context = {}
    current_date = '{0}年{1}月'.format(year,month)
    blog_lists = Blog.objects.filter(created_time__year = year,created_time__month = month)
    # print(blog_lists)
    paginator = Paginator(blog_lists, 6)  # 分页，以每6篇内容为一页
    page_num = request.GET.get('page', 1)  # 获取get方法传入的page参数
    page_content = paginator.get_page(page_num)  # 获取对应的页面!!!!
    current_page_num = page_content.number  # 获取当前页面数
    # 限定页面下方导航链接：以当前页面为中心，前后各显示两页，若当前页小于2，取第一页，
    #   若当前页后两页超范围，区最后一页
    #   !!!!分页算法
    page_range = list(range(max(current_page_num - 2, 1), min(current_page_num + 3, paginator.num_pages + 1)))
    # 添加省略号
    if current_page_num - 1 >= 4:
        page_range.insert(0, '...')
    if paginator.num_pages - current_page_num >= 4:
        page_range.append('...')
    # 添加首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    page_of_blogs = page_content.object_list  # 获取页面内容
    blog_types = BlogType.objects.all()
    blog_dates = Blog.objects.dates('created_time', 'year', 'DESC')
    return render(request, "blog_with_date.html", {"page_of_blogs": page_of_blogs, "blog_types": blog_types
        , 'page_content': page_content, 'page_range': page_range,
                                             'blog_dates': blog_dates,'current_date':current_date})
