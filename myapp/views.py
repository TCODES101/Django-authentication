from django.shortcuts import render,redirect
from django.contrib.auth.models import User
import re
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def index_view(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.info(request, 'Invalid credentials')
    return render(request, 'login.html')
    
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['passwordOne']
        password2 = request.POST['passwordTwo']
        pl = len(password)
        subject = 'Welcome to JFLATS'
       
        reg=re.compile('[@_!#$%^&*()~:/\|]')
        if username or email or password or password2 =='':
                messages.info(request, 'All fields must be filled')
                return redirect('signup')

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already used')
                return redirect('signup')
            
            elif(pl < 8):
                messages.info(request, 'password must be 8 or more characters')
                return redirect('signup')
            elif reg.search(password)==None:
                messages.info(request, 'password must contain special characters eg. @ # $')
                return redirect('signup')

            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                return redirect('index')

            

        else:
            messages.info(request, 'Password not the same')
            return redirect('signup')

    else:
        return render(request, 'signup.html')
def home_view(request):
    if request.user.is_authenticated:
        print(request.user.username)
        context={
            'name':request.user.username
        }
        return render(request,'home.html',context)
def logout_view(request):
    logout(request)
    return redirect('index')
  