# CLAUDE.md

- **Version `0.0.0` in `pyproject.toml` is intentional** — the CI/CD pipeline (Release Please) sets the real version from git tags. Never change it.
- **Custom AST linter (PSP001–PSP017)** runs in `uv run tox` alongside ruff/mypy. Suppress with `# psp-ignore: PSP0XX`, NOT `# noqa`. The linter catches project-specific rules that ruff cannot enforce.
- **All local variables must have explicit type annotations** — even obvious ones: `url: str = f"..."` not `url = f"..."`. (PSP001)
- **No `Any`, `cast()`, or `assert` in production code** — use `JsonDict` for `dict[str, Any]`, `@overload` for type-safe factories, `raise` instead of `assert`. OK in test files. (PSP015–PSP017)
- **Use project enums, not string literals** — `Header.ACCEPT`, `MediaType.JSON`, `AuthScheme.BEARER` (from `python_sbb_polarion.types`), `HTTPStatus.OK` (from `http`). (PSP006–PSP009)
- **API request args must be named variables with type annotations** — no inline dicts or f-strings in `api_request_*()` calls. Multiline dict format even for single entries. Standard types: `headers: dict[str, str]`, `params: dict[str, str]`, `data: JsonDict`, `files: FilesDict`. (PSP002/PSP003/PSP005)
- **Empty dicts use `or None` when passed to API methods** — `api_request_get(url, params=params or None)`. (PSP013)
- **API methods always return `Response`, never `None`** — don't add `if response is None` checks. `RequestException` is raised only for network errors; HTTP 4xx/5xx are valid `Response` objects.
- **Use `from __future__ import annotations`** not quoted forward references like `"JsonDict"`. (PSP010)
- **Prefer explicit `if-else` over ternary operators** — SIM108 is intentionally disabled.
- **None checks depend on type** — `str | None`: use `if var:`. `list | None` / `dict | None` / `int | None`: use `if var is not None:`.
- **NamedTuple fields: snake_case. TypedDict fields: camelCase allowed** when matching JSON API schema keys.
- **Extension APIs map to GitHub repos** at `SchweizerischeBundesbahnen/ch.sbb.polarion.extension.*` — verification tests validate methods against their OpenAPI specs.
- **SBB GitHub Actions workflows are pinned to `@main`, not hash-pinned** — `SchweizerischeBundesbahnen/*` reusable workflows intentionally use branch refs. This is enforced by `zizmor.yml`. Do not convert these to commit hash pins.
