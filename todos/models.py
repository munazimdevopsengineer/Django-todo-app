from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Todo(models.Model):
    PRIORITY_CHOICES = [
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def is_overdue(self):
        return self.due_date and self.due_date < timezone.now().date() and not self.is_completed

    def __str__(self):
        return self.title
