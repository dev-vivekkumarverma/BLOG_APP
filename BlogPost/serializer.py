from rest_framework import serializers
from .models import Blog
from django.contrib.auth.models import User
from authHandler.serializer import UserSerializer

class BlogSerializer(serializers.ModelSerializer):
    blogUrl=serializers.SerializerMethodField(method_name='getBlogUrl',read_only=True)
    createdBy=UserSerializer()
    class Meta:
        model=Blog
        fields=['title','body','createdBy','slug','createdOn','blogUrl']
        # depth=1

    def getBlogUrl(self,obj):
        return obj.get_absolute_url()
