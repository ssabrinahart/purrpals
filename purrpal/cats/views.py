from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post
from datetime import datetime
from django.http import JsonResponse
from django.contrib import messages
from .models import Post, UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from .models import Post, UserProfile, Comment, Activity
from .forms import UserRegisterForm
from datetime import datetime
from django.db.models import Q


def home_view(request):
    posts = Post.objects.order_by('-created_at')
    feed = []
    if request.user.is_authenticated:
        feed = Activity.objects.filter(
            Q(user=request.user) |
            Q(target_post__author=request.user.username)
        ).order_by('-timestamp')[:10]
    return render(request, "cats/index.html", {
        "posts": posts,
        "feed": feed,
        "user": request.session.get("username"),
        "role": request.session.get("role")
    })

def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    if request.method == "POST" and request.user.is_authenticated:
        comment_text = request.POST.get("comment")
        if comment_text:
            comment = Comment.objects.create(post=post, user=request.user, text=comment_text)
            Activity.objects.create(user=request.user, action="comment", target_post=post)
            messages.success(request, "Comment posted!")
            return redirect("post_detail", post_id=post_id)
    return render(request, "cats/post_detail.html", {
        "post": post,
        "comments": comments,
        "role": request.session.get("role")
    })

def create_view(request):
    if not request.session.get("username"):
        return redirect("login")
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        author = request.session.get("username")
        post = Post(title=title, content=content, author=author)
        post.save()
        if request.user.is_authenticated:
            Activity.objects.create(user=request.user, action="create_post", target_post=post)
        messages.success(request, f"Post '{post.title}' was created successfully!")
        return redirect("home")
    return render(request, "cats/create.html")

def edit_post_view(request, post_id):
    if not request.session.get("username"):
        return redirect("login")
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        if request.user.is_authenticated:
            Activity.objects.create(user=request.user, action="edit_post", target_post=post)
        messages.info(request, f"Post '{post.title}' was updated successfully!")
        return redirect("post_detail", post_id=post.id)
    return render(request, "cats/edit.html", {"post": post})

def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_author = post.author == request.session.get("username")
    is_admin = request.session.get("role") == "admin"

    if request.method == "POST" and (is_author or is_admin):
        Activity.objects.create(user=request.user, action="delete_post", target_post=post)
        post.delete()
        messages.warning(request, f"Post '{post.title}' was deleted.")
    return redirect("home")



def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    activities = Activity.objects.filter(user=user).order_by('-timestamp')[:10]

    return render(request, 'cats/user_profile.html', {
        'user_obj': user,
        'profile': profile,
        'activities': activities
    })



def detail_view(request, id):
    cat = next((c for c in CatProfile if c.id == id), None)
    return render(request, 'cats/details.html', {'cat': cat})

def list_view(request):
    sort_by = request.GET.get('sort', 'created_at')
    if sort_by not in ['title', 'created_at', 'author']:
        sort_by = 'created_at'
    posts = Post.objects.order_by(sort_by)
    return render(request, 'cats/list.html', {
        'posts': posts,
        'sort_by': sort_by
    })



def logout_home_view(request):
    request.session.flush()
    posts = Post.objects.order_by('-created_at')
    return render(request, 'cats/homeLogOut.html', {'posts': posts})

USERS = {
    "user": {"password": "userpass", "role": "regular"},
    "admin": {"password": "adminpass", "role": "admin"},
}

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login as auth_login
from .models import UserProfile
from django.contrib.auth.models import User

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            request.session["username"] = user.username

            # ✅ Create a UserProfile if missing
            profile, created = UserProfile.objects.get_or_create(user=user)
            request.session["role"] = profile.role

            return redirect("home")
        else:
            return render(request, "cats/login.html", {"error": "Invalid credentials"})

    return render(request, "cats/login.html")


def vote_post(request, post_id):
    if request.method == "POST":
        action = request.POST.get("action")
        post = Post.objects.filter(id=post_id).first()

        if not post or action not in ["upvote", "downvote"]:
            return JsonResponse({"error": "Invalid request"}, status=400)

        if action == "upvote":
            post.votes += 1
        else:
            post.votes -= 1

        post.save()
        return JsonResponse({"votes": post.votes})

    return JsonResponse({"error": "Invalid method"}, status=405)

