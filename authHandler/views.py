from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout
from .serializer import UserCreationSerializer
from django.contrib.auth.models import User
from rest_framework import status
class LoginView(APIView):
    def get(self,request):
        return render(request=request, template_name='login.html')
    
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            authenticatedUser=authenticate(username=username,password=password)
            if authenticatedUser!=None:
                login(request=request,user=authenticatedUser)
                try:
                    referer=str(request.META['HTTP_REFERER'])
                    redirect_url=referer.split('next=')[1]
                    # print(redirect_url)
                    return redirect(to=redirect_url,request=request)
                except:
                    # return redirect(to='ListBlog')
                    return redirect(to='ListBlog')
                
            else:
                return render(request=request,template_name='errorPage.html',context={"ErrorMessage":"Authentication failed !",'status':status.HTTP_406_NOT_ACCEPTABLE})
        except Exception as e:
            return render(request=request,template_name='errorPage.html',context={'ErrorMessage':str(e),'status':status.HTTP_400_BAD_REQUEST})


class LogoutView(APIView):
    def get(self,request,*args, **kwargs):
        user=request.user.username
        logout(request=request)
        return render(request=request,template_name="logout.html",context={"message":"{} \n Have been successfully logged out.".format(user)}, status=status.HTTP_200_OK)


class UserCreationView(APIView):
    def get(self,request,*args, **kwargs):
        return render(request=request,template_name='CreateUser.html')
    def post(self,request,*args, **kwargs):
        username=request.POST.get("username",'')
        email=request.POST.get("email",'')
        password=request.POST.get("password",'')
        conformPassword=request.POST.get("conformPassword",'')
        if password==conformPassword:
            if username and email and password:
                newUser=User.objects.create_user(username=username,email=email,password=password)
                newUser.save()
                return redirect(to='login')
            else:
                message="Invalid Data !"
                return render(request=request,template_name='errorPage.html',context={'ErrorMessage':message,"status":status.HTTP_400_BAD_REQUEST})
        else:
            message="Password and conform password do not match !"
            return render(request=request,template_name='errorPage.html',context={'ErrorMessage':message,'status':status.HTTP_409_CONFLICT})