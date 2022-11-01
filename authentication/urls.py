from django.urls import path

from . import views

app_name = 'authentication'
urlpatterns = [
    # ex: /
    # in progress... don't touch
    #path('', views.IndexView.as_view(), name='index'),

    # pages
    path('', views.index, name='index'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('project/<str:projectname>', views.project, name='project'),
    path('comment-post/<str:post_id>', views.comment_post, name='comment_post'),
    path('profiles-list/', views.profiles_list, name='profiles_list'),
    path('projects-list/', views.projects_list, name='projects_list'),

    # actions
    path('create-project', views.create_project, name='create_project'),
    path('create-post', views.create_post, name='create_post'),
    path('like-post', views.like_post, name='like_post'),

    # authentication
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
]

# path('settings', views.settings, name='settings'),
# path('follow', views.follow, name='follow'),
# path('search', views.search, name='search'),