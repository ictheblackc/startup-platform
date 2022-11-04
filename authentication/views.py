from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Profile, Project, Post, Like, Comment


# Create your views here.
# in progress... don't touch
# class IndexView(generic.IndexView):
#     template_name = 'authentication/index.html'
#     context_object_name = 'profile'
#
#     def get_profile(self):
#         """Return """
#         return Profile.objects


@login_required(login_url='authentication:signin')
@csrf_exempt
def index(request):
    print("[=====================Index====================]")
    current_profile = request.user

    all_other_profiles = Profile.objects.exclude(username=current_profile)

    all_other_projects = Project.objects.exclude(profile=current_profile)

    all_posts = Post.objects.all()

    # TODO: suggest profiles
    suggested_profiles = all_other_profiles[:3]

    # TODO: suggest projects
    suggested_projects = all_other_projects[:3]

    # TODO: suggest posts
    suggested_posts = all_posts

    # Like
    suggested_posts_and_likes = []
    for suggested_post in suggested_posts:

        post_likes = Like.objects.filter(post=suggested_post).values("profile")

        amount_of_likes = 0
        is_profile_like = False

        if post_likes:
            amount_of_likes = post_likes.count()
            is_profile_like = post_likes.filter(profile=current_profile).exists()

        suggested_posts_and_likes.append({
            'post': suggested_post,
            'amount_of_likes': amount_of_likes,
            'is_profile_like': is_profile_like,
        })

    my_projects = Project.objects.filter(profile=current_profile)

    context = {
        'current_profile': current_profile,
        'suggested_profiles': suggested_profiles,
        'suggested_projects': suggested_projects,
        'suggested_posts_and_likes': suggested_posts_and_likes,
        'my_projects': my_projects,
    }
    print("[=====================Index====================]")
    return render(request, 'index.html', context)


@csrf_exempt
@login_required(login_url='authentication:signin')
def profile(request, username):
    current_profile = request.user
    profile = get_object_or_404(Profile, username=username)

    projects_of_profile = Project.objects.filter(profile=profile)
    posts_of_profile = Post.objects.filter(profile=profile)

    # Like
    posts_and_likes_of_profile = []
    for post in posts_of_profile:

        post_likes = Like.objects.filter(post=post).values("profile")

        amount_of_likes = 0
        is_profile_like = False

        if post_likes:
            amount_of_likes = post_likes.count()
            is_profile_like = post_likes.filter(profile=current_profile).exists()

        posts_and_likes_of_profile.append({
            'post': post,
            'amount_of_likes': amount_of_likes,
            'is_profile_like': is_profile_like,
        })

    is_follow = False

    quantities = {
        'posts': posts_of_profile.count(),
        'projects': projects_of_profile.count(),
        'followers': 0,
    }

    context = {
        'current_profile': current_profile,
        'profile': profile,
        'projects_of_profile': projects_of_profile,
        'posts_and_likes_of_profile': posts_and_likes_of_profile,
        'is_follow': is_follow,
        'quantities': quantities,
    }
    return render(request, 'profile.html', context)


@csrf_exempt
@login_required(login_url='authentication:signin')
def project(request, projectname):
    current_profile = request.user
    project = get_object_or_404(Project, projectname=projectname)

    context = {
        'current_profile': current_profile,
        'project': project,
    }
    return render(request, 'project.html', context)


@csrf_exempt
@login_required(login_url='authentication:signin')
def create_project(request):
    if request.method == 'POST':
        current_profile = request.user
        projectname = request.POST['projectname']
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES.get('image')

        if image is None:
            image = "blank-project-image.jpg"

        if projectname and Project.objects.filter(projectname=projectname).exists() is False:
            new_project = Project.objects.create(profile=current_profile, projectname=projectname, name=name,
                                                 description=description, image=image)
            new_project.save()

        # TODO: handle exception value

        return redirect('/')
    else:
        return redirect('/')


@csrf_exempt
@login_required(login_url='authentication:signin')
def create_post(request):
    if request.method == 'POST':
        current_profile = request.user
        projectname = request.POST['projectname']
        content = request.POST['content']
        image = request.FILES.get('image')

        if projectname:
            selected_project = Project.objects.get(projectname=projectname)

            if selected_project:
                new_post = Post.objects.create(profile=current_profile, project=selected_project, content=content,
                                               image=image)
                new_post.save()

        # TODO: handle exception value

        return redirect('/')
    else:
        return redirect('/')


