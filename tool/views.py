from django.shortcuts import render
# from .models import Product

# Create your views here.
def browse(request):
    return render(request, "browse.html")

def compare(request):
    return render(request,"compare.html")