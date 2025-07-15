from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from sqlER import ERGenerator, ERDiagram, TypeRankdir, Table

# Create your views here.

server = "localhost"
Name_database = "AdventureWorks2019"
username = "sa"
password = "test@123SA"
driver = "ODBC Driver 17 for SQL Server"
schema = "HumanResources"


def er(request):
    """Serve ER diagram as SVG."""
    diagram_gen = ERGenerator(
        driver=driver,
        server=server,
        database=Name_database,
        username=username,
        password=password,
    )
    svg_data = diagram_gen.render_diagrams()
    print("SVG Data:", svg_data)  # Debugging line to check SVG data
    return HttpResponse(
        svg_data,
        content_type="image/svg+xml",
        headers={"Content-Disposition": "inline; filename=er_diagram.svg"},
    )


def api1(request):
    return JsonResponse({"message": "Hello, World!"})


def http1(request):
    return HttpResponse("Hello, World!")


def api2(request):
    return JsonResponse({"api1": "api/api1"})


def http2(request):
    return HttpResponse("api/http1")
