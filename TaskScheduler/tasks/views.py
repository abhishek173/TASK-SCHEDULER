from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . forms import TaskForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json

def login_page(request):

    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.info(request,"Invalid Username.")
            return redirect('/login/')
        else:
            user = authenticate(username = username,password=password)
            if user is None:
                messages.error(request,"Invalid Password..")
            else:
                login(request,user)
                return redirect('/')

    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect("/login/")


def register_page(request):
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, "Username already taken.")
            return redirect('/')


        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password)
        user.save()

        messages.info(request, "Account Created Successfully.")
        return redirect('/register/')

    return render(request,'register.html')

@login_required(login_url='/login/')
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    completed = request.GET.get('completed')
    sort_by = request.GET.get('sort_by')

    if completed == 'completed':
        tasks = tasks.filter(completed=True)
    elif completed == 'uncompleted':
        tasks = tasks.filter(completed = False)

    if sort_by == 'due_date':
        tasks = tasks.order_by('due_date')
    elif sort_by == 'completion_status':
        tasks = tasks.order_by('completed')

    return render(request,'task_list.html',{'tasks':tasks})

@login_required(login_url='/login/')
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user =  request.user
            task.save()
            return redirect('/')
        else:
            messages.info(request, "Please Enter Valid data.. ")

    else:
        form = TaskForm()
    return render(request,'task_create.html',{'form':form})


@login_required(login_url='/login/')
def task_update(request,id):
    task = Task.objects.get(id=id , user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TaskForm(instance=task)
    return render(request,'task_update.html',{'form':form})


@login_required(login_url='/login/')
@require_POST
def task_complete(request, id):
    try:
        task = Task.objects.get(id=id, user=request.user)
        data = json.loads(request.body)  # Parse the JSON body
        task.completed = data.get('completed', False)
        task.save()
        return JsonResponse({'status': 'success'})
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)


@login_required(login_url='/login/')
def task_delete(request,id):
    task = Task.objects.get(id=id,user=request.user)
    task.delete()
    return redirect('/')