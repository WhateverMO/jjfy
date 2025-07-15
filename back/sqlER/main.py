from connection import dbConnection

server = "localhost"
Name_database = "AdventureWorks2019"
username = "sa"
password = "test@123SA"
driver = "ODBC Driver 17 for SQL Server"
schema = "HumanResources"


# server = "svn.dev.jd.jk"
# database = "TM_DATABASE"
# username = "sa"
# password = "cardc_0820"
# driver = "ODBC Driver 17 for SQL Server"

dbcnxt = dbConnection(
    driver=driver,
    server=server,
    database=Name_database,
    username=username,
    password=password,
    schema=schema,
)

with dbcnxt:
    print(dbcnxt.schemas())
    tables = dbcnxt.tables()
for t in tables:
    print(t)

# with dbcnxt:
#     results = dbcnxt.selct_all("EmployeeDepartmentHistory")
with dbcnxt:
    results = dbcnxt.selct_all("EmployeeDepartmentHistory")
    # rows = results["rows"]
    desc = results["desc"]
    # messages = results["messages"]
    # rowcount = results["rowcount"]
    # for row in rows:
    #     print(row)
    # print()
    # print(desc)
    # print(rowcount)
    # print(messages)
    # print()
    print("desc:")
    for d in desc:
        print(d)
    print()

    results = dbcnxt.pk("EmployeeDepartmentHistory")
    desc = results["desc"]
    messages = results["messages"]
    rowcount = results["rowcount"]
    primaryKeys = results["primaryKeys"]

    print()
    print(rowcount)
    print(desc)
    print(messages)
    print()
    print("primaryKeys:")
    print(primaryKeys)
    print()

    results = dbcnxt.fk("Employee")
    desc = results["desc"]
    messages = results["messages"]
    rowcount = results["rowcount"]
    foreignKeys = results["foreignKeys"]
    print()
    print(rowcount)
    print(desc)
    print(messages)
    print()
    print("foreignKeys:")
    print(foreignKeys)
    print()
    for fk in foreignKeys:
        print(fk)

# from ERDiagram import ERDiagram, Table
#
#
# class DiagramGenerator:
#     """Service wrapper for generating ER diagrams."""
#
#     def __init__(self, diagram_name: str = "SystemDiagram"):
#         """
#         Initialize a DiagramGenerator instance.
#
#         Args:
#             diagram_name (str, optional): Diagram name. Defaults to "SystemDiagram".
#         """
#         self.diagram = ERDiagram(diagram_name)
#         self.diagram.set_quality_settings()
#
#     def build_example_diagram(self) -> None:
#         """Build an example ER diagram."""
#         # Create tables
#         user_table = Table("User")
#         user_table.add_field("id", "INT", "PK")
#         user_table.add_field("name", "VARCHAR(50)")
#         user_table.add_field("email", "VARCHAR(100)", "UNIQUE")
#
#         order_table = Table("Order")
#         order_table.add_field("id", "INT", "PK")
#         order_table.add_field("user_id", "INT")
#         order_table.add_field("product_id", "INT")
#         order_table.add_field("order_date", "TIMESTAMP")
#         order_table.add_field("amount", "DECIMAL(10,2)")
#
#         product_table = Table("Product")
#         product_table.add_field("id", "INT", "PK")
#         product_table.add_field("name", "VARCHAR(100)")
#         product_table.add_field("price", "DECIMAL(8,2)")
#
#         # Create view
#         user_order_view = self.diagram.add_view("v_user_orders")
#         user_order_view.add_field("user_id", "INT")
#         user_order_view.add_field("user_name", "VARCHAR(50)")
#         user_order_view.add_field("total_orders", "INT")
#         user_order_view.add_field("total_spent", "DECIMAL(10,2)")
#
#         # Add to diagram
#         self.diagram.add_table(user_table)
#         self.diagram.add_table(order_table)
#         self.diagram.add_table(product_table)
#
#         # Add relationships
#         self.diagram.add_relation(
#             "Order", "user_id", "User", "id", relation_label="FK (1..N)"
#         )
#         self.diagram.add_relation(
#             "Order", "product_id", "Product", "id", relation_label="FK (N..1)"
#         )
#
#     def get_diagram(self, format: str = "svg") -> bytes:
#         """
#         Get ER diagram in byte format.
#
#         Args:
#             format (str, optional): Output format. Defaults to "svg".
#
#         Returns:
#             bytes: Diagram data
#         """
#         self.diagram.render_to_file(format=format)
#         return self.diagram.render_to_bytes(format)
#
#     def get_diagram_base64(self, format: str = "svg") -> str:
#         """
#         Get ER diagram as base64-encoded string.
#
#         Args:
#             format (str, optional): Output format. Defaults to "svg".
#
#         Returns:
#             str: Base64-encoded diagram
#         """
#         import base64
#
#         er_bytes = self.get_diagram(format)
#         return base64.b64encode(er_bytes).decode("utf-8")
#
#
# from flask import Flask, Response
#
# app = Flask(__name__)
#
#
# @app.route("/er-diagram")
# def serve_er_diagram() -> Response:
#     """Serve ER diagram as SVG."""
#     diagram_gen = DiagramGenerator()
#     diagram_gen.build_example_diagram()
#     svg_data = diagram_gen.get_diagram("svg")
#     return Response(
#         svg_data,
#         mimetype="image/svg+xml",
#         headers={"Content-Disposition": "inline; filename=er_diagram.svg"},
#     )
#
#
# if __name__ == "__main__":
#     app.run(port=5000)

if __name__ == "__main__":
    pass
