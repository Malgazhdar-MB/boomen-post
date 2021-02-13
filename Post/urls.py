from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', Posts.as_view(), name='home'),
    path('login/', userLogin, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('category/<int:category_id>', PostsByCategory.as_view(), name = 'category'),
    path('post/<int:pk>', ShowPost.as_view(), name='show_post'),
    path('create_post/', CreatePost.as_view(), name='create_new'),
    path('contact/', contactMail, name='contact'),
]
