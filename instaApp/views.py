from django.shortcuts import render
from .forms import UploadForm,ProfileUpdateForm, CommentForm
from .models import Image, Profile, Comments
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request,**kwargs):
    posts=Image.objects.all()[::-1]
    current_profile=Profile.objects.exclude(id=request.user.id)
    upload_form = UploadForm(request.POST, request.FILES)
    comment_form = CommentForm(request.POST, request.FILES)
    if upload_form.is_valid():
        upload = upload_form.save(commit=False)
        upload.user = request.user
        upload.save()
        return redirect('homePage')
    else:
        upload_form = UploadForm()
        comment_form = CommentForm()

    context ={
        'posts':posts,
        'upload_form':upload_form,
        'comment_form': comment_form,
        'user':current_profile,
    }
    return render (request, 'index.html',context)


def profile(request):
    current_user = request.user
    current_profile = Profile.objects.get(user=request.user)
    users_posts = Image.objects.filter(user=request.user)[::-1]
    update_form = ProfileUpdateForm(request.POST, instance=request.user)
    if request.method == "POST":
        if update_form.is_valid():
            update = update_form.save(commit=False)
            update.user = current_user
            update.save
            return HttpResponseRedirect(request.path_info)
    else:
        update_form = ProfileUpdateForm()
    context={
        'user':current_user,
        'profile':current_profile,
        'posts':users_posts,
        'form':update_form,
    }
    return render(request, 'profile.html', locals())

@login_required(login_url='/accounts/login/')
def search_user(request):
    if request.method == "GET":
        search_term = request.GET.get('search')
        message = '{}'.format(search_term)
        # searched_user = User.objects.filter(username=search_term).all()
        try:
            searched_user = User.objects.filter(username=search_term)
            searched_posts = Image.objects.filter(user=searched_user)[::-1]
        except DoesNotExist:
            raise Http404()
            return HttpResponseRedirect('homePage')
    context={
        'user':searched_user,
        'message':message,
        'posts':searched_posts
    }

    return render(request, 'searchres.html',context)
