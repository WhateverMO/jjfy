from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponse
from sqlER import ERGenerator, ERDiagram, TypeRankdir, Table

# Create your views here.

server = "localhost"
Name_database = "AdventureWorks2019"
username = "sa"
password = "test@123SA"
driver = "ODBC Driver 17 for SQL Server"
schema = "HumanResources"


def get_table_names(request: HttpRequest) -> JsonResponse:
    erd: ERDiagram = ERGenerator(
        driver=driver,
        server=server,
        database=Name_database,
        username=username,
        password=password,
    ).diagram
    return JsonResponse(
        {
            "table_names": erd.get_table_names(),
        }
    )


def get_view_names(request: HttpRequest) -> JsonResponse:
    erd: ERDiagram = ERGenerator(
        driver=driver,
        server=server,
        database=Name_database,
        username=username,
        password=password,
    ).diagram
    return JsonResponse(
        {
            "view_names": erd.get_view_names(),
        }
    )


def get_all_relations(request: HttpRequest) -> JsonResponse:
    erd: ERDiagram = ERGenerator(
        driver=driver,
        server=server,
        database=Name_database,
        username=username,
        password=password,
        reasoning_FK=True,
    ).diagram
    return JsonResponse(
        {
            "view_names": erd.get_all_relations(),
        }
    )


def get_table(request: HttpRequest) -> JsonResponse:  # TODO: unfinished
    erd: ERDiagram = ERGenerator(
        driver=driver,
        server=server,
        database=Name_database,
        username=username,
        password=password,
    ).diagram
    table: dict = erd.get_table("Employee").get_dict()
    return JsonResponse(table)


def er(request: HttpRequest) -> HttpResponse:
    """Serve ER diagram as SVG."""
    diagram_gen = ERGenerator(
        driver=driver,
        server=server,
        database=Name_database,
        username=username,
        password=password,
    )
    svg_data = diagram_gen.render_diagrams()
    return HttpResponse(
        svg_data,
        content_type="image/svg+xml",
        headers={"Content-Disposition": "inline; filename=er_diagram.svg"},
    )


def er1test(request: HttpRequest) -> HttpResponse:
    """Serve ER diagram as SVG."""
    diagram_gen = ERGenerator(
        driver=driver,
        server=server,
        database=Name_database,
        username=username,
        password=password,
    )
    svg_data = diagram_gen.render_diagrams(
        render_tables=["Employee", "vEmployee", "ProductPhoto"], render_related=True
    )
    return HttpResponse(
        svg_data,
        content_type="image/svg+xml",
        headers={"Content-Disposition": "inline; filename=er_diagram.svg"},
    )


def er2test(request: HttpRequest) -> HttpResponse:
    """Serve ER diagram as SVG."""
    diagram_gen = ERGenerator(
        driver=driver,
        server=server,
        database=Name_database,
        username=username,
        password=password,
    )
    svg_data = diagram_gen.render_diagrams(
        render_tables=["Employee", "vEmployee", "ProductPhoto"], render_related=False
    )
    return HttpResponse(
        svg_data,
        content_type="image/svg+xml",
        headers={"Content-Disposition": "inline; filename=er_diagram.svg"},
    )


def erfit(request: HttpRequest) -> HttpResponse:
    """Serve ER diagram as SVG."""
    diagram_gen = ERGenerator(
        driver=driver,
        server=server,
        database=Name_database,
        username=username,
        password=password,
    )
    svg_data = diagram_gen.render_diagrams()
    # return a width height of 100% svg fit to the container
    html = f"""
    <html>
      <head>
        <style>
          html, body {{
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
          }}
          .svg-container {{
            width: 100vw;
            height: 100vh;
          }}
          .svg-container svg {{
            width: 100%;
            height: 100%;
            display: block;
          }}
        </style>
      </head>
      <body>
        <div class="svg-container">
          {svg_data}
        </div>
      </body>
    </html>
    """
    return HttpResponse(html, content_type="text/html")


def er1testfit(request: HttpRequest) -> HttpResponse:
    """Serve ER diagram as SVG."""
    diagram_gen = ERGenerator(
        driver=driver,
        server=server,
        database=Name_database,
        username=username,
        password=password,
    )
    svg_data = diagram_gen.render_diagrams(
        render_tables=["Employee", "vEmployee", "ProductPhoto"], render_related=True
    )
    html = f"""
    <html>
      <head>
        <style>
          html, body {{
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
          }}
          .svg-container {{
            width: 100vw;
            height: 100vh;
          }}
          .svg-container svg {{
            width: 100%;
            height: 100%;
            display: block;
          }}
        </style>
      </head>
      <body>
        <div class="svg-container">
          {svg_data}
        </div>
      </body>
    </html>
    """
    return HttpResponse(html, content_type="text/html")


def er2testfit(request: HttpRequest) -> HttpResponse:
    """Serve ER diagram as SVG."""
    diagram_gen = ERGenerator(
        driver=driver,
        server=server,
        database=Name_database,
        username=username,
        password=password,
    )
    svg_data = diagram_gen.render_diagrams(
        render_tables=["Employee", "vEmployee", "ProductPhoto"], render_related=False
    )
    html = f"""
    <html>
      <head>
        <style>
          html, body {{
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
          }}
          .svg-container {{
            width: 100vw;
            height: 100vh;
          }}
          .svg-container svg {{
            width: 100%;
            height: 100%;
            display: block;
          }}
        </style>
      </head>
      <body>
        <div class="svg-container">
          {svg_data}
        </div>
      </body>
    </html>
    """
    return HttpResponse(html, content_type="text/html")


def api1(request):
    return JsonResponse({"message": "Hello, World!"})


def http1(request):
    return HttpResponse("Hello, World!")


def api2(request):
    return JsonResponse({"api1": "api/api1"})


def http2(request):
    return HttpResponse("api/http1")
