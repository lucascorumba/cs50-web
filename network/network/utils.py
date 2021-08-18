from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Follows, Likes, Post


# New Post form
class newPost(forms.Form):
    body = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'New Post...', 'class': 'form-control form-title'}))

# Return pagination
def paginate(all_posts):
    query = [post for post in all_posts]
    p = Paginator(query, 10)
    return p


# Place new post
@login_required
@csrf_exempt
def publish(request):
    data = newPost(request.POST)
    if data.is_valid():
        f = Post(author = User.objects.get(pk=request.user.id), body = data.cleaned_data["body"], likes = 0)
        f.save()
        return 0


# Get post's data
def getPost(request, post_id):
    post = Post.objects.get(pk = post_id)
    return JsonResponse(post.serialize(), safe=False)

