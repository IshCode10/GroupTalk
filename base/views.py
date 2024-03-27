from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Group, Topic, Message
from .forms import GroupForm, UserForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    
    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    groups = Group.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    
    topics = Topic.objects.all()
    group_count = groups.count()
    group_messages = Message.objects.filter(Q(group__topic__name__icontains=q))

    context = {'groups': groups, 'topics': topics, 'group_count': group_count, 'group_messages': group_messages}
    return render(request, 'base/home.html', context)

def group(request, pk):
   group = Group.objects.get(id=pk)
   group_messages = group.message_set.all()
   participants = group.participants.all()
   
   if request.method == 'POST':
       message = Message.objects.create(
           user= request.user,
           group= group,
           body= request.POST.get('body')
       )
       group.participants.add(request.user)
       return redirect('group', pk=group.id)
   
   context = {'group': group, 'group_messages': group_messages, 'participants': participants}
   return render(request, 'base/group.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    groups = user.group_set.all()
    group_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'groups': groups, 'group_messages': group_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createGroup(request):
    form = GroupForm()
    topics= Topic.objects.all()

    if request.method == 'POST':
        topic_name= request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Group.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form' : form, 'topics': topics}
    return render(request, 'base/group_form.html', context)

@login_required(login_url='login')
def updateGroup(request, pk):
    group = Group.objects.get(id=pk)
    form = GroupForm(instance=group)
    topics= Topic.objects.all()

    if request.user != group.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        topic_name= request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        group.name= request.POST.get('name')
        group.topic= topic
        group.description= request.POST.get('description')
        group.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'group': group}
    return render(request, 'base/group_form.html', context)

@login_required(login_url='login')
def deleteGroup(request, pk):
    group = Group.objects.get(id=pk)

    if request.user != group.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        group.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': group})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})
    
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance= user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})