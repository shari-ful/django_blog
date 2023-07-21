
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),
    path('register', views.register_page, name='register'),
    path('profile/<str:pk>/', views.user_profile, name='user-profile'),
    path('blog/<str:pk>/', views.blog_items, name='blogitem'),
    path('createblog/', views.create_blog, name='create-blog'),
    path('updateblog/<str:pk>/', views.update_blog, name='update-blog'),
    path('deleteblog/<str:pk>/', views.delete_blog, name='delete-blog'),
    # path('updatecomment/<str:pk>/', views.update_comment, name='update-comment'),
    path('deletecomment/<str:pk>/', views.delete_comment, name='delete-comment'),

]