@csrf_exempt
@login_required(login_url='authentication:signin')
def like_post(request):
    if request.method == 'POST':
        current_profile = request.user
        post_id = request.POST['post_id']

        if post_id:
            selected_post = Post.objects.get(pk=post_id)
            if selected_post:
                like = Like.objects.filter(profile=current_profile, post_id=post_id)
                if like.exists():
                    like.delete()
                else:
                    new_like = Like.objects.create(profile=current_profile, post=selected_post)
                    new_like.save()

        return redirect('/')
    else:
        return redirect('/')


@csrf_exempt
@login_required(login_url='authentication:signin')
def comment_post(request, post_id):
    current_profile = request.user
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':

        if request.POST['method'] == 'post':
            content = request.POST['content']

            if content:
                comment_of_post = Comment.objects.create(profile=current_profile, post=post, content=content)
                comment_of_post.save()

            return redirect(f'/comment-post/{post_id}')

        elif request.POST['method'] == 'delete':
            comment_id = request.POST['comment_id']

            comment_of_post = get_object_or_404(Comment, pk=comment_id)

            if comment_of_post.profile == current_profile or post.profile == current_profile:
                comment_of_post.delete()

            return redirect(f'/comment-post/{post_id}')

    elif request.method == "GET":

        comments_of_post = Comment.objects.filter(post=post)

        is_editor = post.profile == current_profile

        context = {
            'current_profile': current_profile,
            'post': post,
            'comments_of_post': comments_of_post,
            'is_editor': is_editor,
        }

        return render(request, 'comment_post.html', context)

    else:
        return redirect('/')


@csrf_exempt
@login_required(login_url='authentication:signin')
def profiles_list(request):
    current_profile = request.user

    if request.method == "POST":
        search = request.POST['search']
        profiles = Profile.objects.filter(username__contains=search)

    elif request.method == "GET":
        profiles = Profile.objects.all()
        search = ""

    context = {
        'current_profile': current_profile,
        'profiles': profiles,
        'search': search,
    }
    return render(request, 'profiles_list.html', context)


@csrf_exempt
@login_required(login_url='authentication:signin')
def projects_list(request):
    current_profile = request.user

    if request.method == "POST":
        search = request.POST['search']
        projects = Project.objects.filter(projectname__contains=search)

    elif request.method == "GET":
        projects = Project.objects.all()
        search = ""

    context = {
        'current_profile': current_profile,
        'projects': projects,
        'search': search,
    }

    return render(request, 'projects_list.html', context)



@csrf_exempt
@login_required(login_url='authentication:signin')
def profile_settings(request):
    current_profile = request.user

    if request.method == "POST":
        search = request.POST['search']
        projects = Project.objects.filter(projectname__contains=search)

    elif request.method == "GET":
        projects = Project.objects.all()
        search = ""

    context = {
        'current_profile': current_profile,
    }

    return render(request, 'profile_settings.html', context)



'''
@csrf_exempt
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_list,
                                          'suggestions_username_profile_list': suggestions_username_profile_list[:4]})





@csrf_exempt
@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html',
                  {'user_profile': user_profile, 'username_profile_list': username_profile_list})


@csrf_exempt
@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter is None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('/')

'''

'''
@csrf_exempt
@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/' + user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/' + user)
    else:
        return redirect('/')


@csrf_exempt
@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') is None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        else:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('index')
    return render(request, 'profile_settings.html', {'user_profile': user_profile})

'''


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if Profile.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('authentication:signup')
            elif Profile.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('authentication:signup')
            else:
                # Create Profile
                profile = Profile.objects.create_user(username=username, email=email, password=password)
                profile.save()

                # Login user in and redirect to index page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                return redirect('authentication:index')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('authentication:signup')

    else:
        return render(request, 'authentication/signup.html')


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('authentication:index')
        else:
            messages.info(request, 'Неверные данные')
            return redirect('authentication:signin')

    else:
        return render(request, 'authentication/signin.html')


@csrf_exempt
@login_required(login_url='authentication:signin')
def logout(request):
    auth.logout(request)
    return redirect('authentication:signin')
