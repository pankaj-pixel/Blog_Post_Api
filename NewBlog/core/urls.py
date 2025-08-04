from django.contrib import admin
from django.urls import path,include
from .views import logoutview, blogview,BlogById,blog_list_view,admin_blog_create_view,admin_blog_list_view,admin_blog_update_view,admin_blog_detail_view,admin_blog_delete_view,signupview,homepage,signinview
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    
    path('api/', blogview,name='BlogsView'),
    path('api/<int:id>', BlogById,name='Blogbyid'),
    #path('/login/', blogview,name='BlogsView')
    path('', blog_list_view, name='blog_list_view'),
    #path('blogs/<int:blog_id>/',blog_detail_view, name='blog_detail_view'),
    #path('', homepage, name='homepage'),
    path('list/', admin_blog_list_view, name='blog_list'),
    path('blogs/create/',admin_blog_create_view, name='admin_blog_create'),
    path('blogs/<int:blog_id>/', admin_blog_detail_view, name='blog_detail'),
    path('blogs/<int:blog_id>/edit/', admin_blog_update_view, name='admin_blog_update'),
    path('blogs/<int:blog_id>/delete/', admin_blog_delete_view, name='admin_blog_delete'),
    
    #authentication paths
    path('signup/', signupview,name='signup'),
    path('signin/',signinview,name='signin'),
    path('logut/',logoutview,name='logout')
    

   

]
urlpatterns += [
    path('api-token-auth/', obtain_auth_token)
]