from login_app.models import User, Post, Comment
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib import messages
import bcrypt

# view to load homepage

def login(request):
    return render(request, 'login.html')

def login_process(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
    else:
        messages.error(request, "Invalid Email")
        return redirect('/')

    if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
        request.session['userid'] = logged_user.id
        return redirect('/wall')
    else:
        messages.error(request, 'Incorrect password')
        return redirect('/')

def register(request):
    return render(request, 'register.html')

def register_process(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print(pw_hash)
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash.decode())
        messages.success(request, "Successfully registered!")
        return redirect('/')

def wall(request):
    context = {
        "user": User.objects.get(id = request.session['userid']),
        "posts": Post.objects.all(),
        "comments": Comment.objects.all()
    }
    return render(request, 'wall.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def add_post(request):
    print('hell')
    Post.objects.create(post_message=request.POST['post-message-text'], user=User.objects.get(id=request.session['userid']))
    return redirect('/wall')

def add_comment(request):
    print(request.POST['post-id'])
    Comment.objects.create(comment_message=request.POST['comment-message-text'], post = Post.objects.get(id=request.POST['post-id']),
    user = User.objects.get(id=request.POST['user-id']))
    return redirect('/wall')