from typing import Optional
from django.http import HttpRequest, HttpResponse, JsonResponse

from sqlER import ERDiagram, ERGenerator, TypeRankdir

# Create your views here.

server = "localhost"
Name_database = "AdventureWorks2019"
username = "sa"
password = "test@123SA"
driver = "ODBC Driver 17 for SQL Server"
schema = "HumanResources"


# return a simply HTML to get the ER diagram
def testHMTL(request: HttpRequest) -> HttpResponse:
    # it can select [disable_sqlFK:bool,reasoning_FK:bool,tables:list[str],render_related:bool] to render ER diagram
    data_api_url = "/api/get_table_names"
    view_api_url = "/api/get_view_names"
    draw_url = "/api/erfit"

    render_tables: Optional[list[str]] = None
    reasoning_FK: bool = True
    disable_sqlFK: bool = False
    rankdir: TypeRankdir = TypeRankdir.LR
    render_related: bool = True

    html = f"""
    <html>
      <head>
        <meta charset="utf-8">
        <title>选择数据并绘制</title>
        <style>
          body {{
            font-family: sans-serif;
            margin: 2em;
          }}
          .item-list {{
            margin-bottom: 1em;
          }}
        </style>
      </head>
      <body>
        <h2>请选择要绘制的数据表或视图</h2>
        <form id="select-form">
          <div style="margin-bottom:1em; display:flex; align-items:center; gap:2em;">
            <label>
              <input type="checkbox" name="render_related" checked>
              渲染相关表
            </label>
            <label>
              <input type="checkbox" name="disable_sqlFK">
              禁用SQL外键
            </label>
            <label>
              <input type="checkbox" name="reasoning_FK" checked>
              推理外键
            </label>
            <label style="margin-left:2em;">
              图方向:
              <select name="rankdir">
                <option value="LR" selected>从左到右 (LR)</option>
                <option value="TB">从上到下 (TB)</option>
              </select>
            </label>
            <button type="submit" style="margin-right:2em;">绘制</button>
          </div>
          <div style="display: flex; gap: 2em;">
            <div style="flex:1;">
              <div style="font-weight:bold; margin-bottom:0.5em;">数据表</div>
              <div class="item-list" id="table-list">
                <label style="display:block; font-weight:bold;">
                  <input type="checkbox" id="select-all-tables">
                  全选
                </label>
                加载中...
              </div>
            </div>
            <div style="flex:1;">
              <div style="font-weight:bold; margin-bottom:0.5em;">视图</div>
              <div class="item-list" id="view-list">
                <label style="display:block; font-weight:bold;">
                  <input type="checkbox" id="select-all-views">
                  全选
                </label>
                加载中...
              </div>
            </div>
          </div>
          <button type="submit" style="margin-top:1em;">绘制</button>
        </form>
        <script>
          // 获取表和视图数据并渲染复选框
          Promise.all([
            fetch("{data_api_url}").then(resp => resp.json()),
            fetch("{view_api_url}").then(resp => resp.json())
          ]).then(([tableData, viewData]) => {{
            const tableList = document.getElementById('table-list');
            const viewList = document.getElementById('view-list');
            tableList.innerHTML = '';
            viewList.innerHTML = '';
            // 渲染表
            if (tableData.table_names && tableData.table_names.length > 0) {{
              tableData.table_names.forEach(name => {{
                const label = document.createElement('label');
                label.style.display = 'block';
                const cb = document.createElement('input');
                cb.type = 'checkbox';
                cb.name = 'tables';
                cb.value = name;
                label.appendChild(cb);
                label.appendChild(document.createTextNode(' ' + name));
                tableList.appendChild(label);
              }});
            }}
            // 渲染视图
            if (viewData.view_names && viewData.view_names.length > 0) {{
              viewData.view_names.forEach(name => {{
                const label = document.createElement('label');
                label.style.display = 'block';
                const cb = document.createElement('input');
                cb.type = 'checkbox';
                cb.name = 'tables';
                cb.value = name;
                label.appendChild(cb);
                label.appendChild(document.createTextNode(' ' + name));
                viewList.appendChild(label);
              }});
            }}
          }});

          // 全选/取消全选表
          document.getElementById('select-all-tables').addEventListener('change', function() {{
            const checked = this.checked;
            document.querySelectorAll('#table-list input[type="checkbox"][name="tables"]').forEach(cb => {{
              cb.checked = checked;
            }});
          }});
          // 全选/取消全选视图
          document.getElementById('select-all-views').addEventListener('change', function() {{
            const checked = this.checked;
            document.querySelectorAll('#view-list input[type="checkbox"][name="tables"]').forEach(cb => {{
              cb.checked = checked;
            }});
          }});

          // 表单提交跳转到绘制页面
          document.getElementById('select-form').onsubmit = function(e) {{
            e.preventDefault();
            const checked = Array.from(document.querySelectorAll('input[name="tables"]:checked'))
              .map(cb => cb.value);
            // 如果一个都没选，不传 tables 参数
            const params = new URLSearchParams();
            if (checked.length > 0) {{
              params.set('tables', checked.join(','));
            }}
            params.set('render_related', document.querySelector('input[name="render_related"]').checked ? 'True' : 'False');
            params.set('disable_sqlFK', document.querySelector('input[name="disable_sqlFK"]').checked ? 'True' : 'False');
            params.set('reasoning_FK', document.querySelector('input[name="reasoning_FK"]').checked ? 'True' : 'False');
            params.set('rankdir', document.querySelector('select[name="rankdir"]').value);
            window.location.href = "{draw_url}?" + params.toString();
          }};
        </script>
      </body>
    </html>
    """
    return HttpResponse(html, content_type="text/html")


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
    if request.method == "GET":
        render_tables = None
        reasoning_FK = True
        disable_sqlFK = False
        rankdir = TypeRankdir.LR
        render_related = True

        render_tables = request.GET.get("tables", "")
        reasoning_FK: bool = request.GET.get("reasoning_FK", "true").lower() == "true"
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
        print(f"Received data: {render_tables}")
        diagram_gen = ERGenerator(
            driver=driver,
            server=server,
            database=Name_database,
            username=username,
            password=password,
            reasoning_FK=reasoning_FK,
            disable_sql_FK=disable_sqlFK,
        )
        svg_data = diagram_gen.render_diagrams()
        return HttpResponse(
            svg_data,
            content_type="image/svg+xml",
            headers={"Content-Disposition": "inline; filename=er_diagram.svg"},
        )
    else:
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


