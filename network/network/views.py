from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .utils import paginate, newPost, publish, getPost
from .models import User, Post, Likes, Follows

@csrf_exempt
def index(request):
    if request.method == "POST":
        publish(request)
        return HttpResponseRedirect("")
    else:
        try:
            user = User.objects.get(pk = request.user.id)
        except ObjectDoesNotExist:
            user = None
        all_posts = Post.objects.all().order_by("-time")
        pagination = paginate(all_posts)
        p = pagination.page(1)
        navigation = {
            "previous": p.has_previous(),
            "next": p.has_next(),
            "page_plus": 2
        }
        likes_filter = Likes.objects.filter(user = user)
        likes = [i.post.id for i in likes_filter]
        return render(request, "network/index.html", {
            "home": True,
            "form": newPost(auto_id=False),
            "posts": p.object_list,
            "user": user,
            "like": likes,
            "pagination": range(1, pagination.num_pages + 1),
            "navigate": navigation
        })


def feed(request, page):
    if page == 0 or page == 1:
        return index(request)
    else:
        all_posts = Post.objects.all().order_by("-time")
        pagination = paginate(all_posts)
        p = pagination.page(int(page))
        navigation = {
            "previous": p.has_previous(),
            "next": p.has_next(),
            "page_plus": page + 1,
            "page_minus": page -1
        }
        return render(request, "network/index.html", {
            "page": page,
            "home": False,
            "pagination": range(1, pagination.num_pages + 1),
            "posts": p.object_list,
            "navigate": navigation
        })


# Return selected profile
def profile(request, profile, page):
    profile = User.objects.get(pk = profile)
    try:
        user = User.objects.get(pk = request.user.id)
    except ObjectDoesNotExist:
        user = None

    is_follower = 0
    if request.user.is_authenticated:
        try:
            followCheck = Follows.objects.filter(source = user, follow = profile)
            if followCheck:
                is_follower = 1
        except ObjectDoesNotExist:
            pass

    profile_posts = Post.objects.filter(author = profile).order_by("-time")
    pagination = paginate(profile_posts)
    p = pagination.page(int(page))
    navigation = {
            "previous": p.has_previous(),
            "next": p.has_next(),
            "page_plus": page + 1,
            "page_minus": page -1
        }

    likes_filter = Likes.objects.filter(user = user)
    likes = [i.post.id for i in likes_filter]
    return render(request, "network/profile.html", {
        "profile": profile,
        "posts": p.object_list,
        "following": len(Follows.objects.filter(source = profile)),
        "followers": len(Follows.objects.filter(follow = profile)),
        "is_follower": is_follower,
        "like": likes,
        "pagination": range(1, pagination.num_pages + 1),
        "navigate": navigation
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# Filter posts
@login_required
def following(request, page):
    user = User.objects.get(pk = request.user.id)

    following_query = Follows.objects.filter(source = user)
    following_list = [i.follow for i in following_query]

    likes_filter = Likes.objects.filter(user = user)
    likes = [i.post.id for i in likes_filter]

    selected_posts = Post.objects.filter(author__in = following_list).order_by("-time")
    pagination = paginate(selected_posts)
    p = pagination.page(int(page))
    navigation = {
            "previous": p.has_previous(),
            "next": p.has_next(),
            "page_plus": page + 1,
            "page_minus": page -1
        }

    return render(request, "network/index.html", {
        "user": user,
        "posts": p.object_list,
        "like": likes,
        "navigate": navigation,
        "pagination": range(1, pagination.num_pages + 1),
        "following": True
    })


##############################################################
##### Fetch Calls ############################################
##############################################################

# Follow/Unfollow profile
@csrf_exempt
@login_required
def network(request):
    data = json.loads(request.body)

    source = User.objects.get(pk = data.get("user_id"))
    profile = User.objects.get(pk = data.get("profile_id"))
    
    f = Follows(source = source, follow = profile)
    if request.method == "POST":
        f.save()
        return JsonResponse({"message": "'Follow' model successfully changed"})
    elif request.method == "DELETE":
        g = Follows.objects.filter(source = source, follow = profile)
        g.delete()
        return JsonResponse({"message": "'Follow' model successfully changed"})
    else:
        return JsonResponse({"message": "An error has occurred while storing changes"})


# Like/Unlike post
@csrf_exempt
@login_required
def like(request):
    data = json.loads(request.body)
    if request.method == "PUT":

        action = data.get("action")

        post = Post.objects.get(pk = data.get("post_id"))
        user = User.objects.get(pk = data.get("user_id"))
        try:
            history = Likes.objects.get(user = user, post = post)                
            if action == 'unlike':
                history.delete()
                post.likes -= 1
            else:
                return JsonResponse({"message": "A user can only 'like' or 'unlike' a post once"}, status=404)      
        except Likes.DoesNotExist:
            if action == 'like':
                post.likes += 1
                f = Likes(user = user, post = post)
                f.save()
            else:
                return JsonResponse({"message": "A user can only 'like' or 'unlike' a post once"}, status=404)
        post.save()
        return JsonResponse({"message": "'Post' and 'Likes' models successfully changed"}, status=200)
    else:
        return JsonResponse({"message": "An error has occurred while making changes"}, status=400)


# Save post changes
@csrf_exempt
@login_required
def saveChanges(request):
    data = json.loads(request.body)
    if request.method == "PUT":
        try:
            post = Post.objects.get(pk = data.get("post_id"))
            post.body = data.get("post_body")
            post.save()
            return JsonResponse(post.serialize(), safe=False)
        except:
            return JsonResponse({"message": "An error occuried while making changes"}, status=400)
    else:
        return JsonResponse({"message": "An error has occurred while making changes"}, status=400)