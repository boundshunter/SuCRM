from django.shortcuts import render, redirect, HttpResponse

# Create your views here.


def index(request):
    return render(request, 'index.html')


def customer_list(request):
    return render(request, 'sales/customers.html')