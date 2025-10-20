from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Bag, Employee, Borrowingtime
import json
def return_bag(request, bag_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not authenticated"}, status=403)

    bag = get_object_or_404(Bag, pk=bag_id)
    employee = Employee.objects.filter(user=request.user).first()

    try:
        data = json.loads(request.body)
        contents = data.get("contents")
    except (json.JSONDecodeError, AttributeError):
        contents = None

    if not employee:
        return JsonResponse({"error": "Employee not found"}, status=404)

    borrowing_time_query = Borrowingtime.objects.filter(
        bag=bag, member=employee, end__isnull=True
    )
    if contents is not None:
        borrowing_time_query = borrowing_time_query.filter(contents=contents)

    borrowing_time = borrowing_time_query.order_by("-start").first()

    if borrowing_time:
        borrowing_time.end = timezone.now()
        borrowing_time.save()
        return JsonResponse({
            "success": True,
            "end": borrowing_time.end,
            "member": borrowing_time.member.user.username
        })
    else:
        return JsonResponse({"error": "No active borrowing found"}, status=404)


def borrow_bag(request, bag_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not authenticated"}, status=403)

    bag = get_object_or_404(Bag, pk=bag_id)
    employee = Employee.objects.filter(user=request.user).first()

    try:
        data = json.loads(request.body)
        contents = data.get("contents")
    except (json.JSONDecodeError, AttributeError):
        contents = None

    if not employee:
        return JsonResponse({"error": "Employee not found"}, status=404)

    borrowing_time = Borrowingtime.objects.filter(bag=bag).order_by("-start").first()

    if borrowing_time is None or borrowing_time.end is not None:
        borrowing_time = Borrowingtime.objects.create(
            bag=bag,
            member=employee,
            contents=contents,
            start=timezone.now(),
            end=None
        )
    else:
        borrowing_time.start = timezone.now()
        borrowing_time.member = employee
        borrowing_time.contents = contents
        borrowing_time.save()

    return JsonResponse({
        "success": True,
        "start": borrowing_time.start,
        "member": borrowing_time.member.user.username
    })


def index(request):
    bags = Bag.objects.all()

    for bag in bags:
        bag.last_borrowingtime = bag.borrowingtimes.order_by("-start").first()
        bag.end_borrowingtime = bag.borrowingtimes.order_by("-end").first()
        bag.being_used = bag.last_borrowingtime and bag.last_borrowingtime.end is None
    context = {
        "bags": bags,
        "authenticated": request.user.is_authenticated,
        "username": request.user.username,
        "buttoo": not bag.being_used if bags else True
    }

    return render(request, "sitebag/detail.html", context=context)


def addbg(request):
    if request.method == "POST":
        user_input = request.POST.get('user_input')
        messages.info(request, f"You typed: {user_input}")
        return redirect('index')
    return render(request, 'sitebag/bag.html')


def my_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)

    return render(request, "sitebag/detail.html", {"username": username})