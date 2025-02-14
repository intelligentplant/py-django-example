from django.contrib import admin
from django.http import HttpResponse

# Register your models here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")