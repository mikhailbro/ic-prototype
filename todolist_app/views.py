from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(request, ("New task successfully added!"))
        else: 
            messages.error(request, ("New task couldn't be saved!"))
        return redirect('todolist')
    else:
        # ALL TASKS:
        all_tasks = TaskList.objects.all()
        # Pagination:
        paginator_all_tasks = Paginator(all_tasks, 10)
        page = request.GET.get('pg')
        all_tasks = paginator_all_tasks.get_page(page)

        # MY TASKS:
        my_tasks = TaskList.objects.filter(owner=request.user)
        # Pagination:
        paginator_my_tasks = Paginator(my_tasks, 10)
        page = request.GET.get('pg')
        my_tasks = paginator_my_tasks.get_page(page)

        # return render(request, 'todolist.html', {'tasks': all_tasks})
        return render(request, 'todolist.html', {'tasks': my_tasks})
    
    # context = {
    #         'title_text': 'Task Mate - Todo List Manager',
    #         'welcome_text': 'Welcome to Todo List',
    #     }
    #return HttpResponse("Welcome to Todolist!")
        
        
@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.delete()
        messages.success(request, (f"Task '{task.task}' is successfully deleted!"))
    else:
        messages.error(request, ("Access restricted, you are NOT allowed!"))

    return redirect('todolist')


@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance = task)
        if form.is_valid():
            form.save()

        messages.success(request, (f"Task '{task.task}' is successfully updated!"))
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {'task_obj': task_obj})


@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.done = True
        task.save()
        messages.success(request, (f"Task '{task.task}' is successfully completed"))
    else:
        messages.error(request, ("Access restricted, you are NOT allowed!"))

    return redirect('todolist')


@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.done = False
        task.save()
        messages.success(request, (f"Task '{task.task}' is opened again"))
    else:
        messages.error(request, ("Access restricted, you are NOT allowed!"))

    return redirect('todolist')


@login_required
def contact(request):
    context = {
            'title_text': 'Task Mate - Contact Us',
            'contact_text': 'Welcome to Contact Us page',
        }
    return render(request, 'contact.html', context)


@login_required
def about(request):
    context = {
            'title_text': 'Task Mate - About Us',
            'about_text': 'Welcome to About Us page',
        }
    return render(request, 'about.html', context)


def index(request):
    context = {
            'title_text': 'Task Mate',
            'index_text': 'Welcome to Task Mate',
        }
    return render(request, 'index.html', context)
