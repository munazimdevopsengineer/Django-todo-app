from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator

from .models import Todo
from .forms import TodoForm

def home(request: HttpRequest) -> HttpResponse:
    # Handle new todo creation
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TodoForm()

    # --- 🔍 Search Integration ---
    query = request.GET.get('q', '')  # get search keyword
    todos = Todo.objects.all().order_by('-created_at')
    if query:
        todos = todos.filter(title__icontains=query)

    # --- 📄 Pagination ---
    paginator = Paginator(todos, 5)  # 5 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'todos/index.html',
        {
            'form': form,
            'todos': page_obj,  # send paginated todos
            'query': query,     # send search keyword back
        }
    )

def toggle(request: HttpRequest, pk: int) -> HttpResponse:
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('home')

def delete(request: HttpRequest, pk: int) -> HttpResponse:
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect('home')
