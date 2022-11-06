from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Profile, Project, Post, Like, Comment, Followers, Teammates


@login_required(login_url='authentication:signin')
@csrf_exempt
def index(request):
    current_profile = request.user

    is_index_page = request.get_full_path() == "/" if True else False

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
        'is_index_page': is_index_page,
    }
    return render(request, 'index.html', context)


@csrf_exempt
@login_required(login_url='authentication:signin')
def profile(request, username):
    current_profile = request.user
    profile = get_object_or_404(Profile, username=username)

    projects_of_profile = Project.objects.filter(profile=profile)
    posts_of_profile = Post.objects.filter(profile=profile)
    followers_of_profile = Followers.objects.filter(profile=profile)

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

    is_follow = Followers.objects.filter(profile=profile, follower=current_profile).exists() if True else False

    quantities = {
        'posts': posts_of_profile.count(),
        'projects': projects_of_profile.count(),
        'followers': followers_of_profile.count(),
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

    is_teammate = Teammates.objects.filter(project=project, teammate=current_profile).exists() if True else False

    context = {
        'current_profile': current_profile,
        'project': project,
        'is_teammate': is_teammate,
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
            selected_project = get_object_or_404(Project, projectname=projectname)

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
            selected_post = get_object_or_404(Post, pk=post_id)
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

    profile = get_object_or_404(Profile, username=current_profile)

    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        avatar = request.FILES.get('avatar')
        background_profile_photo = request.FILES.get('background_profile_photo')
        bio = request.POST['bio']
        gender = request.POST['gender']
        date_of_birth = request.POST['date_of_birth']
        website = request.POST['website']
        country_id = request.POST['country_id']
        city_id = request.POST['city_id']
        citizenship = request.POST['citizenship']
        tin = request.POST['tin']
        address = request.POST['address']
        university = request.POST['university']
        speciality = request.POST['speciality']
        ending_year = request.POST['ending_year']
        employment_id = request.POST['employment_id']
        skills = request.POST['skills']
        work_experience = request.POST['work_experience']
        achievements = request.POST['achievements']
        hackathons = request.POST['hackathons']

        profile.name = name
        profile.phone = phone

        if avatar is not None:
            profile.avatar = avatar

        if background_profile_photo is not None:
            profile.background_profile_photo = background_profile_photo

        profile.gender = gender
        profile.bio = bio
        profile.date_of_birth = date_of_birth
        profile.website = website
        profile.citizenship = citizenship
        profile.address = address
        profile.university = university
        profile.speciality = speciality
        profile.ending_year = ending_year
        profile.skills = skills
        profile.achievements = achievements

        # profile.work_experience = work_experience
        # profile.hackathons = hackathons

        # profile.tin = tin
        # profile.employment_id = employment_id
        # profile.country_id = country_id
        # profile.city_id = city_id

        profile.save()

    elif request.method == "GET":
        pass

    context = {
        'current_profile': current_profile,
        'profile': profile,
    }

    return render(request, 'profile_settings.html', context)


@csrf_exempt
@login_required(login_url='authentication:signin')
def follow(request, username):
    if request.method == 'POST':

        current_profile = request.user
        profile = get_object_or_404(Profile, username=username)

        method = request.POST['method']

        if method == "post" and Followers.objects.filter(profile=profile, follower=current_profile).exists() is False:
            follower = Followers.objects.create(profile=profile, follower=current_profile)
            follower.save()
        elif method == "delete" and Followers.objects.filter(profile=profile,
                                                             follower=current_profile).exists() is True:
            follower = get_object_or_404(Followers, profile=profile, follower=current_profile)
            follower.delete()

    return redirect(f'/profile/{username}')


@csrf_exempt
@login_required(login_url='authentication:signin')
def join(request, projectname):
    if request.method == 'POST':

        current_profile = request.user
        project = get_object_or_404(Project, projectname=projectname)

        method = request.POST['method']

        if method == "post" and Teammates.objects.filter(project=project, teammate=current_profile).exists() is False:
            teammate = Teammates.objects.create(project=project, teammate=current_profile)
            teammate.save()
        elif method == "delete" and Teammates.objects.filter(project=project,
                                                             teammate=current_profile).exists() is True:
            teammate = get_object_or_404(Teammates, project=project, teammate=current_profile)
            teammate.delete()

    return redirect(f'/project/{projectname}')


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
            messages.info(request, 'Пароли не совпадают')
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
