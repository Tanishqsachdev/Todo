from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import TodoForm
from .models import Todo
# Create your views here.
def home(request):
    return render(request,'todo_app/home.html')

def usersignup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            newuser = User.objects.create_user(username=username,password=password)
            newuser.save()
            login(request,newuser)
            return redirect('alltodos')
        else:
            return render(request,'todo_app/signup.html',{'form':form,'error':'Invalid Request.'})
    else:
        if request.user.is_authenticated:
            return redirect('alltodos')
        else:
            form = UserCreationForm()
            return render(request,'todo_app/signup.html',{'form':form})  

def userlogin(request):
    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is None:
            return render(request,'todo_app/login.html',{'form':AuthenticationForm(),'error':'Username or Password Incorrect'})
        login(request,user)
        return redirect('alltodos')
    else:
        return render(request,'todo_app/login.html',{'form':AuthenticationForm()})

def userlogout(request):
    if request.method =='POST':
        logout(request)
        return redirect('login')
    else:
        return redirect('home')
@login_required
def alltodos(request):
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,'todo_app/todos.html',{'todos':todos})

@login_required
def newtodo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('alltodos')
    else:
        return render(request,'todo_app/newtodo.html',{'form':TodoForm()})

@login_required
def viewtodo(request,id):
    todo = get_object_or_404(Todo,pk=id,user=request.user)
    form = TodoForm(instance=todo)
    if request.method == 'POST':
        form = TodoForm(request.POST,instance=todo)
        if form.is_valid():
            form.save()
            return redirect('alltodos')
        else:
           return render(request,'todo_app/viewtodo.html',{'form':form,'todo':todo,'error':'Something went wrong'}) 
        
    else:
        return render(request,'todo_app/viewtodo.html',{'form':form,'todo':todo})

@login_required
def deletetodo(request,id):
    todo = get_object_or_404(Todo,pk=id,user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect(alltodos)

@login_required
def completetodo(request,id):
    todo = get_object_or_404(Todo,pk=id,user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect(alltodos)
    else:
        return redirect(home)

@login_required
def completed(request):
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=False)
    return render(request,'todo_app/todos.html',{'todos':todos})