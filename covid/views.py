from django.shortcuts import render
from . import data
# Create your views here.
def index(request):
    total = data.total
    totaltest = data.totaltest
    return render(request, 'covid/home.html', {'total':total, 'totaltest':totaltest})