# CLAUDE.md

- **The version in `pyproject.toml` is pipeline-managed — never hand-edit it** — Release Please (`release-type: python` in `ci.yml`) writes the bumped version into the file in its release PR, and `build-and-publish` runs a plain `uv build` over whatever is committed. The committed value is therefore the real released version, not a `0.0.0` placeholder; hand-editing it ships a mis-versioned artifact or fights the release PR.
- **Custom AST linter (PSP001–PSP017)** runs in `uv run tox` alongside ruff/mypy. Suppress with `# psp-ignore: PSP0XX`, NOT `# noqa`. The linter catches project-specific rules that ruff cannot enforce.
- **All local variables must have explicit type annotations** — even obvious ones: `url: str = f"..."` not `url = f"..."`. (PSP001)
- **No `Any`, `cast()`, or `assert` in production code** — use `JsonDict` for `dict[str, Any]`, `@overload` for type-safe factories, `raise` instead of `assert`. OK in test files. Ruff's `ANN401` is ignored because `Any` is correct at JSON and `**kwargs` boundaries, but PSP017 still enforces the wider rule. (PSP015–PSP017)
- **Use project enums, not string literals** — `Header.ACCEPT`, `MediaType.JSON`, `AuthScheme.BEARER` (from `python_sbb_polarion.types`), `HTTPStatus.OK` (from `http`). (PSP006–PSP009)
- **API request args must be named variables with type annotations** — no inline dicts or f-strings in `api_request_*()` calls. Multiline dict format even for single entries. Standard types: `headers: dict[str, str]`, `params: dict[str, str]`, `data: JsonDict`, `files: FilesDict`. (PSP002/PSP003/PSP005)
- **Empty dicts use `or None` when passed to API methods** — `api_request_get(url, params=params or None)`. (PSP013)
- **API methods always return `Response`, never `None`** — don't add `if response is None` checks. `RequestException` is raised only for network errors; HTTP 4xx/5xx are valid `Response` objects.
- **Use `from __future__ import annotations`** not quoted forward references like `"JsonDict"`. (PSP010)
- **Prefer explicit `if-else` over ternary operators** — but SIM108 is enabled, so a deliberate `if-else` carries `# noqa: SIM108` and the reason.
- **None checks depend on type** — `str | None`: use `if var:`. `list | None` / `dict | None` / `int | None`: use `if var is not None:`.
- **NamedTuple fields: snake_case. TypedDict fields: camelCase allowed** when matching JSON API schema keys.
- **Extension APIs map to GitHub repos** at `SchweizerischeBundesbahnen/ch.sbb.polarion.extension.*` — verification tests validate methods against their OpenAPI specs.
- **`@deprecated_method` goes innermost, below `@restapi_endpoint`** — for extension methods duplicating a `PolarionApiV1` operation. A deprecated convenience method must issue its own HTTP request rather than delegating to other deprecated methods, so the caller sees exactly one `DeprecationWarning` without the thread-unsafe `warnings.catch_warnings()`. No method carries it right now — the admin-utility duplicates it marked were removed in 4.0.0 — so the decorator stands ready for the next deprecation cycle.
- **SBB GitHub Actions workflows are pinned to `@main`, not hash-pinned** — `SchweizerischeBundesbahnen/*` reusable workflows intentionally use branch refs. This is enforced by `zizmor.yml`. Do not convert these to commit hash pins.
