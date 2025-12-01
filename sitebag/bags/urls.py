from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("borrow/<int:bag_id>/", views.borrow_bag, name="borrow_bag"),
    path("return/<int:bag_id>/", views.return_bag, name="return_bag"),
    path('add-bag/', views.add_bag, name='add_bag'),
    path('addcontent/', views.add_content, name='addcontent'),
    path('contentsave/<int:bag_id>/',views.contentsave, name="contentsave"),
    path('deletebag/<int:bag_id>/',views.deletebag, name="deletebag"),
]

