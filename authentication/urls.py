from django.urls import path

from . import views

appname = 'authentication'
urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    # path('follow', views.follow, name='follow'),
    # path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    # path('like-post', views.like_post, name='like-post'),
    # ex: /signup
    path('signup', views.signup, name='signup'),
    # ex: /signin
    path('signin', views.signin, name='signin'),
    # ex: /logout
    path('logout', views.logout, name='logout'),
]