def erfit(request: HttpRequest) -> HttpResponse:
    """Serve ER diagram as SVG."""
    if request.method == "GET":
        render_tables = None
        reasoning_FK = True
        disable_sqlFK = False
        rankdir = TypeRankdir.LR
        render_related = True

        render_tables = request.GET.get("tables", None)
        render_tables = render_tables.split(",") if render_tables else None
        reasoning_FK: bool = request.GET.get("reasoning_FK", "true").lower() == "true"
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
        print(
            f"Received data: {render_tables}\nreasoning_FK: {reasoning_FK}, disable_sqlFK: {disable_sqlFK}, rankdir: {rankdir}, render_related: {render_related}"
        )
        diagram_gen = ERGenerator(
            driver=driver,
            server=server,
            database=Name_database,
            username=username,
            password=password,
            reasoning_FK=reasoning_FK,
            disable_sql_FK=disable_sqlFK,
        )
        svg_data = diagram_gen.render_diagrams(
            rankdir=rankdir,
            render_tables=render_tables,
            render_related=render_related,
        ).decode("utf-8")
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
    else:
        return HttpResponse("Method not allowed", status=405)


def api1(request):
    return JsonResponse({"message": "Hello, World!"})


def http1(request):
    return HttpResponse("Hello, World!")


def api2(request):
    return JsonResponse({"api1": "api/api1"})


def http2(request):
    return HttpResponse("api/http1")
