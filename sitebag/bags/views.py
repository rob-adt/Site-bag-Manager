from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from bags.models import Bag,Borrowingtime,Employee
import json
from django.views.decorators.csrf import csrf_exempt

def return_bag(request, bag_id):
    if not request.user.is_authenicated:
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

def add_content(request, cont):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not authenticated"}, status=403)
    
    
# Create new URL in urls.py for updating contents of a bag, and point it to the following view:
# Create view in views.py for updating the contents of a bag
#   bag = get_object_or_404(Bag, pk=bag_id)
#   bag.contents = "THis is my sample contents"
#   bag.save()
# Have your javascrpt function send a post / get request to the URL

def contentsave(request, bag_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not authenticated"}, status=403)
    
    bag = get_object_or_404(Bag, pk=bag_id)
    employee = Employee.objects.filter(user=request.user).first()

    bag.contents = request.body.decode()
    bag.save()
    return JsonResponse({
        "success": True,
        "contents_text": bag.contents
    })

def deletebag(request, bag_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not authenticated"}, status=403)
    
    bag = get_object_or_404(Bag, pk=bag_id)
    employee = Employee.objects.filter(user=request.user).first()

    bag.delete()
    
    return JsonResponse({
        "success": True,
        "contents_text": bag.contents
    })

    


    
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

    # Check if the bag is currently being used
    active_borrowing = Borrowingtime.objects.filter(bag=bag, end__isnull=True).first()

    if active_borrowing:
        return JsonResponse({"error": "Bag is currently in use"}, status=400)


    borrowing_time = Borrowingtime.objects.create(
        bag=bag,
        member=employee,
        start=timezone.now(),
        end=None
    )

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
        bag.being_used = (
            bag.last_borrowingtime is not None and bag.last_borrowingtime.end is None
        )
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





@csrf_exempt
def add_bag(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bag_name = data.get('bagName')
        if bag_name:
            new_bag = Bag(inbag=bag_name)
            new_bag.save()
            return JsonResponse({'message': f'Bag "{bag_name}" added successfully!'})
        return JsonResponse({'error': 'No bag name provided.'}, status=400)