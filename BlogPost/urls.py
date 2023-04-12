from django.urls import path, include
from .views import DetailedBlogView,CreateNewBlogView,PaginatedBlogListView,DeleteBlogView,BlogEditView
# from .views import BlogListView
# from 


urlpatterns = [
    # path('blogs/',BlogListView,name='ListBlog'),
    path('blogs/',PaginatedBlogListView,name='ListBlog'),
    # path('blogs/',PaginatedBlogListView,name='defaultPaginatedListBlog'),
    path('blogs/page/<int:page>',PaginatedBlogListView,name='paginatedListBlog'),
    path('blogs/<slug:slugId>',DetailedBlogView,name='SigleBlog'),
    path('blogs/delete/<slug:slugId>',DeleteBlogView,name='DeleteBlog'),
    path('blogs/create/',CreateNewBlogView,name='CreateBlog'),
    path('blogs/edit/<slug:slugId>',BlogEditView,name='EditBlogView')
]
