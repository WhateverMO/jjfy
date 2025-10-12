from typing import Optional
import re
from django.http import HttpRequest, HttpResponse, JsonResponse

from sqlER import ERDiagram, ERGenerator, TypeRankdir
from eval.eval import eval_qa
from eval.test_case import (
    qa1_case1,
    qa1_case2,
    qa1_case3,
    qa1_case4,
    qa2_case1,
    qa2_case2,
    qa2_case3,
    qa2_case4,
)
# Create your views here.

server_ = "localhost"
Name_database_ = "AdventureWorks2019"
username_ = "sa"
password_ = "test@123SA"
driver_ = "ODBC Driver 17 for SQL Server"
schema_ = "HumanResources"


def get_table_names(request: HttpRequest) -> JsonResponse:
    server: str = request.GET.get("server", server_)
    Name_database: str = request.GET.get("database", Name_database_)
    username: str = request.GET.get("username", username_)
    password: str = request.GET.get("password", password_)
    driver: str = request.GET.get("driver", driver_)
    schema: Optional[str] = request.GET.get("schema", schema_)
    erg: ERGenerator = ERGenerator(
        driver=driver,
        server=server,
        database=Name_database,
        username=username,
        password=password,
    )
    erd: ERDiagram = erg.diagram
    return JsonResponse(
        {
            "table_names": erd.get_table_names(),
            "problem_tables": erg.get_problem_tables(),
        }
    )


def get_view_names(request: HttpRequest) -> JsonResponse:
    server: str = request.GET.get("server", server_)
    Name_database: str = request.GET.get("database", Name_database_)
    username: str = request.GET.get("username", username_)
    password: str = request.GET.get("password", password_)
    driver: str = request.GET.get("driver", driver_)
    schema: Optional[str] = request.GET.get("schema", schema_)
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
    server: str = request.GET.get("server", server_)
    Name_database: str = request.GET.get("database", Name_database_)
    username: str = request.GET.get("username", username_)
    password: str = request.GET.get("password", password_)
    driver: str = request.GET.get("driver", driver_)
    schema: Optional[str] = request.GET.get("schema", schema_)
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
    server: str = request.GET.get("server", server_)
    Name_database: str = request.GET.get("database", Name_database_)
    username: str = request.GET.get("username", username_)
    password: str = request.GET.get("password", password_)
    driver: str = request.GET.get("driver", driver_)
    schema: Optional[str] = request.GET.get("schema", schema_)
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
    if request.method == "GET":
        render_tables = None
        reasoning_FK = True
        reasoning_all_FK = False
        disable_sqlFK = False
        rankdir = TypeRankdir.LR
        render_related = True
        field_omission: bool = False

        server: str = request.GET.get("server", server_)
        Name_database: str = request.GET.get("database", Name_database_)
        username: str = request.GET.get("username", username_)
        password: str = request.GET.get("password", password_)
        driver: str = request.GET.get("driver", driver_)
        schema: Optional[str] = request.GET.get("schema", schema_)
        render_tables: str = request.GET.get("tables", None)
        render_tables: list[str] = render_tables.split(",") if render_tables else None
        reasoning_FK: bool = request.GET.get("reasoning_FK", "true").lower() == "true"
        reasoning_all_FK: bool = (
            request.GET.get("reasoning_all_FK", "false").lower() == "true"
        )
        disable_sqlFK: bool = (
            request.GET.get("disable_sqlFK", "false").lower() == "true"
        )
        if request.GET.get("rankdir", "LR") == "LR":
            rankdir: TypeRankdir = TypeRankdir.LR
        else:
            rankdir: TypeRankdir = TypeRankdir.TB

        render_related: bool = (
            request.GET.get("render_related", "true").lower() == "true"
        )

        field_omission: bool = (
            request.GET.get("field_omission", "false").lower() == "true"
        )
        print(
            f"Received data: {render_tables}\nreasoning_FK: {reasoning_FK}, reasoning_all_FK: {reasoning_all_FK},\
            disable_sqlFK: {disable_sqlFK}, rankdir: {rankdir}, render_related: {render_related},\
            field_omission: {field_omission}"
        )
        diagram_gen = ERGenerator(
            driver=driver,
            server=server,
            database=Name_database,
            username=username,
            password=password,
            reasoning_FK=reasoning_FK,
            reasoning_all_FK=reasoning_all_FK,
            disable_sql_FK=disable_sqlFK,
        )
        svg_data = diagram_gen.render_diagrams(
            rankdir=rankdir,
            render_tables=render_tables,
            render_related=render_related,
            field_omission=field_omission,
        ).decode("utf-8")
        svg_data = re.sub(
            r'<svg\s+width="[^"]+"\s+height="[^"]+"',
            '<svg preserveAspectRatio="xMidYMid meet"',
            svg_data,
            count=1,
        )
        return HttpResponse(svg_data, content_type="image/svg+xml")
    else:
        driver = driver_
        server = server_
        Name_database = Name_database_
        username = username_
        password = password_
        diagram_gen = ERGenerator(
            driver=driver,
            server=server,
            database=Name_database,
            username=username,
            password=password,
        )
        svg_data = diagram_gen.render_diagrams().decode("utf-8")
        svg_data = re.sub(
            r'<svg\s+width="[^"]+"\s+height="[^"]+"',
            '<svg preserveAspectRatio="xMidYMid meet"',
            svg_data,
            count=1,
        ).decode("utf-8")
        return HttpResponse(
            svg_data,
            content_type="image/svg+xml",
        )


from eval.generate_dict_main import level1_names, level2_names, level3_names
from eval.question_2 import SECTION_INDICES


def eval(request: HttpRequest) -> HttpResponse:
    method: str = request.GET.get("method", "entropy")
    res = eval_qa(
        qa1_case1,
        qa2_case1,
        [8, 3, 4, 2, 2, 4, 4, 3, 3],
        [3, 2, 3, 3, 3, 2, 3, 3, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 3, 2, 2, 3],
        level1_names,
        level2_names,
        level3_names,
        SECTION_INDICES,
        method=method,
    )
    return JsonResponse(res)
