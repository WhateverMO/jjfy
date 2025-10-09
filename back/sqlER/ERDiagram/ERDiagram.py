from enum import Enum
import re, difflib
from typing import Dict, List, Optional, Tuple, Union
from graphviz import Digraph
from pyodbc import Error
from ..connection import dbConnection


class Table:
    """Represents a database table or view."""

    def __init__(self, name: str, is_view: bool = False, schema: Optional[str] = None):
        """
        Initialize a Table instance.

        Args:
            name (str): Name of the table/view.
            is_view (bool, optional): Indicates if it's a view. Defaults to False.
            schema (str, optional): Schema name. Defaults to None.
        """
        self.name = name
        self.fields: List[
            Tuple[str, str, str, bool]
        ] = []  # (field name, type, constraint)
        self.primary_keys: List[str] = []
        self.foreign_keys: List[
            Tuple[str, str, str, str, bool]
        ] = []  # (local field, referenced table, referenced field, constraint, reasoning)
        self.is_view = is_view
        self.schema = schema
        self.comments: List[str] = []  # External comments for the table

    def get_dict(self) -> dict:
        return {
            "name": self.name,
            "fields": [
                {
                    "name": field[0],
                    "type": field[1],
                    "constraint": field[2],
                    "nullable": field[3],
                }
                for field in self.fields
            ],
            "primary_keys": self.primary_keys,
            "foreign_keys": [
                {
                    "field": fk[0],
                    "ref_table": fk[1],
                    "ref_field": fk[2],
                    "constraint": fk[3],
                    "reasoning": fk[4],
                }
                for fk in self.foreign_keys
            ],
            "is_view": self.is_view,
            "schema": self.schema,
            "comments": self.comments,
        }

    def add_field(
        self, name: str, type: str, constraint: str = "", nullable: bool = True
    ) -> None:
        """
        Add a field to the table/view.

        Args:
            name (str): Field name
            type (str): Data type
            constraint (str, optional): Field constraints. Defaults to "".
        """
        self.fields.append((name, type, constraint, nullable))

    def add_primary_key(self, field: str, constraint: str = "PK") -> None:
        """
        Add a primary key field (only for tables).

        Args:
            field (str): Field name
            constraint (str, optional): Constraint type. Defaults to "PK".
        """
        self.primary_keys.append(field)
        # Update field constraint to include PK
        for i, (fname, ftype, fconstraint, fnullable) in enumerate(self.fields):
            if fname == field:
                if fconstraint:
                    # Preserve existing constraints and add PK
                    if "PK" not in fconstraint:
                        new_constraint = fconstraint + "," + constraint
                    else:
                        new_constraint = fconstraint
                else:
                    new_constraint = constraint
                self.fields[i] = (fname, ftype, new_constraint, fnullable)

    def add_foreign_key(
        self,
        field: str,
        ref_table: str,
        ref_field: str,
        constraint: str = "FK",
        reasoning: bool = False,
    ) -> None:
        """
        Add a foreign key relationship (only for tables).

        Args:
            field (str): Local field name
            ref_table (str): Referenced table name
            ref_field (str): Referenced field name
            constraint (str, optional): Constraint type. Defaults to "FK".
        """
        # Add foreign key relationship
        self.foreign_keys.append((field, ref_table, ref_field, constraint, reasoning))
        # Update field constraint to include FK
        for i, (fname, ftype, fconstraint, fnullable) in enumerate(self.fields):
            if fname == field:
                if fconstraint:
                    # Preserve existing constraints and add FK
                    if "FK" not in fconstraint:
                        # new_constraint = fconstraint + "," + constraint
                        new_constraint = fconstraint + "," + "FK"
                    else:
                        new_constraint = fconstraint
                else:
                    # new_constraint = constraint
                    new_constraint = "FK"
                self.fields[i] = (fname, ftype, new_constraint, fnullable)

    def add_comment(self, comment: str) -> None:
        """
        Add an external comment to the table.

        Args:
            comment (str): Comment text
        """
        self.comments.append(comment)

    def __repr__(self) -> str:
        s: str = (
            f"<{'View' if self.is_view else 'Table'}: {self.schema + '.' if self.schema else ''}{self.name}>\n"
            + "Fields:\n"
        )
        for field in self.fields:
            s += f"  - {field[0]}: {field[1]} nullable:{field[3]} ({field[2]})\n"
        if self.comments:
            s += "Comments:\n"
            for comment in self.comments:
                s += f"  - {comment}\n"
        return s


