from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Blog_post
from django.contrib.auth.models import Group
#home
def home(request):
    post = Blog_post.objects.all()
    return render(request, 'home.html',{'posts':post})

#about
def about(request):
    return render(request, 'about.html')

#contact
def contact(request):
    return render (request, 'contact.html')

#dashboard
def dashboard(request):
    if request.user.is_authenticated:
     post = Blog_post.objects.all()
     user = request.user
     full_name = user.get_full_name()
     gps = user.groups.all()
     return render (request,'dashboard.html',{'posts' : post, 'fname':full_name,'groups':gps})
    else:
       return HttpResponseRedirect('/login/')
#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#signup
def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulation!! You have become an Author.")
            user = form.save()
            group = Group.objects.get(name = 'Author')
            user.groups.add(group)
    else:        
     form = SignupForm()
    return render (request,'signup.html', {'form':form})

#login
def user_login(request):
    if not request.user.is_authenticated:

     if request.method == "POST":
        form = LoginForm(request=request,data= request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username=uname,password = upass)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully !!")
                return HttpResponseRedirect('/dashboard')
            else:
                form = LoginForm()
     form = LoginForm()
     return render (request,'login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard')
    
#add new post
def add_post(request):
   if request.user.is_authenticated:
      if request.method == 'POST':
         form = PostForm(request.POST)
         if form.is_valid():
            title = form.cleaned_data['title']
            desc = form.cleaned_data['desc']
            pst = Blog_post(title=title,desc=desc)
            pst.save()
            form = PostForm()
      else:
         form = PostForm()      
      return render(request, 'addpost.html',{'form':form})
   else:
      return HttpResponseRedirect('/login/')    
   
#updata post
def edit_post(request,id):
   if request.user.is_authenticated:
      if request.method == 'POST':
         pi = Blog_post.objects.get(pk=id)
         form = PostForm(request.POST, instance=pi)
         if form.is_valid():
            form.save()
      else:
         pi = Blog_post.objects.get(pk=id)
         form = PostForm(instance=pi)      
      return render(request, 'updatepost.html',{'form':form})
   else:
      return HttpResponseRedirect('/login/')    
   
#deletepost
def delete_post(request,id):
   if request.user.is_authenticated:
      if request.method == 'POST':
         pi = Blog_post.objects.get(pk=id)
         pi.delete()
      return HttpResponseRedirect('/dashboard/')
   else:
        return HttpResponseRedirect('/login/')  