from django.shortcuts import render, redirect
from .models import UserId, MessageModel
from .forms import UserRegForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
import random
import string

# Create your views here.

def create_unique_id():
    return ''.join(random.choices(string.digits, k=8))

def create_object():
    id = create_unique_id()
    unique = False
    while not unique:
        try:
            user = UserId.objects.filter(uniqueId=id)
        except UserId.DoesNotExist:
            user = None
        if not user:
            unique = True
        else:
            id = create_unique_id()
    return id

def home(request):
    return render(request, 'Home.html')   

def userReg(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            userID = create_object()
            try:
                prof = UserId.objects.get(user=user)
            except UserId.DoesNotExist:
                prof = UserId.objects.create(user=user)
            prof.uniqueId = userID
            user.save()
            prof.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, "Successfully Registered as user")
            return redirect('msg')
        else:
            messages.success(request, "Try again")
            return render(request, 'Register.html', {'form': form})        
    else:
        form = UserRegForm()
    return render(request, 'Register.html', {'form': form})

def userLogin(request):
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            messages.success(request, "Successfully Login.")
            return redirect('msg')
        else:
            messages.warning(request,"Invalid Credentials")
            return redirect("userLogin")
    return render(request, 'Login.html', {'form': form})

def logout_view(request):
    logout(request)
    form = UserLoginForm()
    return render(request, 'Login.html', {'form': form})

@login_required(login_url="userLogin")
def msg(request):
    print("temppppp")
    temp=False
    if request.session.has_key('receiver'):
        temp = True
    msg = MessageModel.objects.filter(
            Q(sender = request.user) |
            Q(receiver = request.user)
        )
    identity = UserId.objects.get(user=request.user)
    uniqueUsers = UserId.objects.filter()
    unique = []
    for x in uniqueUsers:
        print(x.uniqueId)
        for y in msg:
            if (x.user == y.receiver and [x.user, x.uniqueId] not in unique and x.user != request.user) or (x.user == y.sender and [x.user, x.uniqueId] not in unique and x.user != request.user):
                print("YYYY",y, y.receiver)
                unique.append([x.user, x.uniqueId])
    # print(unique)
    context = {
        'msg': msg,
        'identity':identity,
        'temp':temp,
        'uniqueUsers':unique,
    }
    return render(request, 'chat.html', context )

@login_required(login_url="userLogin")
def idsent(request):
    id = request.POST.get('id')
    try:
        receiver = UserId.objects.get(Q(uniqueId=id))
    except UserId.DoesNotExist:
        receiver = None
    if receiver:
        u = receiver.user
        request.session['receiver'] = receiver.user.username
        request.session['id'] = receiver.user.id
        return redirect('msg')
    return redirect('msg')

@login_required(login_url="userLogin")
def idset(request,identity=None):
    if identity:
        try:
            receiver = UserId.objects.get(Q(uniqueId=identity))
        except UserId.DoesNotExist:
            receiver = None
        if receiver:
            # print(type(receiver.uniqueId), type(receiver.user.username))
            request.session['receiver'] = receiver.user.username
            request.session['id'] = receiver.user.id
            #request.session['receiver'] = receiver.user
            return redirect('msg')
    return redirect('msg')

@login_required(login_url="userLogin")
def msgSent(request):
    if request.method == "POST":  
        if request.POST.get('msg'):
            user = request.session['id']
            #print(user)
            userRec = User.objects.get(id=user)
            #print(userRec)
            msgModel = MessageModel.objects.create(sender=request.user, receiver = userRec)  
            msgModel.message = request.POST.get('msg')
            msgModel.save()
    return redirect("msg")