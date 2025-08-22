from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from .models import Todo, Category
from .forms import TodoForm
# todos/views.py
from io import BytesIO
from django.http import HttpResponse
import openpyxl

def export_excel(request):
    # Example Excel export logic
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=todos.xlsx'
    
    # Create workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Todos'
    
    # Add some example data
    sheet.append(['ID', 'Title', 'Completed'])
    # You can loop through your todos
    # for todo in Todo.objects.all():
    #     sheet.append([todo.id, todo.title, todo.completed])
    
    workbook.save(response)
    return response


# Redirect to signup first
def home(request):
    if not request.user.is_authenticated:
        return redirect("register")
    return redirect("todo_list")

@login_required
def todo_list(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    priority_filter = request.GET.get('priority', '')

    todos = Todo.objects.filter(user=request.user).order_by('-created_at')

    if search_query:
        todos = todos.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
    if category_filter:
        todos = todos.filter(category__id=category_filter)
    if priority_filter:
        todos = todos.filter(priority=priority_filter)

    paginator = Paginator(todos, 5)
    page_number = request.GET.get('page')
    todos = paginator.get_page(page_number)

    categories = Category.objects.all()
    return render(request, 'todos/todo_list.html', {
        'todos': todos,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'priority_filter': priority_filter,
    })

@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todos/todo_form.html', {'form': form})

@login_required
def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/todo_form.html', {'form': form})

@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("todo_list")
    else:
        form = UserCreationForm()
    return render(request, "todos/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("todo_list")
    else:
        form = AuthenticationForm()
    return render(request, "todos/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def export_todos_excel(request):
    todos = Todo.objects.filter(user=request.user).order_by('-created_at')
    ...
    response = HttpResponse(
        content=openpyxl.writer.excel.save_virtual_workbook(wb),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="todos.xlsx"'
    return response


    # Header
    ws.append(["Title", "Description", "Priority", "Category", "Due Date", "Status"])

    for todo in todos:
        ws.append([
            todo.title,
            todo.description,
            todo.get_priority_display(),
            todo.category.name if todo.category else "",
            todo.due_date.strftime("%Y-%m-%d") if todo.due_date else "",
            "Completed" if todo.is_completed else "Pending"
        ])

    response = HttpResponse(
        content=openpyxl.writer.excel.save_virtual_workbook(wb),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="todos.xlsx"'
    return response
# other imports and views above...

@login_required
def todo_delete(request, pk):
    ...

def register(request):
    ...

def login_view(request):
    ...

def logout_view(request):
    ...

# <<< PASTE EXPORT FUNCTION HERE >>>
@login_required
def export_todos_excel(request):
    todos = Todo.objects.filter(user=request.user).order_by('-created_at')
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Todos"

    # Header
    ws.append(["Title", "Description", "Priority", "Category", "Due Date", "Status"])

    for todo in todos:
        ws.append([
            todo.title,
            todo.description,
            todo.get_priority_display(),
            todo.category.name if todo.category else "",
            todo.due_date.strftime("%Y-%m-%d") if todo.due_date else "",
            "Completed" if todo.is_completed else "Pending"
        ])

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="todos.xlsx"'
    return response
