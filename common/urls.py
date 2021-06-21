from django.urls import path

from common.views import foo

urlpatterns = [
    path('foos/<int:pk>', foo.GetFoo.as_view()),
    path('foos', foo.CreateFoo.as_view()),
]
