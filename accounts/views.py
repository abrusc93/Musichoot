import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import RegistrationForm, UserEditForm, UserProfileForm
from .models import Profile
from django.shortcuts import get_object_or_404
from .models import *
from django.core.exceptions import ObjectDoesNotExist


def avatar(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        avatar = Profile.objects.filter(user=user)
        context = {
            "avatar": avatar,
        }
        return context
    else:
        return {
            'NotLoggedIn': User.objects.none()}

def accounts_register(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.save()
            return redirect("/recommender/home")
    else:
        registerForm = RegistrationForm()
    return render(request, 'registration/register.html', {'form': registerForm})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)

        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    return render(request,
                  'accounts/update.html',
                  {'user_form': user_form, 'profile_form': profile_form})

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        return redirect('accounts:login')

    return render(request, 'accounts/delete.html')

def friendlist(request):
    userfriends = FriendList.objects.filter(user=request.user)
    friends = []
    if userfriends:
        for userfriend in userfriends:
            friends = userfriend.friends.all()
    friendrequest = FriendRequest.objects.filter(sender=request.user)
    recfriendrequest = FriendRequest.objects.filter(receiver=request.user)
    return render(request, 'accounts/friendlist.html', {'friends': friends, 'friendrequest':friendrequest, 'recfriendrequest':recfriendrequest})

@login_required
def profile(request):
    userfriends = FriendList.objects.filter(user=request.user)
    friends = []
    if userfriends:
        for userfriend in userfriends:
            friends = userfriend.friends.all()

    numfriends = len(friends)
    return render(request,
                  'accounts/profile.html',
                  {'section': 'profile',
                   'friends': friends,
                   'numfriends': numfriends})


def sentrequest(request, username):
    friendrequest = FriendRequest.objects.filter(sender=request.user)
    user = get_object_or_404(User, username=username)
    newfriend = 1
    for req in friendrequest:
        if req.receiver == user:
            newfriend = 0
    if newfriend:
        newfriendrequest = FriendRequest()
        newfriendrequest.sender = request.user
        newfriendrequest.receiver = user
        newfriendrequest.save()
    userfriends = FriendList.objects.filter(user=request.user)
    friends = []
    if userfriends:
        for userfriend in userfriends:
            friends = userfriend.friends.all()
    friendrequest = FriendRequest.objects.filter(sender=request.user)
    recfriendrequest = FriendRequest.objects.filter(receiver=request.user)
    return render(request, 'accounts/friendlist.html', {'friends': friends, 'friendrequest':friendrequest, 'recfriendrequest':recfriendrequest})

def lookup_friendslist(user):
    try:
        friendlist = FriendList.objects.get(user=user)
        return friendlist
    except ObjectDoesNotExist:
        return None

def accept(request, username):
    userid = User.objects.get(username=username)
    friend_request = FriendRequest.objects.get(sender= userid, receiver=request.user)
    if friend_request:
        friend_request.delete()

    userfriends = lookup_friendslist(request.user)
    if not userfriends:
        userfriends = FriendList()
        userfriends.user = request.user
        userfriends.save()
    userfriends.friends.add(userid)
    userfriends.save()

    otheruserfriends = lookup_friendslist(userid)
    if not otheruserfriends:
        otheruserfriends = FriendList()
        otheruserfriends.user = userid
        otheruserfriends.save()
    otheruserfriends.friends.add(request.user)
    otheruserfriends.save()

    userfriends = FriendList.objects.filter(user=request.user)
    friends = []
    if userfriends:
        for userfriend in userfriends:
            friends = userfriend.friends.all()
    friendrequest = FriendRequest.objects.filter(sender=request.user)
    recfriendrequest = FriendRequest.objects.filter(receiver=request.user)
    return render(request, 'accounts/friendlist.html', {'friends': friends, 'friendrequest':friendrequest, 'recfriendrequest':recfriendrequest})


def decline(request, username):
    userid = User.objects.get(username=username)
    friend_request = FriendRequest.objects.get(sender= userid, receiver=request.user)
    if friend_request:
        friend_request.delete()
    userfriends = FriendList.objects.filter(user=request.user)
    friends = []
    if userfriends:
        for userfriend in userfriends:
            friends = userfriend.friends.all()
    friendrequest = FriendRequest.objects.filter(sender=request.user)
    recfriendrequest = FriendRequest.objects.filter(receiver=request.user)
    return render(request, 'accounts/friendlist.html', {'friends': friends, 'friendrequest':friendrequest, 'recfriendrequest':recfriendrequest})


def cancel(request, username):
    userid = User.objects.get(username=username)
    friend_request = FriendRequest.objects.get(sender= request.user, receiver=userid)
    if friend_request:
        friend_request.delete()
    userfriends = FriendList.objects.filter(user=request.user)
    friends = []
    if userfriends:
        for userfriend in userfriends:
            friends = userfriend.friends.all()
    friendrequest = FriendRequest.objects.filter(sender=request.user)
    recfriendrequest = FriendRequest.objects.filter(receiver=request.user)
    return render(request, 'accounts/friendlist.html', {'friends': friends, 'friendrequest':friendrequest, 'recfriendrequest':recfriendrequest})



