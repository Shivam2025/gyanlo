from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post
# my pages.
def home (request):
    return render(request, 'home/home.html')

def about (request):
    return render(request, 'home/about.html')

def contact (request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        print(name,email,phone,content)

        if len(name)==''or len(email)<5 or len(phone)<10 or len(content)=='':
            messages.error(request, "Please fill the forms correctly")
        else:
            contact=Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request, "your message has been sent successfully")
    return render(request, 'home/contact.html')
    
def search(request):
    #allPosts=Post.objects.all()
    query=request.GET['query']
    if len(query)>301:
        allPosts=Post.objects.none()
    else:
        allPostsTitle=Post.objects.filter(title__icontains=query)
        allPostsContent=Post.objects.filter(content__icontains=query)
        allPosts=allPostsTitle.union(allPostsContent)
    if allPosts.count()==0:
        messages.warning(request,'No documents matched your query, Please refine your search')
    params={'allPosts':allPosts,'query':query}
    return render(request,'home/search.html',params)
    #return HttpResponse('This is search')
#authentication APIs.

def handleSignup(request):
    if request.method =='POST':
        #Get the post parametres
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']


        #Check for errenous input
        if len(username)>15:
            messages.error(request,"Username should be under 15 characters")
            return redirect('home')
        if not username.isalnum():
            messages.error(request,"Username should only contain letters and numbers")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request,"Passwords do not match")
            return redirect('home')
        #Create the user
        myuser=User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request,"Your gyanlo account has been created successfully")
        return redirect('home')
    else:
        return HttpResponse('404-Not Found')

def handleLogin(request):
    if request.method =='POST':
        #Get the post parametres
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In successfully")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials, please try again to get logged in")
            return redirect('home')
    return HttpResponse('Error 404 - Not Found')
def handleLogout(request):
    logout(request)
    messages.success(request, "Logged Out successfully")
    return redirect('home')
    
