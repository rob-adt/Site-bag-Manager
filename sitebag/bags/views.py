from django.shortcuts import render, redirect, get_object_or_404
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

    context["authenticated"] = request.user.is_authenticated
    context["username"]=request.user.username

    if bag.being_used == True:
        buttoo=False
    else:
        buttoo=True

    context["buttoo"]=buttoo


    return render(request, "sitebag/detail.html", context=context)
    
from django.contrib.auth import authenticate, login


def my_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    username="fish"
    if user is not None:
        login(request, user)
        
        # Redirect to a success page.
    else:
        # Return an 'invalid login' error message.
        ...
    return render(request,"sitebag/detail.html",username=username)


def borrowbagview(request, pk):
    bag = get_object_or_404(Bag, pk=pk)
    print(bag)
    username=request.user.username
    borrowing_time = Borrowingtime.objects.get(bag=bag)
    bagg=borrowing_time.start
    print(username)
    print(bagg)
    return redirect("index")