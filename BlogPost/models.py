from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils.text import slugify
from django.urls import reverse


class Blog(models.Model):
    title=models.CharField(max_length=255,null=False)
    body=models.TextField(null=False)
    slug=models.SlugField(null=False,unique=True)
    createdOn=models.DateField(auto_now_add=True,null=False)
    createdBy=models.ForeignKey(User,on_delete=models.PROTECT,related_name='createdBy')

    def __str__(self):
        return self.title
    
    # to get the absolute path to the detailed Blog
    def get_absolute_url(self):
        return reverse("SigleBlog", kwargs={"slugId":self.slug})
        


    
    
    # def save(self,*args, **kwargs):
    #     self.slug=slugify(self.title)
    #     super().save(*args, **kwargs)
    # # models.SlugField(_(""))