class TypeRankdir(Enum):
    LR = "LR"  # Left to Right
    TB = "TB"  # Top to Bottom


class ERDiagram:
    """Generates and manages ER diagrams."""

    def __init__(self, name: str = "ER_Diagram"):
        """
        Initialize an ERDiagram instance.

        Args:
            name (str, optional): Diagram name. Defaults to "ER_Diagram".
        """
        self.name = name
        self.tables: Dict[str, Table] = {}
        self.relations: List[Dict] = []  # Stores relationship information
        # High-quality rendering settings
        self.font_name = "Arial"
        self.font_size = 13
        self.dpi = 300
        self.cell_padding = 4
        self.comment_font_size = 10  # Font size for comments
        self.comment_color = "#666666"  # Color for comments

    def set_quality_settings(
        self,
        font_name: str = "Arial",
        font_size: int = 13,
        dpi: int = 1300,
        cell_padding: int = 4,
        comment_font_size: int = 10,
        comment_color: str = "#666666",
        rankdir: TypeRankdir = TypeRankdir.TB,
    ) -> None:
        """
        Set high-quality rendering parameters.

        Args:
            font_name (str, optional): Font name. Defaults to "Arial".
            font_size (int, optional): Font size. Defaults to 14.
            dpi (int, optional): Image resolution. Defaults to 1300.
            cell_padding (int, optional): Cell padding. Defaults to 4.
            comment_font_size (int, optional): Comment font size. Defaults to 10.
            comment_color (str, optional): Comment text color. Defaults to "#666666".
        """
        self.font_name = font_name
        self.font_size = font_size
        self.dpi = dpi
        self.cell_padding = cell_padding
        self.comment_font_size = comment_font_size
        self.comment_color = comment_color
        self.rankdir = rankdir

    def add_table(self, table: Table) -> None:
        """Add a table to the ER diagram."""
        self.tables[table.name] = table

    def add_view(self, name: str) -> Table:
        """
        Create and add a view to the ER diagram.

        Args:
            name (str): View name

        Returns:
            Table: Created view object
        """
        view = Table(name, is_view=True)
        self.tables[name] = view
        return view

    def add_relation(
        self,
        from_table: str,
        from_field: str,
        to_table: str,
        to_field: str,
        relation_label: str = "1..N",
        reasoning: bool = False,
    ) -> None:
        """
        Add a table relationship (only for tables).

        Args:
            from_table (str): Source table name
            from_field (str): Source field name
            to_table (str): Target table name
            to_field (str): Target field name
            relation_label (str, optional): Relationship label. Defaults to "1..N".
        """
        if from_table in self.tables:
            self.tables[from_table].add_foreign_key(
                from_field, to_table, to_field, "FK", reasoning
            )
            self.relations.append(
                {
                    "from_table": from_table,
                    "from_field": from_field,
                    "to_table": to_table,
                    "to_field": to_field,
                    "label": relation_label,
                    "reasoning": reasoning,
                }
            )

    def get_table(self, table_name: str) -> Optional[Table]:
        """
        Get table structure by name.

        Args:
            table_name (str): Table name

        Returns:
            Optional[Table]: Table object or None if not found
        """
        return self.tables.get(table_name)

    def get_all_relations(self) -> List[Dict]:
        """Get all relationships."""
        return self.relations

    def get_table_names(self) -> List[str]:
        """Get all table names (excluding views)."""
        return [name for name, table in self.tables.items() if not table.is_view]

    def get_view_names(self) -> List[str]:
        """Get all view names."""
        return [name for name, table in self.tables.items() if table.is_view]

    def render_to_bytes(
        self,
        format: str = "svg",
        render_tables: Optional[list[str]] = None,
        render_related: bool = False,
        field_omission: bool = False,
    ) -> bytes:
        """
        Render ER diagram to bytes.

        Args:
            format (str, optional): Output format. Defaults to "svg".
            render_tables (Optional[list[str]], optional): List of table names to render. If None, renders all tables. Defaults to None.
            render_related (bool, optional): If True, renders related tables. Defaults to False.

        Returns:
            bytes: Rendered diagram bytes
        """
        er = Digraph(
            self.name,
            graph_attr={
                "dpi": str(self.dpi),
                "fontname": self.font_name,
                "fontsize": str(self.font_size),
            },
            node_attr={"fontname": self.font_name},
            edge_attr={"fontname": self.font_name},
        )
        er.attr(rankdir=self.rankdir.value)
        er.attr("node", shape="plaintext")
        er.attr(splines="polyline")

        dst_table = render_tables
        render_fields: list[str] = []
        if render_tables is not None and render_related:
            dst_table = render_tables.copy()
            for rel in self.relations:
                from_table = rel["from_table"]
                from_field = rel["from_field"]
                to_table = rel["to_table"]
                to_field = rel["to_field"]
                if from_table in dst_table:
                    render_tables.append(to_table)
                if to_table in dst_table:
                    render_tables.append(from_table)
                render_fields.append(from_field)
                render_fields.append(to_field)

        render_fields = list(set(render_fields))  # Remove duplicates
        if not field_omission:
            render_fields = []

        # Render all tables
        for table in self.tables.values():
            render: bool = False
            if render_tables == None:
                render = True
            elif table.name in render_tables:
                render = True

            if render:
                er.node(
                    table.name, label=self._generate_table_label(table, render_fields)
                )
                # Add external comments for the table
                if table.comments:
                    comment_node_name = f"{table.name}_comment"
                    er.node(
                        comment_node_name,
                        label=self._generate_comment_label(table.comments),
                        shape="none",
                        fontsize=str(self.comment_font_size),
                        fontcolor=self.comment_color,
                    )
                    er.edge(
                        table.name,
                        comment_node_name,
                        style="invis",  # Invisible edge to position comment below table
                        constraint="false",  # Don't affect layout constraints
                    )

        # Render relationships (only for tables)
        for rel in self.relations:
            from_table = rel["to_table"]
            from_field = rel["to_field"]
            to_table = rel["from_table"]
            to_field = rel["from_field"]
            label = rel["label"]
            reasoning = rel["reasoning"]

            render: bool = False
            if render_tables == None:
                render = True
            elif from_table in render_tables and to_table in render_tables:
                render = True

            if render:
                style = "solid"
                if reasoning:
                    style = "dashed"
                er.edge(
                    f"{from_table}",
                    f"{to_table}",
                    label=label,
                    style=style,
                    arrowhead="dot",
                    fontsize=str(self.font_size),
                )

        return er.pipe(format=format)

    def render_to_file(
        self,
        filename: str = "er_diagram",
        format: str = "svg",
        render_tables: Optional[list[str]] = None,
        render_related: bool = False,
        field_omission: bool = False,
    ) -> None:
        """
        Render ER diagram to file.

        Args:
            filename (str, optional): Output filename. Defaults to "er_diagram".
            format (str, optional): Output format. Defaults to "svg".
        """
        er_bytes = self.render_to_bytes(
            format,
            render_tables=render_tables,
            render_related=render_related,
            field_omission=field_omission,
        )
        with open(f"{filename}.{format}", "wb") as f:
            f.write(er_bytes)

    def _generate_table_label(self, table: Table, render_fields: list[str] = []) -> str:
        """
        Generate high-quality table structure label.

        Args:
            table (Table): Table object
            render_fields (list[str], optional): List of fields to render. If empty, renders all fields. Defaults to [].

        Returns:
            str: HTML-like label string
        """
        header_bg = ""
        title = ""
        if table.is_view:
            header_bg = "#cceeff"
            title = f"<B><FONT POINT-SIZE='{self.font_size + 2}'>{table.name}</FONT><BR/><I>(VIEW)</I></B>"
        else:
            header_bg = "#f0f0f0"
            title = (
                f"<B><FONT POINT-SIZE='{self.font_size + 2}'>{table.name}</FONT></B>"
            )

        rows = [
            f'<TR><TD COLSPAN="4" BGCOLOR="{header_bg}">{title}</TD></TR>',
            '<TR><TD ALIGN="LEFT"><B>Column</B></TD><TD ALIGN="LEFT"><B>Type</B></TD><TD ALIGN="LEFT"><B>nullable</B></TD><TD ALIGN="LEFT"><B>Constraint</B></TD></TR>',
        ]

        omitted: bool = False

        for name, type, constraint, nullable in table.fields:
            type_cell = f'<TD ALIGN="LEFT">{type}</TD>'
            nullable_cell: str = f'<TD ALIGN="LEFT">{str(nullable).upper()}</TD>'
            DIVISION = 13
            # Handle fields that are both PK and FK
            if constraint and "PK" in constraint and "FK" in constraint:
                Constraints = constraint.split(",")
                PK_constraint = FK_constraint = ""
                for constraint in Constraints:
                    if "PK" in constraint:
                        PK_constraint = constraint + " " * int(
                            len(constraint) / DIVISION
                        )
                    if "FK" in constraint:
                        FK_constraint = constraint
                name_cell = f'<TD rowspan="2" ALIGN="LEFT"><B><I>{name}</I></B></TD>'
                type_cell = f'<TD rowspan="2" ALIGN="LEFT">{type}</TD>'
                nullable_cell = (
                    f'<TD rowspan="2" ALIGN="LEFT">{str(nullable).upper()}</TD>'
                )
                PK_constraint_cell = (
                    f'<TD ALIGN="LEFT" BGCOLOR="#ffcccc">{PK_constraint}</TD>'
                )
                FK_constraint_cell = (
                    f'<TD ALIGN="LEFT" BGCOLOR="#ccffcc">{FK_constraint}</TD>'
                )
                row = f"<TR>{name_cell}{type_cell}{nullable_cell}{PK_constraint_cell}</TR><TR>{FK_constraint_cell}</TR>"
            elif constraint and "PK" in constraint:
                constraint += " " * int(len(constraint) / DIVISION)
                name_cell = f'<TD ALIGN="LEFT"><B>{name}</B></TD>'
                constraint_cell = (
                    f'<TD ALIGN="LEFT" BGCOLOR="#ffcccc">{constraint}</TD>'
                )
                row = f"<TR>{name_cell}{type_cell}{nullable_cell}{constraint_cell}</TR>"
            elif constraint and "FK" in constraint:
                constraint += " " * int(len(constraint) / DIVISION)
                name_cell = f'<TD ALIGN="LEFT"><I>{name}</I></TD>'
                constraint_cell = (
                    f'<TD ALIGN="LEFT" BGCOLOR="#ccffcc">{constraint}</TD>'
                )
                row = f"<TR>{name_cell}{type_cell}{nullable_cell}{constraint_cell}</TR>"
            else:
                render_field: bool = True
                if len(render_fields) != 0 and name not in render_fields:
                    render_field = False
                if render_field:
                    constraint += " " * int(len(constraint) / DIVISION)
                    name_cell = f'<TD ALIGN="LEFT">{name}</TD>'
                    constraint_cell = (
                        f'<TD ALIGN="LEFT">{constraint}</TD>'
                        if constraint
                        else '<TD ALIGN="LEFT"></TD>'
                    )
                    row = f"<TR>{name_cell}{type_cell}{nullable_cell}{constraint_cell}</TR>"
                else:
                    omitted = True
                    continue

            rows.append(row)

        if omitted:
            rows.append(
                '<TR><TD ALIGN="LEFT">...</TD><TD ALIGN="LEFT">...</TD><TD ALIGN="LEFT">...</TD><TD ALIGN="LEFT">...</TD></TR>'
            )

        return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="{self.cell_padding}">
        {"".join(rows)}
        </TABLE>>'''

    def _generate_comment_label(self, comments: List[str]) -> str:
        """
        Generate label for external comments.

        Args:
            comments (List[str]): List of comment strings

        Returns:
            str: HTML-like label string for comments
        """
        comment_lines = []
        for comment in comments:
            # Split long comments into multiple lines
            words = comment.split()
            line = ""
            for word in words:
                if len(line) + len(word) + 1 > 60:  # Limit line length
                    comment_lines.append(f"<TR><TD>{line}</TD></TR>")
                    line = word
                else:
                    line += (" " if line else "") + word
            if line:
                comment_lines.append(f"<TR><TD>{line}</TD></TR>")

        return f"""<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="2">
        {"".join(comment_lines)}
        </TABLE>>"""


class ERGenerator:
    """service wrapper for generating all ER diagrams."""

    def __init__(
        self,
        driver: Optional[str] = None,
        server: Optional[str] = None,
        database: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        reasoning_FK: bool = False,
        reasoning_all_FK: bool = False,
        disable_sql_FK: bool = False,
    ):
        """
        Initialize an ERGenerator instance.
        And analysis the database schema and generate ER diagrams.

        Args:
            driver (Optional[str]): Database driver name.
            server (Optional[str]): Database server address.
            database (Optional[str]): Database name.
            username (Optional[str]): Database username.
            password (Optional[str]): Database password.
            reasoning_FK (bool, optional): Whether to reason foreign keys. Defaults to False.
            disable_sql_FK (bool, optional): Whether to disable SQL foreign keys. Defaults to True.
        """
        self.driver: Optional[str] = driver
        self.server: Optional[str] = server
        self.database: Optional[str] = database
        self.username: Optional[str] = username
        self.password: Optional[str] = password
        self.diagram: ERDiagram = ERDiagram(str(database))
        self._analysis_database_mssql(
            reasoning_FK=reasoning_FK,
            reasoning_all_FK=reasoning_all_FK,
            disable_sql_FK=disable_sql_FK,
        )

    def _analysis_database_mssql(
        self,
        reasoning_FK: bool = False,
        reasoning_all_FK: bool = False,
        disable_sql_FK: bool = False,
    ) -> None:
        """
        Analyze the database schema and generate ER diagrams.
        This method retrieves tables, views, primary keys, and foreign keys
        from the database connection and builds the ER diagrams accordingly.

        Args:
            reasoning_FK (bool, optional): Whether to reason foreign keys. Defaults to False.
            disable_sql_FK (bool, optional): Whether to disable SQL foreign keys. Defaults to True.
        """

        self.schemas: list[str] = []
        self.tables: list[Table] = []
        self.relations: list[tuple[str, str, str, str, str, bool]] = []
        self.problem_tables: list[str] = []

        class field_reasoing_FK:
            def __init__(self, field_name: str):
                self.field_name: str = field_name
                self.pk_tables: list[Tuple[str, int]] = []
                self.fk_tables: list[str] = []

            def reasoning(self) -> None:
                # sort the tables by the number of primary keys
                self.pk_tables.sort(key=lambda x: x[1])
                similaritest: float = 0.0
                similarity: float = 0.0
                similaritest_table = ""
                if len(self.pk_tables) + len(self.fk_tables) <= 1:
                    return
                if len(self.pk_tables) == 0:
                    self.pk_tables = [(fkt, 1) for fkt in self.fk_tables]
                    self.fk_tables = []
                if len(self.pk_tables) != 1:
                    not_onePKT = []
                    onePKT = []
                    for table, pk_num in self.pk_tables:
                        if pk_num == 1:
                            similaritest_table = table
                            onePKT.append((table, pk_num))
                        else:
                            not_onePKT.append((table, pk_num))
                    onePKT_num = len(onePKT)
                    for_PKT = onePKT
                    if onePKT_num == 1:
                        for_PKT = [(similaritest_table, 1)]
                    elif onePKT_num < 1:
                        for_PKT = not_onePKT
                    for table, pk_num in for_PKT:
                        # select the most similar table (calculate table,field_name similarity)
                        similarity = difflib.SequenceMatcher(
                            None, self.field_name, table
                        ).ratio()
                        if similarity > similaritest:
                            similaritest = similarity
                            similaritest_table = table
                    for table, _ in self.pk_tables:
                        if table != similaritest_table:
                            self.fk_tables.append(table)
                    self.pk_tables = [(similaritest_table, 1)]

            def __repr__(self) -> str:
                repr: str = (
                    f"Field: {self.field_name}\n"
                    + f"Primary Key Table: {self.pk_tables}\n"
                    + f"fk Tables: {self.fk_tables}\n"
                )
                return repr

        reasoning_FK_dict: dict[str, field_reasoing_FK] = {
            # "field": {
            #     field_reasoing_FK()
            # }
        }

        dbcnxt: dbConnection = dbConnection(
            driver=self.driver,
            server=self.server,
            database=self.database,
            username=self.username,
            password=self.password,
            schema_name="dbo",
        )
        with dbcnxt:
            schemas = dbcnxt.schemas()
            for schema in schemas:
                self.schemas.append(schema[1])
        for schema in self.schemas:
            dbcnxt: dbConnection = dbConnection(
                driver=self.driver,
                server=self.server,
                database=self.database,
                username=self.username,
                password=self.password,
                schema_name=schema,
            )
            with dbcnxt:
                tables = dbcnxt.tables(exclusion=True)
                for table in tables:
                    table_name = table[2]
                    table_schema = table[1]
                    is_view = table[-2] == "VIEW"
                    if table_schema == schema:
                        t: Table = Table(table_name, is_view=is_view, schema=schema)
                        primary_keys = dbcnxt.pk(table[2])["primaryKeys"]
                        primary_key_fields_constraint = [
                            (fk[3], fk[-1]) for fk in primary_keys
                        ]
                        try:
                            fields = dbcnxt.fields(table_name, schema_name=schema)
                        except Exception:
                            self.problem_tables.append(table_name)
                            continue
                        for field in fields:
                            field_name = field[0]
                            field_type = "UNKNOWN"
                            field_nullable = field[6]
                            match = re.search(r"'(.+?)'", str(field[1]))
                            if match:
                                full_name = match.group(1)
                                # 分割并取最后一部分（如 'datetime'）
                                field_type = full_name.split(".")[-1].lower()
                            t.add_field(field_name, field_type, nullable=field_nullable)
                            if reasoning_FK and not is_view:
                                pk_fields = [
                                    pk_field
                                    for pk_field, _ in primary_key_fields_constraint
                                ]
                                pk_num = len(pk_fields)
                                if field_name in reasoning_FK_dict.keys():
                                    obj = reasoning_FK_dict[field_name]
                                    if field_name in pk_fields:
                                        obj.pk_tables.append((table_name, pk_num))
                                    else:
                                        obj.fk_tables.append(table_name)
                                else:
                                    obj = field_reasoing_FK(field_name)
                                    if field_name in pk_fields:
                                        obj.pk_tables.append((table_name, pk_num))
                                    else:
                                        obj.fk_tables.append(table_name)
                                    reasoning_FK_dict[field_name] = obj

                        for pk_field, pk_constraint in primary_key_fields_constraint:
                            t.add_primary_key(pk_field, pk_constraint)
                        if not disable_sql_FK:
                            foreign_keys = dbcnxt.fk(table[2])["foreignKeys"]
                            foreign_key_fields_constraint = [
                                (fk[6], fk[7], fk[2], fk[3], fk[-3])
                                for fk in foreign_keys
                            ]
                            for (
                                fk_ref_table,
                                fk_ref_field,
                                fk_table,
                                fk_field,
                                fk_constraint,
                            ) in foreign_key_fields_constraint:
                                # t.add_foreign_key(
                                #     fk_field, fk_ref_table, fk_ref_field, fk_constraint
                                # )
                                self.relations.append(
                                    (
                                        fk_ref_table,
                                        fk_ref_field,
                                        fk_table,
                                        fk_field,
                                        fk_constraint,
                                        False,
                                    )
                                )

                        self.diagram.add_table(t)
                        self.tables.append(t)

        for FieldrFK, rFKdict in reasoning_FK_dict.items():
            if (
                (len(rFKdict.pk_tables) != 0 and len(rFKdict.fk_tables) != 0)
                or len(rFKdict.pk_tables) > 1
                or (
                    reasoning_all_FK
                    and len(rFKdict.pk_tables) == 0
                    and len(rFKdict.fk_tables) > 1
                )
            ):
                rFKdict.reasoning()
                pk_table = rFKdict.pk_tables[0][0]
                fk_tables = rFKdict.fk_tables
                for fk_table in fk_tables:
                    self.relations.append(
                        (
                            fk_table,
                            FieldrFK,
                            pk_table,
                            FieldrFK,
                            "FK_" + fk_table + "_" + pk_table + "_" + FieldrFK,
                            True,
                        )
                    )

        for relation in self.relations:
            fk_ref_table, fk_ref_field, fk_table, fk_field, fk_constraint, reasoning = (
                relation
            )
            self.diagram.add_relation(
                fk_ref_table,
                fk_ref_field,
                fk_table,
                fk_field,
                relation_label=fk_constraint,
                reasoning=reasoning,
            )

    def get_problem_tables(self):
        return self.problem_tables

    def render_diagrams(
        self,
        rankdir: TypeRankdir = TypeRankdir.TB,
        dpi: int = 1300,
        render_tables: Optional[list[str]] = None,
        render_related: bool = False,
        field_omission: bool = False,
    ) -> bytes:
        """
        Render all ER diagrams to bytes.
        """
        self.diagram.set_quality_settings(rankdir=rankdir, dpi=dpi)
        return self.diagram.render_to_bytes(
            format="svg",
            render_tables=render_tables,
            render_related=render_related,
            field_omission=field_omission,
        )

    def render_file(
        self,
        filename: str = "er-diagram",
        format: str = "svg",
        dpi: int = 1300,
        rankdir: TypeRankdir = TypeRankdir.TB,
        render_tables: Optional[list[str]] = None,
        render_related: bool = False,
        field_omission: bool = False,
    ) -> None:
        """
        Render the ER diagram to a file.
        """
        self.diagram.set_quality_settings(rankdir=rankdir, dpi=dpi)
        self.diagram.render_to_file(
            format=format,
            filename=filename,
            render_tables=render_tables,
            render_related=render_related,
            field_omission=field_omission,
        )
