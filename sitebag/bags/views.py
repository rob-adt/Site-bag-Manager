from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
# Add view to borrow a bag and update Borrowingtime
def borrow_bag(request, bag_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not authenticated"}, status=403)
    bag = get_object_or_404(Bag, pk=bag_id)
    employee = Employee.objects.filter(user=request.user).first()
    if not employee:
        return JsonResponse({"error": "Employee not found"}, status=404)
    borrowing_time = Borrowingtime.objects.filter(bag=bag).order_by("-start").first()
    if borrowing_time is None or borrowing_time.end is not None:
        borrowing_time = Borrowingtime.objects.create(
            bag=bag,
            member=employee,
            start=timezone.now(),
            end=None
        )
    else:
        borrowing_time.start = timezone.now()
        borrowing_time.member = employee
        borrowing_time.save()
    return JsonResponse({"success": True, "start": borrowing_time.start, "member": borrowing_time.member.user.username})
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



