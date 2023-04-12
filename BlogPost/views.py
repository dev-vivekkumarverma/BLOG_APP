from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rest_framework import generics
from .models import Blog
from rest_framework.decorators import api_view
from .serializer import BlogSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework import status
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# app_name="BlogPost"
# Create your views here.


# @login_required(login_url='login')
# @api_view(['GET'])
# def BlogListView(request):
#     if request.method=='GET':
#         username=request.user
#         queryset=Blog.objects.select_related("createdBy").all().order_by('-createdOn')
#         serializedData=BlogSerializer(queryset,many=True)
#         # print(serializedData.data)
#         return render(request=request,template_name="BlogList.html",context={"blogs":serializedData.data,'user':username})


@login_required(login_url='login')
@api_view(['GET'])
def DetailedBlogView(request, slugId):
    userId = request.user.id
    try:
        blogInstance = Blog.objects.get(slug=slugId)
        if request.method == 'GET':
            serializedData = BlogSerializer(blogInstance)
            # print(serializedData.data)
            return render(request=request, template_name='BlogDetail.html', context={'blog': serializedData.data, 'user': request.user})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


# view for creating new Post
@login_required(login_url='login')
@api_view(['GET', 'POST'])
def CreateNewBlogView(request):
    try:
        if request.method == 'POST':
            if request.user.is_authenticated:
                user = request.user
                title = request.data.get("title")
                body = request.data.get("body")
                slug = slugify(title, allow_unicode=True)
                newBlog = Blog(title=title, body=body,
                               slug=slug, createdBy=user)
                try:
                    newBlog.save()
                    return render(request=request, template_name='Message.html', context={'user': user, 'message': "Your Blog Created Successfully !"})

                except:
                    raise Exception(
                        "Blog Title already exists!\nTitle must be unique !")
            else:
                raise Exception("Un-authenticated User")

        elif request.method == 'GET':
            return render(request=request, template_name='BlogPostForm.html', context={'user': request.user})
    except Exception as e:
        return render(request=request, template_name='errorPage.html', context={'ErrorMessage': str(e), 'status': status.HTTP_406_NOT_ACCEPTABLE})


@login_required(login_url='login')
@api_view(['GET', 'POST'])
def BlogEditView(request, slugId):
    userId = request.user.id
    try:
        blogInstance = Blog.objects.get(slug=slugId)
        if request.method == 'GET':
            if userId == blogInstance.createdBy.pk:
                serializedData = BlogSerializer(blogInstance)
                # print(serializedData.data)
                return render(request=request, template_name='BlogEditForm.html', context={'blog': serializedData.data, 'user': request.user})
            else:
                raise Exception("You are not authorized to perform this operation")
        if userId == blogInstance.createdBy.pk:
            if request.method == "POST":
                BlogObject = Blog.objects.get(slug=slugId)
                title = request.data.get("title", "")
                body = request.data.get("body", "")
                slug = slugify(title)
                BlogObject.title = title
                BlogObject.slug = slug
                BlogObject.body = body
                BlogObject.save()
                message = "Post has successfully edited !\n Thank You !"
                return render(request=request, template_name='Message.html', context={'message': message})

        else:
            raise Exception("You are not authorized to perform this operation")

    except Exception as e:
        message = str(e)
        return render(request=request, template_name='errorPage.html', context={'ErrorMessage': message, 'status': status.HTTP_401_UNAUTHORIZED})


@login_required(login_url='login')
@api_view(['GET'])
def PaginatedBlogListView(request, page=1):
    if request.method == 'GET':
        username = request.user
        queryset = Blog.objects.select_related(
            "createdBy").all().order_by('-createdOn')
        # page=request.GET.get('page',1)
        paginator = Paginator(queryset, 3)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(request=request, template_name="PaginatedBlogList.html", context={"blogs": posts, 'user': username})


@login_required(login_url='login')
@api_view(['GET'])
def DeleteBlogView(request, slugId):
    userId = request.user.id
    try:
        blogInstance = Blog.objects.get(slug=slugId)
        # print("=>>>",userId,blogInstance.createdBy,userId==blogInstance.createdBy,type(userId),type(blogInstance.createdBy))
        if userId == blogInstance.createdBy.pk:
            if request.method == "GET":
                blogInstance.delete()
                return render(request=request, template_name='Message.html', context={"message": "Deleted successfully"})
        else:
            raise Exception("You are not authorized to perform this operation")

    except Exception as e:
        return render(request=request, template_name='errorPage.html', context={'ErrorMessage': str(e), 'status': status.HTTP_401_UNAUTHORIZED})
