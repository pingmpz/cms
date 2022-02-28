from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from dateutil import parser

def index(request):
    context = {
    }
    return render(request, 'index.html', context)
