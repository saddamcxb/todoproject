from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, RegisterForm
# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "todo/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("task_list")
    return render(request, 'todo/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo/task_list.html', {"tasks": tasks})


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect("task_list")
    return render(request, 'todo/task_form.html', {"form": form})


@login_required
def task_update(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect("task_list")
    return render(request, 'todo/task_form.html', {"form": form})


@login_required
def task_delete(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    return render(request, 'todo/task_delete.html', {"task": task })

