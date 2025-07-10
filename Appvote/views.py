from django.shortcuts import render, redirect
from django.http import request
from Appvote.forms import adduserform
from django.contrib import messages
from .models import Category, CategoryItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views import View

# Create your views here. 
@login_required
def index(request):
    categories = Category.objects.all()
    return render(request, "index.html", {"categories": categories})

@login_required
def home(request, slug):
    category = Category.objects.get(slug=slug)
    categories = CategoryItem.objects.filter(category=category)

    msg = None

    if request.user.is_authenticated:
        if category.voters.filter(id=request.user.id).exists():
            msg = "voted"

    if request.method == "POST":
        selectedid = request.POST.get("vote")
        print(selectedid)

        item = CategoryItem.objects.get(id=selectedid)
        item.total_vote += 1 

        itemcategory = item.category
        itemcategory.total_vote += 1

        item.voters.add(request.user)
        itemcategory.voters.add(request.user)

        item.save() 
        itemcategory.save()

        return redirect('result', slug=category.slug)

    return render(request, "home.html", {"category": category, "Categories": categories, "msg": msg})

def register(request):
    submitted = False
    if request.method == "POST":

        form = adduserform(request.POST)
        if form.is_valid():
            form.save()
             
            messages.success(request, 'Registration Successful')

            return redirect('index')
    else:
        form = adduserform
        if 'submitted' in request.GET:
            submitted = True 
    
    return render(request, "registration/register.html", {'form':form, 'submitted':submitted})

# def logout(request):
#     return render(request, "registration/logout.html", {})

@login_required
def result(request, slug):
    category = Category.objects.get(slug=slug)
    items = CategoryItem.objects.filter(category=category)

    return render(request, "result.html", {"category": category, "items": items})

class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')  # or redirect to any other URL name


