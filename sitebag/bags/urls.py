from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("borrow/<int:pk>", views.borrowbagview, name="borrow_bag"),
]