def live_search_view(request):
    query = request.GET.get("query", "")
    results = []

    if query:
        posts = Post.objects.filter(title__icontains=query)[:5]  # Top 5 results
        results = [{"id": p.id, "title": p.title, "author": p.author} for p in posts]

    return JsonResponse({"results": results})

def search_view(request):
    query = request.GET.get("query", "").strip().lower()
    results = []

    if query:
        matching_posts = Post.objects.filter(
            title__icontains=query
        ) | Post.objects.filter(content__icontains=query)

        results = [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "author": post.author,
                "created_at": post.created_at.strftime("%B %d, %Y at %I:%M %p"),
                "votes": post.votes,
            }
            for post in matching_posts
        ]

    return JsonResponse({"posts": results})

from .forms import UserRegisterForm
from django.contrib.auth import login
from .models import UserProfile

from django.db import IntegrityError

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Only create profile if one doesn't already exist
                if not hasattr(user, 'userprofile'):
                    UserProfile.objects.create(
                        user=user,
                        gender=form.cleaned_data['gender'],
                        role=form.cleaned_data['role']
                    )
                login(request, user)
                request.session["username"] = user.username
                request.session["role"] = "regular"
                messages.success(request, f"Welcome {user.username}, your account was created!")
                return redirect('home')
            except IntegrityError:
                messages.error(request, "A user profile already exists for this user.")
    else:
        form = UserRegisterForm()
    return render(request, 'cats/register.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

@login_required
def settings_view(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        profile.gender = request.POST.get("gender")

        if request.POST.get("password"):
            user.set_password(request.POST.get("password"))

        user.save()
        profile.save()
        messages.success(request, "Your profile has been updated.")
        return redirect("settings")

    all_users = UserProfile.objects.select_related("user").all() if profile.role == "admin" else []

    return render(request, "cats/settings.html", {
        "user": user,
        "profile": profile,
        "all_users": all_users,
    })


# Admin Role Changing Logic
from django.views.decorators.http import require_POST

@require_POST
@login_required
def change_user_role_view(request, user_id):
    if request.session.get("role") != "admin":
        return redirect("home")

    new_role = request.POST.get("role")
    target_user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(UserProfile, user=target_user)

    if new_role in ["admin", "regular"]:
        profile.role = new_role
        profile.save()
        messages.success(request, f"Updated {target_user.username}'s role to {new_role}.")

    return redirect("settings")


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def update_user_role(request, username):
    if request.method == "POST":
        admin_profile = UserProfile.objects.get(user=request.user)
        if admin_profile.role != "admin":
            return redirect("settings")

        if username == "admin":
            messages.error(request, "You cannot modify the default admin.")
            return redirect("settings")

        target_user = User.objects.get(username=username)
        target_profile = UserProfile.objects.get(user=target_user)
        target_profile.role = request.POST.get("role")
        target_profile.save()
        messages.info(request, f"{username}'s role updated to {target_profile.role}.")
    return redirect("settings")

def user_list_view(request):
    users = UserProfile.objects.select_related('user').all()
    return render(request, 'cats/users.html', {'users': users})


from django.views.decorators.http import require_POST

@require_POST
@login_required
def delete_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.user or request.session.get("role") == "admin":
        comment.delete()
        messages.warning(request, "Comment deleted.")
    return redirect("post_detail", post_id=comment.post.id)

from django.shortcuts import get_object_or_404
from .models import Comment

@login_required
def edit_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    profile = UserProfile.objects.get(user=request.user)

    # Permission check
    if comment.user != request.user and profile.role != "admin":
        messages.error(request, "You do not have permission to edit this comment.")
        return redirect("post_detail", post_id=comment.post.id)

    if request.method == "POST":
        new_text = request.POST.get("text")
        comment.text = new_text
        comment.save()
        messages.info(request, "Comment updated.")
        return redirect("post_detail", post_id=comment.post.id)

    return render(request, "cats/edit_comment.html", {
        "comment": comment
    })

