from django.urls import path

from .views import foo

urlpatterns = [
    path('foos/<int:pk>', foo.GetFoo.as_view()),
    path('foos', foo.CreateFoo.as_view()),
]
