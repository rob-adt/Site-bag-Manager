from django.shortcuts import render
from django.http import HttpResponse
from .models import Bag,Employee,Borrowingtime
from django.db.models import Max

# Create your views here.

def index(request):
    # context = {"bags":Bag.objects.all().annotate(Max("borrowingtimes__start"))}
    context = {"bags":Bag.objects.all()}
    
    for bag in context["bags"]:
        bag.last_borrowingtime = bag.borrowingtimes.order_by("-start").first()
        bag.end_borrowingtime = bag.borrowingtimes.order_by("-end").first()

        if bag.last_borrowingtime is None:
            bag.being_used = False
        else:
            bag.being_used = bag.last_borrowingtime.end is None
   
    return render(request, "sitebag/detail.html", context=context)
    
from django.contrib.auth import authenticate, login


def my_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
    else:
        # Return an 'invalid login' error message.
        ...