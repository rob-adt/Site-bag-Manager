from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("borrow/<int:bag_id>/", views.borrow_bag, name="borrow_bag"),
]
