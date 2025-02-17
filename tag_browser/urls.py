from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:dsn>/<int:page>", views.tag_search, name='tag_search')
]