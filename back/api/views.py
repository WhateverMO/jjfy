from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# Create your views here.


def api1(request):
    return JsonResponse({"message": "Hello, World!"})


def http1(request):
    return HttpResponse("Hello, World!")


def api2(request):
    return JsonResponse({"api1": "api/api1"})


def http2(request):
    return HttpResponse("api/http1")
