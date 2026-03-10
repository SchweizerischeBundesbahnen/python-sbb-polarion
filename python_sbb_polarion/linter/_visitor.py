"""AST visitor for code style linting."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import ClassVar

from ._helpers import contains_query_params, get_method_name, reconstruct_fstring
from ._violation import Violation


class CodeStyleLinter(ast.NodeVisitor):
    """AST visitor that checks for code style violations."""

    # API request methods that require variable arguments
    API_REQUEST_METHODS: frozenset[str] = frozenset(
        {
            "api_request_get",
            "api_request_post",
            "api_request_put",
            "api_request_patch",
            "api_request_delete",
        }
    )

    # Arguments that must be variables (not inline expressions)
    MUST_BE_VARIABLE_ARGS: frozenset[str] = frozenset(
        {
            "headers",
            "params",
            "data",
            "files",
            "json",
        }
    )

    # Dict variable names that require multiline formatting
    TYPED_DICT_NAMES: frozenset[str] = frozenset(
        {
            "headers",
            "params",
            "data",
            "files",
        }
    )

    # Type annotations that require multiline dict formatting
    MULTILINE_DICT_TYPES: frozenset[str] = frozenset(
        {
            "JsonDict",
        }
    )

    # Variables that don't need type annotations
    SKIP_VARS: frozenset[str] = frozenset({"self", "cls"})

    # Directories to skip when scanning
    SKIP_DIRS: frozenset[str] = frozenset({"__pycache__", "build", "dist", ".tox", ".venv"})

    # HTTP status codes that should use HTTPStatus enum (PSP006)
    HTTP_STATUS_CODES: ClassVar[dict[int, str]] = {
        100: "CONTINUE",
        101: "SWITCHING_PROTOCOLS",
        200: "OK",
        201: "CREATED",
        202: "ACCEPTED",
        204: "NO_CONTENT",
        206: "PARTIAL_CONTENT",
        301: "MOVED_PERMANENTLY",
        302: "FOUND",
        304: "NOT_MODIFIED",
        307: "TEMPORARY_REDIRECT",
        308: "PERMANENT_REDIRECT",
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        406: "NOT_ACCEPTABLE",
        408: "REQUEST_TIMEOUT",
        409: "CONFLICT",
        410: "GONE",
        415: "UNSUPPORTED_MEDIA_TYPE",
        422: "UNPROCESSABLE_ENTITY",
        429: "TOO_MANY_REQUESTS",
        500: "INTERNAL_SERVER_ERROR",
        501: "NOT_IMPLEMENTED",
        502: "BAD_GATEWAY",
        503: "SERVICE_UNAVAILABLE",
        504: "GATEWAY_TIMEOUT",
    }

    # Header string values that should use Header enum (PSP007)
    HEADER_VALUES: ClassVar[dict[str, str]] = {
        "Accept": "Header.ACCEPT",
        "Authorization": "Header.AUTHORIZATION",
        "Content-Type": "Header.CONTENT_TYPE",
        "X-API-Key": "Header.X_API_KEY",
    }

    # MediaType string values that should use MediaType enum (PSP008)
    MEDIA_TYPE_VALUES: ClassVar[dict[str, str]] = {
        "application/json": "MediaType.JSON",
        "text/html": "MediaType.HTML",
        "application/xml": "MediaType.XML",
        "application/pdf": "MediaType.PDF",
        "text/plain": "MediaType.PLAIN",
        "application/octet-stream": "MediaType.OCTET_STREAM",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "MediaType.DOCX",
        "application/zip": "MediaType.ZIP",
        "*/*": "MediaType.ANY",
    }

    # AuthScheme string values that should use AuthScheme enum (PSP009)
    AUTH_SCHEME_VALUES: ClassVar[dict[str, str]] = {
        "Bearer": "AuthScheme.BEARER",
        "Basic": "AuthScheme.BASIC",
    }

    # Custom ignore comment prefix (different from ruff's noqa to avoid conflicts)
    IGNORE_COMMENT: str = "# psp-ignore:"

    def __init__(self, file_path: Path, source_lines: list[str] | None = None) -> None:
        """Initialize linter with file path and optional source lines."""
        self.file_path: Path = file_path
        self.source_lines: list[str] = source_lines or []
        self.violations: list[Violation] = []
        self._in_function: bool = False
        self._function_args: set[str] = set()
        self._annotated_vars: set[str] = set()
        self._class_attrs: set[str] = set()
        self._in_class: bool = False
        self._in_comprehension: bool = False
        self._in_binop: bool = False
        self._in_status_code_compare: bool = False
        self._has_future_annotations: bool = False
        self._collection_none_vars: set[str] = set()
        self._empty_dict_vars: set[str] = set()
        self._is_test_file: bool = _check_is_test_file(file_path)
        self._has_cast_import: bool = False

    def _add_violation(self, node: ast.expr | ast.stmt, code: str, message: str) -> None:
        """Add a violation to the list, respecting psp-ignore comments."""
        if self._is_suppressed(node, code):
            return
        self.violations.append(
            Violation(
                file=self.file_path,
                line=node.lineno,
                col=node.col_offset,
                code=code,
                message=message,
            )
        )

    def _is_suppressed(self, node: ast.expr | ast.stmt, code: str) -> bool:
        """Check if violation is suppressed by psp-ignore comment.

        Returns:
            True if violation is suppressed, False otherwise.
        """
        if not self.source_lines or node.lineno <= 0 or node.lineno > len(self.source_lines):
            return False
        line: str = self.source_lines[node.lineno - 1]
        if self.IGNORE_COMMENT not in line:
            return False
        ignore_part: str = line.split(self.IGNORE_COMMENT)[1]
        suppressed_codes: set[str] = _parse_suppressed_codes(ignore_part)
        return code in suppressed_codes

    def visit_Module(self, node: ast.Module) -> None:
        """Check module for future annotations import and cast import."""
        for stmt in node.body:
            if isinstance(stmt, ast.ImportFrom):
                self._check_import_from(stmt)
        self.generic_visit(node)

    def _check_import_from(self, stmt: ast.ImportFrom) -> None:
        """Check import from statement for annotations and cast."""
        if stmt.module == "__future__":
            for alias in stmt.names:
                if alias.name == "annotations":
                    self._has_future_annotations = True
                    break
        elif stmt.module == "typing":
            for alias in stmt.names:
                if alias.name == "cast":
                    self._has_cast_import = True
                    break

    def _check_quoted_annotation(self, annotation: ast.expr | None, node: ast.AST, *, inside_literal: bool = False) -> None:
        """Check if annotation is a quoted string (PSP010)."""
        if annotation is None:
            return
        if isinstance(annotation, ast.Constant) and isinstance(annotation.value, str) and not inside_literal:
            msg: str = _get_quoted_type_message(annotation.value, self._has_future_annotations)
            self._add_violation(annotation, "PSP010", msg)
        elif isinstance(annotation, ast.Subscript):
            self._check_subscript_annotation(annotation, node)
        elif isinstance(annotation, ast.Tuple):
            for elt in annotation.elts:
                self._check_quoted_annotation(elt, node)
        elif isinstance(annotation, ast.BinOp):
            self._check_quoted_annotation(annotation.left, node)
            self._check_quoted_annotation(annotation.right, node)

    def _check_subscript_annotation(self, annotation: ast.Subscript, node: ast.AST) -> None:
        """Check subscript annotation for quoted types."""
        is_literal: bool = _is_literal_subscript(annotation)
        self._check_quoted_annotation(annotation.slice, node, inside_literal=is_literal)
        if isinstance(annotation.value, ast.Constant) and isinstance(annotation.value.value, str):
            msg: str = _get_quoted_type_message(annotation.value.value, self._has_future_annotations)
            self._add_violation(annotation.value, "PSP010", msg)

    def _check_any_in_annotation(self, annotation: ast.expr | None) -> None:
        """Check if annotation contains Any which is disallowed (PSP017)."""
        if annotation is None or self._is_test_file:
            return
        # Check for standalone Any (e.g., var: Any = ...)
        if isinstance(annotation, ast.Name) and annotation.id == "Any":
            self._add_violation(
                annotation,
                "PSP017",
                "Don't use `Any` in type annotations. Use a specific type.",
            )
        elif isinstance(annotation, ast.Subscript):
            self._check_subscript_for_any(annotation)
        elif isinstance(annotation, ast.BinOp) and isinstance(annotation.op, ast.BitOr):
            self._check_any_in_annotation(annotation.left)
            self._check_any_in_annotation(annotation.right)
        elif isinstance(annotation, ast.Tuple):
            for elt in annotation.elts:
                self._check_any_in_annotation(elt)

    def _check_subscript_for_any(self, annotation: ast.Subscript) -> None:
        """Check subscript for Any usage patterns."""
        # Special case: dict[str, Any] -> suggest JsonDict (don't recurse to avoid double-flagging)
        if _is_dict_str_any(annotation):
            self._add_violation(
                annotation,
                "PSP017",
                "Use `JsonDict` instead of `dict[str, Any]`. Import from `python_sbb_polarion.types`.",
            )
            return  # Don't recurse - we already flagged this pattern
        # Recurse into slice to find Any in nested types (e.g., list[Any], dict[str, list[Any]])
        self._check_any_in_annotation(annotation.slice)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Track class context for attribute handling."""
        old_in_class: bool = self._in_class
        old_class_attrs: set[str] = self._class_attrs
        self._in_class = True
        self._class_attrs = set()
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                self._class_attrs.add(item.target.id)
        self.generic_visit(node)
        self._in_class = old_in_class
        self._class_attrs = old_class_attrs

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition and track context."""
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definition."""
        self._visit_function(node)

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Common logic for function definitions."""
        old_state: dict[str, object] = self._save_function_state()
        self._init_function_state()
        self._collect_function_args(node)
        self._collect_annotated_vars(node)
        self._check_function_annotations(node)
        self.generic_visit(node)
        self._restore_function_state(old_state)

    def _save_function_state(self) -> dict[str, object]:
        """Save current function state.

        Returns:
            Dictionary containing current function state.
        """
        return {
            "in_function": self._in_function,
            "function_args": self._function_args,
            "annotated_vars": self._annotated_vars,
            "collection_none_vars": self._collection_none_vars,
            "empty_dict_vars": self._empty_dict_vars,
        }

    def _init_function_state(self) -> None:
        """Initialize state for new function."""
        self._in_function = True
        self._function_args = set()
        self._annotated_vars = set()
        self._collection_none_vars = set()
        self._empty_dict_vars = set()

    def _restore_function_state(self, state: dict[str, object]) -> None:
        """Restore previous function state."""
        self._in_function = bool(state["in_function"])
        func_args: object = state["function_args"]
        annotated: object = state["annotated_vars"]
        collection_none: object = state["collection_none_vars"]
        empty_dict: object = state["empty_dict_vars"]
        self._function_args = set(func_args) if isinstance(func_args, set) else set()
        self._annotated_vars = set(annotated) if isinstance(annotated, set) else set()
        self._collection_none_vars = set(collection_none) if isinstance(collection_none, set) else set()
        self._empty_dict_vars = set(empty_dict) if isinstance(empty_dict, set) else set()

    def _collect_function_args(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Collect function argument names."""
        for arg in node.args.args:
            self._function_args.add(arg.arg)
        for arg in node.args.posonlyargs:
            self._function_args.add(arg.arg)
        for arg in node.args.kwonlyargs:
            self._function_args.add(arg.arg)
        if node.args.vararg:
            self._function_args.add(node.args.vararg.arg)
        if node.args.kwarg:
            self._function_args.add(node.args.kwarg.arg)

    def _collect_annotated_vars(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Collect all annotated assignments in function."""
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                self._annotated_vars.add(stmt.target.id)

    def _check_function_annotations(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Check function signature for PSP010 and PSP017."""
        self._check_quoted_annotation(node.returns, node)
        self._check_any_in_annotation(node.returns)
        all_args: list[ast.arg] = node.args.args + node.args.posonlyargs + node.args.kwonlyargs
        for arg in all_args:
            self._check_quoted_annotation(arg.annotation, node)
            self._check_any_in_annotation(arg.annotation)
        if node.args.vararg:
            self._check_quoted_annotation(node.args.vararg.annotation, node)
            self._check_any_in_annotation(node.args.vararg.annotation)
        if node.args.kwarg:
            self._check_quoted_annotation(node.args.kwarg.annotation, node)
            self._check_any_in_annotation(node.args.kwarg.annotation)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        """Track comprehension context."""
        self._visit_comprehension(node)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        """Track comprehension context."""
        self._visit_comprehension(node)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        """Track comprehension context."""
        self._visit_comprehension(node)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        """Track comprehension context."""
        self._visit_comprehension(node)

    def _visit_comprehension(self, node: ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp) -> None:
        """Common logic for comprehensions."""
        old_in_comprehension: bool = self._in_comprehension
        self._in_comprehension = True
        self.generic_visit(node)
        self._in_comprehension = old_in_comprehension

    def visit_For(self, node: ast.For) -> None:
        """Handle for loop - loop variables don't need annotations."""
        loop_vars: set[str] = _extract_names(node.target)
        old_annotated: set[str] = self._annotated_vars.copy()
        self._annotated_vars.update(loop_vars)
        self.generic_visit(node)
        self._annotated_vars = old_annotated

    def visit_With(self, node: ast.With) -> None:
        """Handle with statement - context manager variables don't need annotations."""
        with_vars: set[str] = set()
        for item in node.items:
            if item.optional_vars:
                with_vars.update(_extract_names(item.optional_vars))
        old_annotated: set[str] = self._annotated_vars.copy()
        self._annotated_vars.update(with_vars)
        self.generic_visit(node)
        self._annotated_vars = old_annotated

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """Handle except handler - exception variable doesn't need annotation."""
        old_annotated: set[str] = self._annotated_vars.copy()
        if node.name:
            self._annotated_vars.add(node.name)
        self.generic_visit(node)
        self._annotated_vars = old_annotated

    def visit_Assign(self, node: ast.Assign) -> None:
        """Check for unannotated local variable assignments (PSP001)."""
        if self._in_function and not self._in_comprehension:
            for target in node.targets:
                self._check_unannotated_assignment(target, node)
        self.generic_visit(node)

    def _check_unannotated_assignment(self, target: ast.AST, node: ast.Assign) -> None:
        """Check single assignment target for missing annotation."""
        if isinstance(target, ast.Name):
            self._check_name_assignment(target, node)
        elif isinstance(target, ast.Tuple | ast.List):
            for elt in target.elts:
                self._check_unannotated_assignment(elt, node)

    def _check_name_assignment(self, target: ast.Name, node: ast.Assign) -> None:
        """Check if name assignment needs annotation."""
        var_name: str = target.id
        if self._should_skip_annotation(var_name, node.value):
            return
        self._add_violation(
            node,
            "PSP001",
            f"Local variable '{var_name}' must have a type annotation",
        )

    def _should_skip_annotation(self, var_name: str, value: ast.expr | None) -> bool:
        """Check if variable should skip annotation requirement.

        Returns:
            True if annotation should be skipped, False otherwise.
        """
        if var_name in self._function_args:
            return True
        if var_name in self._annotated_vars:
            return True
        if var_name.startswith("_"):
            return True
        if var_name in self.SKIP_VARS:
            return True
        return _is_constructor_call(value)

    def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
        """Handle walrus operator - these don't need separate annotation."""
        if isinstance(node.target, ast.Name):
            self._annotated_vars.add(node.target.id)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        """Check annotated assignments for PSP005, PSP010, PSP011, PSP012, PSP013, PSP017."""
        self._check_quoted_annotation(node.annotation, node)
        self._check_any_in_annotation(node.annotation)
        if isinstance(node.target, ast.Name):
            self._check_annotated_assignment(node)
        self.generic_visit(node)

    def _check_annotated_assignment(self, node: ast.AnnAssign) -> None:
        """Check annotated assignment for various rules."""
        if not isinstance(node.target, ast.Name):
            return
        var_name: str = node.target.id
        if _is_collection_or_none_type(node.annotation):
            self._collection_none_vars.add(var_name)
        is_json_dict: bool = _is_json_dict_type(node.annotation, self.MULTILINE_DICT_TYPES)
        if var_name in self.TYPED_DICT_NAMES:
            # Check for PSP011 (None initialization) and PSP013 (empty dict in API calls)
            self._check_typed_dict_var(node, var_name)
            # If also typed as JsonDict, do recursive nested structure checking
            if is_json_dict:
                self._check_json_dict_nested_only(node, var_name)
        elif is_json_dict:
            self._check_json_dict_var(node, var_name)

    def _check_typed_dict_var(self, node: ast.AnnAssign, var_name: str) -> None:
        """Check typed dict variable for PSP005, PSP011, PSP013."""
        if isinstance(node.value, ast.Dict) and not node.value.keys:
            self._empty_dict_vars.add(var_name)
        if isinstance(node.value, ast.Constant) and node.value.value is None:
            self._add_violation(
                node,
                "PSP011",
                f"Variable '{var_name}' should be initialized with empty dict `{{}}`, not `None`. Use `{var_name}: dict[str, str] = {{}}` and add keys conditionally.",
            )
        if node.value is not None and isinstance(node.value, ast.Dict):
            self._check_dict_multiline(node.value, var_name)

    def _check_json_dict_var(self, node: ast.AnnAssign, var_name: str) -> None:
        """Check JsonDict variable for PSP005 (multiline formatting with nested structures).

        Skipped for test files to allow concise inline dicts in test code.
        """
        if self._is_test_file:
            return
        if node.value is not None and isinstance(node.value, ast.Dict):
            self._check_dict_multiline_recursive(node.value, var_name)

    def _check_json_dict_nested_only(self, node: ast.AnnAssign, var_name: str) -> None:
        """Check only nested structures in JsonDict (top-level already checked by _check_typed_dict_var).

        Skipped for test files to allow concise inline dicts in test code.
        """
        if self._is_test_file:
            return
        if node.value is not None and isinstance(node.value, ast.Dict):
            # Skip top-level check, only check nested structures
            for value in node.value.values:
                if value is not None:
                    self._check_nested_structure(value, var_name)

    def _check_dict_multiline(self, dict_node: ast.Dict, var_name: str) -> None:
        """Check that dict has each key-value pair on a separate line (PSP005)."""
        if not dict_node.keys:
            return
        if len(dict_node.keys) > 1:
            self._check_multiline_dict(dict_node, var_name)
        elif len(dict_node.keys) == 1:
            self._check_single_item_dict(dict_node, var_name)

    def _check_dict_multiline_recursive(self, dict_node: ast.Dict, var_name: str) -> None:
        """Check that dict and all nested dicts/lists have proper multiline formatting (PSP005)."""
        if not dict_node.keys:
            return
        # Check the top-level dict first
        if len(dict_node.keys) > 1:
            self._check_multiline_dict(dict_node, var_name)
        elif len(dict_node.keys) == 1:
            self._check_single_item_dict(dict_node, var_name)
        # Recursively check all nested structures
        for value in dict_node.values:
            if value is not None:
                self._check_nested_structure(value, var_name)

    def _check_nested_structure(self, node: ast.expr, var_name: str) -> None:
        """Recursively check nested dicts and lists for multiline formatting."""
        if isinstance(node, ast.Dict):
            self._check_nested_dict(node, var_name)
        elif isinstance(node, ast.List):
            self._check_nested_list(node, var_name)

    def _check_nested_dict(self, dict_node: ast.Dict, var_name: str) -> None:
        """Check nested dict for multiline formatting."""
        if not dict_node.keys:
            return
        # Check if this nested dict is on a single line
        if self._is_dict_on_single_line(dict_node):
            self._add_violation(
                dict_node,
                "PSP005",
                f"Nested dict in '{var_name}' must have each key-value pair on a separate line",
            )
        # Recursively check nested structures
        for value in dict_node.values:
            if value is not None:
                self._check_nested_structure(value, var_name)

    def _check_nested_list(self, list_node: ast.List, var_name: str) -> None:
        """Check list elements for nested dicts that need multiline formatting."""
        for element in list_node.elts:
            if isinstance(element, ast.Dict):
                self._check_nested_dict(element, var_name)
            elif isinstance(element, ast.List):
                self._check_nested_list(element, var_name)

    def _is_dict_on_single_line(self, dict_node: ast.Dict) -> bool:
        """Check if a dict is written on a single line.

        Returns:
            True if dict is on single line, False otherwise.
        """
        if not dict_node.keys:
            return False
        if not self.source_lines:
            return False
        # Get the line range of the dict
        start_line: int = dict_node.lineno
        end_line: int = dict_node.end_lineno or start_line
        # If start and end are on same line, it's a single-line dict
        return start_line == end_line

    def _check_multiline_dict(self, dict_node: ast.Dict, var_name: str) -> None:
        """Check multi-item dict for multiline formatting."""
        key_lines: set[int] = set()
        for key in dict_node.keys:
            if key is not None:
                key_lines.add(key.lineno)
        dict_start_line: int = dict_node.lineno
        first_key_line: int | None = dict_node.keys[0].lineno if dict_node.keys[0] else None
        if first_key_line == dict_start_line and len(key_lines) == 1:
            self._add_violation(
                dict_node,
                "PSP005",
                f"Dict '{var_name}' must have each key-value pair on a separate line",
            )

    def _check_single_item_dict(self, dict_node: ast.Dict, var_name: str) -> None:
        """Check single-item dict for multiline formatting."""
        if not self.source_lines:
            return
        dict_start_line: int = dict_node.lineno
        first_key_line: int | None = dict_node.keys[0].lineno if dict_node.keys[0] else None
        if first_key_line != dict_start_line:
            return
        if dict_start_line > len(self.source_lines):
            return
        line_content: str = self.source_lines[dict_start_line - 1]
        if "{" in line_content and "}" in line_content:
            self._add_violation(
                dict_node,
                "PSP005",
                f"Dict '{var_name}' must have each key-value pair on a separate line (even single-item dicts)",
            )

    def visit_If(self, node: ast.If) -> None:
        """Check for truthy checks on collection | None variables (PSP012)."""
        if isinstance(node.test, ast.Name):
            var_name: str = node.test.id
            if var_name in self._collection_none_vars:
                self._add_violation(
                    node.test,
                    "PSP012",
                    f"Use `if {var_name} is not None:` instead of `if {var_name}:` for collection | None types (empty list/dict is falsy but may be a valid value)",
                )
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        """Check for assert statements in production code (PSP015)."""
        if not self._is_test_file:
            self._add_violation(
                node,
                "PSP015",
                "Don't use `assert` in production code. Use explicit checks with `raise` or proper type design. `assert` is only allowed in test files (tests/ directory).",
            )
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        """Track binary operation context to avoid false positives in PSP006."""
        old_in_binop: bool = self._in_binop
        self._in_binop = True
        self.generic_visit(node)
        self._in_binop = old_in_binop

    def visit_Compare(self, node: ast.Compare) -> None:
        """Track status_code comparison context for PSP006."""
        is_status_code_compare: bool = isinstance(node.left, ast.Attribute) and node.left.attr == "status_code"
        old_in_status_code_compare: bool = self._in_status_code_compare
        if is_status_code_compare:
            self._in_status_code_compare = True
        self.generic_visit(node)
        self._in_status_code_compare = old_in_status_code_compare

    def visit_Call(self, node: ast.Call) -> None:
        """Check API request method calls (PSP002, PSP003, PSP004, PSP014, PSP016)."""
        func_name: str | None = get_method_name(node)
        self._check_print_call(node, func_name)
        self._check_cast_call(node, func_name)
        if func_name is not None and func_name in self.API_REQUEST_METHODS:
            self._check_api_request_call(node, func_name)
        self.generic_visit(node)

    def _check_print_call(self, node: ast.Call, func_name: str | None) -> None:
        """Check for print() calls in non-test files (PSP014)."""
        if func_name == "print" and isinstance(node.func, ast.Name) and not self._is_test_file:
            self._add_violation(
                node,
                "PSP014",
                "Don't use `print()` in library code. Use `logging` module instead (e.g., `logger.info()`, `logger.debug()`).",
            )

    def _check_cast_call(self, node: ast.Call, func_name: str | None) -> None:
        """Check for cast() calls (PSP016)."""
        if func_name == "cast" and self._has_cast_import and not self._is_test_file:
            self._add_violation(
                node,
                "PSP016",
                "Don't use `typing.cast()`. Use proper type design instead: build typed data structures explicitly or use `@overload` decorators.",
            )

    def visit_Constant(self, node: ast.Constant) -> None:
        """Check for literals that should use enum constants (PSP006, PSP007, PSP008, PSP009)."""
        if not self._in_function:
            return
        value: object = node.value
        if isinstance(value, int):
            self._check_http_status_code(node, value)
        elif isinstance(value, str):
            self._check_string_constants(node, value)
        self.generic_visit(node)

    def _check_http_status_code(self, node: ast.Constant, value: int) -> None:
        """Check for numeric HTTP status codes (PSP006)."""
        if value not in self.HTTP_STATUS_CODES:
            return
        if not self._in_status_code_compare:
            return
        if self._in_binop:
            return
        enum_name: str = self.HTTP_STATUS_CODES[value]
        self._add_violation(
            node,
            "PSP006",
            f"Use HTTPStatus.{enum_name} instead of numeric status code {value}",
        )

    def _check_string_constants(self, node: ast.Constant, value: str) -> None:
        """Check for string literals that should use enums (PSP007, PSP008, PSP009)."""
        if value in self.HEADER_VALUES:
            self._add_violation(
                node,
                "PSP007",
                f'Use {self.HEADER_VALUES[value]} instead of string literal "{value}"',
            )
        if value in self.MEDIA_TYPE_VALUES:
            self._add_violation(
                node,
                "PSP008",
                f'Use {self.MEDIA_TYPE_VALUES[value]} instead of string literal "{value}"',
            )
        if value in self.AUTH_SCHEME_VALUES:
            self._add_violation(
                node,
                "PSP009",
                f'Use {self.AUTH_SCHEME_VALUES[value]} instead of string literal "{value}"',
            )

    def _check_api_request_call(self, node: ast.Call, method_name: str) -> None:
        """Check api_request_* call for style violations (PSP002, PSP003, PSP004, PSP013)."""
        if node.args:
            self._check_url_argument(node.args[0], method_name)
        for keyword in node.keywords:
            if keyword.arg in self.MUST_BE_VARIABLE_ARGS:
                self._check_keyword_argument(keyword, method_name)

    def _check_url_argument(self, url_arg: ast.expr, method_name: str) -> None:
        """Check URL argument for PSP003 and PSP004."""
        if isinstance(url_arg, ast.Name):
            return
        self._check_url_type_violation(url_arg, method_name)
        self._check_url_query_params(url_arg)

    def _check_url_type_violation(self, url_arg: ast.expr, method_name: str) -> None:
        """Check URL argument type for PSP003."""
        if isinstance(url_arg, ast.JoinedStr):
            self._add_violation(
                url_arg,
                "PSP003",
                f"URL in {method_name}() must be a variable, not an f-string. Assign to 'url' variable first.",
            )
        elif isinstance(url_arg, ast.BinOp):
            self._add_violation(
                url_arg,
                "PSP003",
                f"URL in {method_name}() must be a variable, not a concatenation. Assign to 'url' variable first.",
            )
        elif isinstance(url_arg, ast.Constant):
            self._add_violation(
                url_arg,
                "PSP003",
                f"URL in {method_name}() must be a variable, not a literal. Assign to 'url' variable first.",
            )

    def _check_url_query_params(self, url_arg: ast.expr) -> None:
        """Check URL argument for query parameters (PSP004)."""
        if isinstance(url_arg, ast.JoinedStr):
            url_str: str = reconstruct_fstring(url_arg)
            if "?" in url_str or "&" in url_str:
                self._add_violation(
                    url_arg,
                    "PSP004",
                    "Query parameters must use params= dict, not URL concatenation",
                )
        elif isinstance(url_arg, ast.BinOp) and contains_query_params(url_arg):
            self._add_violation(
                url_arg,
                "PSP004",
                "Query parameters must use params= dict, not URL concatenation",
            )

    def _check_keyword_argument(self, keyword: ast.keyword, method_name: str) -> None:
        """Check keyword argument for PSP002 and PSP013."""
        if keyword.arg in {"params", "headers"} and isinstance(keyword.value, ast.Name) and keyword.value.id in self._empty_dict_vars:
            self._add_violation(
                keyword.value,
                "PSP013",
                f"Use `{keyword.value.id} or None` instead of `{keyword.value.id}` to convert empty dict to None",
            )
            return
        if isinstance(keyword.value, ast.Name | ast.Call | ast.BoolOp):
            return
        if isinstance(keyword.value, ast.Constant) and keyword.value.value is None:
            return
        if isinstance(keyword.value, ast.Dict):
            self._add_violation(
                keyword.value,
                "PSP002",
                f"Argument '{keyword.arg}' in {method_name}() must be a variable, not an inline dict. Assign to '{keyword.arg}' variable first.",
            )
        else:
            self._add_violation(
                keyword.value,
                "PSP002",
                f"Argument '{keyword.arg}' in {method_name}() must be a variable. Assign to '{keyword.arg}' variable first.",
            )


# Helper functions


def _check_is_test_file(file_path: Path) -> bool:
    """Check if file is in tests directory or testing module.

    Returns:
        True if file is a test file, False otherwise.
    """
    path_str: str = str(file_path)
    if "/tests/" in path_str or path_str.startswith("tests/") or "\\tests\\" in path_str:
        return True
    if "/testing/" in path_str or "\\testing\\" in path_str:
        return True
    return file_path.name.startswith("test_")


def _parse_suppressed_codes(ignore_part: str) -> set[str]:
    """Parse suppressed codes from psp-ignore comment.

    Returns:
        Set of suppressed PSP codes.
    """
    suppressed_codes: set[str] = set()
    for part in ignore_part.split(","):
        code_match: str = part.strip().split()[0] if part.strip() else ""
        if code_match and code_match.startswith("PSP"):
            suppressed_codes.add(code_match)
    return suppressed_codes


def _get_quoted_type_message(type_name: str, has_future_annotations: bool) -> str:
    """Get appropriate message for quoted type annotation.

    Returns:
        Error message string for quoted type annotation.
    """
    if has_future_annotations:
        return f'Remove unnecessary quotes from "{type_name}", `from __future__ import annotations` already handles forward references'
    return f'Don\'t use quoted type "{type_name}", use `from __future__ import annotations` instead'


def _is_literal_subscript(annotation: ast.Subscript) -> bool:
    """Check if subscript is Literal[].

    Returns:
        True if annotation is Literal[], False otherwise.
    """
    if isinstance(annotation.value, ast.Name) and annotation.value.id == "Literal":
        return True
    return isinstance(annotation.value, ast.Attribute) and annotation.value.attr == "Literal"


def _is_dict_str_any(annotation: ast.Subscript) -> bool:
    """Check if annotation is dict[str, Any].

    Returns:
        True if annotation is dict[str, Any], False otherwise.
    """
    if not isinstance(annotation.value, ast.Name) or annotation.value.id != "dict":
        return False
    if not isinstance(annotation.slice, ast.Tuple) or len(annotation.slice.elts) != 2:
        return False
    first_elt: ast.expr = annotation.slice.elts[0]
    second_elt: ast.expr = annotation.slice.elts[1]
    return isinstance(first_elt, ast.Name) and first_elt.id == "str" and isinstance(second_elt, ast.Name) and second_elt.id == "Any"


def _extract_names(node: ast.AST) -> set[str]:
    """Extract variable names from assignment target.

    Returns:
        Set of variable names found in the target.
    """
    names: set[str] = set()
    if isinstance(node, ast.Name):
        names.add(node.id)
    elif isinstance(node, ast.Tuple | ast.List):
        for elt in node.elts:
            names.update(_extract_names(elt))
    elif isinstance(node, ast.Starred):
        names.update(_extract_names(node.value))
    return names


def _is_constructor_call(node: ast.expr | None) -> bool:
    """Check if expression is a constructor call (ClassName(...)).

    Returns:
        True if node is a constructor call, False otherwise.
    """
    if not isinstance(node, ast.Call):
        return False
    if isinstance(node.func, ast.Name):
        return node.func.id[0].isupper() if node.func.id else False
    if isinstance(node.func, ast.Attribute):
        return node.func.attr[0].isupper() if node.func.attr else False
    return False


def _is_collection_or_none_type(annotation: ast.expr) -> bool:
    """Check if annotation is list[...] | None or dict[...] | None.

    Returns:
        True if annotation is a collection | None type, False otherwise.
    """
    if not isinstance(annotation, ast.BinOp) or not isinstance(annotation.op, ast.BitOr):
        return False
    left_is_none: bool = isinstance(annotation.left, ast.Constant) and annotation.left.value is None
    right_is_none: bool = isinstance(annotation.right, ast.Constant) and annotation.right.value is None
    if not (left_is_none or right_is_none):
        return False
    type_side: ast.expr = annotation.right if left_is_none else annotation.left
    return _is_collection_type(type_side)


def _is_collection_type(annotation: ast.expr) -> bool:
    """Check if annotation is a collection type (list, dict, set, but not str).

    Returns:
        True if annotation is a collection type, False otherwise.
    """
    collection_names: set[str] = {"list", "dict", "set", "frozenset", "List", "Dict", "Set"}
    if isinstance(annotation, ast.Subscript) and isinstance(annotation.value, ast.Name):
        return annotation.value.id in collection_names
    if isinstance(annotation, ast.Name):
        return annotation.id in collection_names
    return False


def _is_json_dict_type(annotation: ast.expr | None, type_names: frozenset[str]) -> bool:
    """Check if annotation is one of the specified dict types (e.g., JsonDict).

    Returns:
        True if annotation is a JsonDict or similar type, False otherwise.
    """
    if annotation is None:
        return False
    if isinstance(annotation, ast.Name):
        return annotation.id in type_names
    return False
