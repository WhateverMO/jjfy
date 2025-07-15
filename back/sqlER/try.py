import itertools
import urllib.parse
from typing import Type

from flask import Flask, Response
from flask.sansio.scaffold import F

from ERDiagram import ERGenerator
from ERDiagram.ERDiagram import TypeRankdir

server = "localhost"
Name_database = "AdventureWorks2019"
username = "sa"
password = "test@123SA"
driver = "ODBC Driver 17 for SQL Server"
schema = "HumanResources"


app = Flask(__name__)


@app.route("/er")
def serve_er_diagram() -> Response:
    """Serve ER diagram as SVG."""
    diagram_gen = ERGenerator(
        driver=driver,
        server=server,
        database=Name_database,
        username=username,
        password=password,
    )
    svg_data = diagram_gen.render_diagrams()
    return Response(
        svg_data,
        mimetype="image/svg+xml",
        headers={"Content-Disposition": "inline; filename=er_diagram.svg"},
    )


@app.route("/")
def serve() -> Response:
    """Serve ER diagram as SVG."""
    diagram_gen = ERGenerator(
        driver=driver,
        server=server,
        database=Name_database,
        username=username,
        password=password,
    )
    svg_data = urllib.parse.quote(diagram_gen.render_diagrams().decode("utf-8"))
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ER Diagram</title>
        <style>
            body {{ margin: 0; padding: 0; }}
            .svg-container {{
                width: 100vw;
                height: 100vh;
                overflow: auto;
            }}
            object, iframe {{
                width: 100%;
                height: 100vh;
                border: none;
            }}
        </style>
    </head>
    <body>
        <div class="svg-container">
            <object data="data:image/svg+xml;utf8,{svg_data}" type="image/svg+xml"></object>
        </div>
    </body>
    </html>
    """
    return Response(html, mimetype="text/html")


if __name__ == "__main__":
    # app.run(port=5000)
    Name_databases = ["AdventureWorks2019", "AdventureWorks2022"]
    Render_tables = [
        ["Employee"],
        ["vEmployee"],
        ["ProductPhoto"],
        ["vEmployee", "ProductPhoto"],
        ["Employee", "ProductPhoto"],
        ["Employee", "vEmployee"],
        ["Employee", "vEmployee", "ProductPhoto"],
    ]

    first: bool = True
    Render_related = [True, False]
    # test all combinations of render_tables and render_related
    for name_database, render_tables, render_related in itertools.product(
        Name_databases, Render_tables, Render_related
    ):
        render_tables = render_tables.copy()
        print()
        file_name = (
            name_database
            + "_"
            + "_".join(render_tables)
            + "_"
            + ("related" if render_related else "unrelated")
        )
        print(f"Rendering ER diagram for {render_tables} with related={render_related}")
        print(f"file name:{file_name}")
        # input("Press Enter to continue to generete...")
        erg = ERGenerator(
            driver=driver,
            server=server,
            database=name_database,
            username=username,
            password=password,
            reasoning_FK=True,
            disable_sql_FK=False,
        )
        erg.render_file(
            file_name,
            format="png",
            rankdir=TypeRankdir.TB,
            render_tables=render_tables,
            render_related=render_related,
        )
        print("ER diagram generated successfully.", Name_database)
        if first:
            erd = erg.diagram
            table_names = erd.get_table_names()
            t = erd.get_table(table_names[0])
            view_names = erd.get_view_names()
            relations = erd.get_all_relations()
            print(table_names)
            print(t)
            print(view_names)
            print(relations)
            first = False
